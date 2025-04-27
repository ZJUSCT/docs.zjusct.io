---
title: Quick Guide to CUDA Profiling
date:
  created: 2018-12-07 23:48:33
authors: [小妹妹]
categories: [Tech, CUDA, Profile]
---

在并行计算领域，很难通过纯理论的分析来确定程序的性能，`GPGPU`这种基于特定计算架构的计算任务更甚。事实上，很多制约并行算法性能的瓶颈很可能不在算法本身（比如资源调度障碍）。因此，对给定程序进行充分的性能测试与后续分析是相当必要的调优方法。

`Nvidia`提供了`nvprof`，`nvvp`，`Nsight`三种 cuda 可用的性能分析工具，本文将简述配合使用`nvprof`与`nvvp`的 cuda 程序性能分析方法。

<!-- more -->

## Check Out Device Properties

由于 cuda 程序的线程/块分配方案与程序运行的的硬件高度相关，故对目标平台的硬件参数有一定程度的了解是相当有必要的。我们可以使用`cudaGetDeviceProperties()`函数获取设备的各项属性，下述代码可以结合`cuda_runtime_api.h#1218`处`struct cudaDeviceProp`的定义和各属性的相应注解自行理解。

```cpp
int nDevices;
cudaDeviceProp prop;
cudaGetDeviceCount( &nDevices );
for ( auto i = 0; i != nDevices; ++i )
{
 cudaGetDeviceProperties( &prop, i );
 // check out interesting property
}
```

## Profile Using Nvprof

### Quick Start

```bash
nvprof --help
```

### Metrics

* 使用`--query-metrics`列出所有可测试的性能指标。
* 使用`--metrics sm_efficiency,warp_execution_efficiency,...`指定要测试的性能指标。

### PC Sampling

在 CC5.2 或更高的设备上支持使用 PC 采样 (PC sampling) 技术。

PC 采样技术通过`Round-Robin`方法对 SM 中所有活动线程束的 PC 状态进行采样，采样结果包含如下两种可能：

* 线程束完成了当前指令。
* 线程束被`stall`，不能完成当前指令，并可以给出`stall`的原因。

事实上线程束被`stall`并不代表指令流水线处于`stall`状态，因为其他正常运行的线程束可以利用计算资源。

CC6.0 以上的设备对 PC 采样方法进行了改进，通过检查线程束调度器是否执行指令来确定指令流水线是否真正处于`stall`状态，从而能正确指示指令`stall`的原因。

## Data Visualize Using Nvvp

`nvvp`可以导入`nvprof`的分析结果，可视化显示统计图表，并且建议性地指出程序可能存在的瓶颈。

<figure markdown>
![以饼状图显示各类 stall 比重](./12-07-cuprof.assets/a.webp)
<figcaption>
    以饼状图显示各类 stall 比重
    </figcaption>
</figure>

<figure markdown>
![以频谱显示各类指令比例](./12-07-cuprof.assets/b.webp)
<figcaption>
    以频谱显示各类指令比例
</figcaption>
</figure>

<figure markdown>
![通过 source file mapping 可视化指令 stall 状态，需要在编译选项中指定`-lineinfo`](./12-07-cuprof.assets/d.webp)
<figcaption>
    通过 source file mapping 可视化指令 stall 状态，需要在编译选项中指定`-lineinfo`
    </figcaption>
</figure>

```bash
nvprof -f --kernels "kernelName" --analysis-metrics -o a.nvvp <task> <args>
nvvp a.nvvp
```

这里我使用的方法是在集群上用`nvprof`做性能测试，之后将分析结果`*.nvvp`传回本地用`nvvp`做可视化。

## Ext. Remarks

### Tradeoff Between Registers and Threads

在实际 Profiling 中重新认识了这个问题。

在默认情况下，`nvcc`为每个线程分配`maxRegsPerThread`个数的寄存器，在*Tesla K40*上，这个值为 64。同时，每个 SM 持有为 65536 个寄存器，这意味着单个 SM 中的线程数最多不超过 1024。通过检查参数表，我们发现该设备单个 SM 可容纳线程数为 2048。这意味着我们计算任务的 GPU 利用率最大只有 50%（所有 SM 均满载的状态下）。

在这种情况下，如果我们将分配给单个线程的寄存器数目减半，则最大 GPU 利用率可以达到 100%。但若发生寄存器溢出（register spilling），溢出的存储空间被放到片外的 local memory，访问速度在（同在片外的）global memory 级别。

在实际的 CUDA 核函数中，能全部利用 64 个寄存器的情况很少。寄存器的使用情况可以在 nvvp 中检查，如果发现有大量寄存器浪费，可以立即减少寄存器数量。在大多数情况下，可以结合计算任务的量级和性质来调节线程最大寄存器数，从而达到有针对性的性能调优。

在`nvcc`中指定单个线程最大寄存器数，可以添加编译选项`-maxrregcount=N`。如果限定不修改编译选项或需要逐核函数指定，则需要使用`__launch_bounds__`限定符，如下（隐式地指定了最大寄存器个数）：

```cpp
__global__ void
__launch_bounds__(maxThreadsPerBlock, minBlocksPerMultiprocessor)
MyKernel(...)
{
    ...
}
```

在我的`path tracer`中对上述方法进行测试，将每线程的寄存器数减半为 32，SM 线程数加倍并满载，GPU 利用率由 30+ 提升到 70+，执行速度有 1.5 倍左右的提升。

### Tradeoff Between BlockDim and BlockPerSM

当一个块（block）中的所有线程束（warp）全部完成时，这个块才可以被 SM 调度。如果块的大小过大，则块的运行速度受单个线程束约束的开销就越大（如果算法并行度很高，增大块的大小不失为一个好选择）；如果块的大小过小，则一方面 SM 可能无法达到其最大利用率（受`maxBlocksPerSM`的限制），另一方面 SM 调度块的额外开销也会增大。尤其是针对不同特点的计算任务有不同的更优选择，如`divergency`较高的任务更适合较小的 BlockDim。所以在选择 BlockDim 时不仅要在算法的适应性上做考虑，还要通过多次性能测试来进行针对性的优化。

### Beware of Ladder Effects

注意计算资源分配时要注意分配的资源量要能够被组别整除，否则会出现断层状的资源浪费现象。

<figure markdown>
![每块线程数与 SM 中最大线程束数的关系](./12-07-cuprof.assets/c.webp)
<figcaption>
    每块线程数与 SM 中最大线程束数的关系
</figcaption>
</figure>
