---
tags:
  - 不完善
---

# 启动过程

!!! abstract

    本文档描述从按下电源键到 Bootloader 引导系统为止，计算机的启动过程。本文以 x86 架构和 Linux 系统为主。

    阅读本文**不**需要汇编和计算机体系结构的知识。

    PXE 相关内容见 [PXE](../diskless/pxe.md)。

!!! quote

    如果你想要在代码层面探究计算机启动早期的工作原理，可以尝试从下面的书籍中开始，至少比动辄几百上千页的标准好读一些。

    - [:simple-github: pinczakko/BIOS-Disassembly-Ninjutsu-Uncovered](https://github.com/pinczakko/BIOS-Disassembly-Ninjutsu-Uncovered)：BIOS 反汇编指南。
    - [Beyond BIOS: Developing with the Unified Extensible Firmware Interface](http://ftp.kolibrios.org/users/seppe/UEFI/Beyond_BIOS_Second_Edition_Digital_Edition_(15-12-10)%20.pdf)：UEFI 开发指南。

    本文不会像这些书籍一样深入探讨实现，而是从用户的角度描述原理。

x86 架构启动过程分为两种：BIOS（Legacy）和 UEFI。BIOS 因为**没有标准且老旧**，现已被 UEFI 取代。

如今服务器都使用 UEFI 启动。你会在 BIOS 选项中看到 CSM（Compatibility Support Module），这是为了兼容旧的 BIOS 启动方式。关闭它，系统就会完全使用 UEFI 启动。

## BIOS（Legacy）

!!! quote

    - [System Initialization (x86) - OSDev Wiki](https://wiki.osdev.org/System_Initialization_(x86))

BIOS 启动过程如下：

- **检测 RAM**：BIOS 需要 RAM 才能工作。为了使用 RAM，CPU 先运行在 ROM 中的代码，检测 RAM 的类型和大小。然后加载各种东西到 RAM，比如实模式中断向量表（Real Mode IVT）等。
- **硬件检测和初始化**：BIOS 检测并初始化各个总线上的设备，保存它们的信息供操作系统使用。BIOS 如果在硬件上检测到 ROM，就会将其映射到物理内存中。这一点在 PXE 启动中涉及网卡固件的地方会用到。
- **启动序列**：完成初始化后，BIOS 尝试寻找可启动的设备（如硬盘、光盘、USB、网卡等）。可启动的设备都有某种引导扇区（Boot Sector），BIOS 会将这个扇区加载到内存中，并跳转到这个扇区的代码执行。

## UEFI

!!! quote

    - [Understanding modern UEFI-based platform boot](https://depletionmode.com/uefi-boot.html)：详细介绍了 UEFI 的启动过程，还贴心地科普了一些硬件常识。
    - [UEFI - OSDev Wiki](https://wiki.osdev.org/UEFI)：简单介绍了 UEFI 的概念、与 BIOS 的对比，然后主要在讲 UEFI 应用程序的开发和调试，涉及 POSIX-EFI、GNU-EFI 和 OVMF 等。
    - [Specifications - Unified Extensible Firmware Interface Forum](https://uefi.org/specifications)

UEFI 规范支持的架构包括 IA-32、x64、AArch32、AArch64、RISC-V 和 LoongArch。

UEFI 的启动过程其实和 BIOS 差不多，只是 UEFI 有更多的功能和更好的设计：

- 标准化了平台初始化过程，可在厂商中立的基础上扩展。
- UEFI 支持从 FAT 分区的 GPT 或 MBR 启动设备中加载任意大小的 UEFI 应用程序，并且可以返回固件继续选择其他启动设备或显示诊断菜单。而 BIOS 只能从启动设备的 MBR 读取 512 字节的扁平二进制代码，且无法返回 BIOS。
- UEFI 通过内存中的“协议”集合提供可调用函数，协议行为受规范定义；UEFI 应用可定义自己的协议并供其他应用使用，函数调用方式标准化，符合现代编程习惯。而 BIOS 通过多种中断挂钩供 bootloader 访问系统资源，中断未标准化，依赖历史惯例。
- UEFI 有更好的开发环境，如 EDK2、GNU-EFI 和 POSIX-UEFI。而 BIOS 需要使用 NASM 和 GCC 等工具生成扁平二进制镜像。
- UEFI 仿真更方便，OVMF 是开源 UEFI 固件，已移植至 QEMU。

下面对 UEFI 启动的流程总结来自 [Understanding modern UEFI-based platform boot](https://depletionmode.com/uefi-boot.html)：

- Pre-UEFI：
    - 最开始 CPU 阻塞在 Reset 中断向量处。
    - PMC（Power Management Controller）给 CSME（Converged Security and Manageability Engine）上电。CSME ROM 启动并作为根信任开始。
    - 接着加载并验证 CPU 微码和 ACM（Authenticated Code Module）组件，使用安全认证方法确保系统完整性，最后加载并验证 OEM IBB（Initial Boot Block），确保系统安全启动。
- SEC（Security）：
    - 从复位向量开始启动处理器，切换到保护模式，并配置 CPU 缓存为 Cache-as-RAM（CAR）以支持后续的固件加载和执行。
    - 还负责处理平台的休眠状态恢复，并为后续的 Pre-EFI 初始化（PEI）阶段提供必要的系统信息。
- PEI（Pre-EFI）：
    - 完成硬件初始化（如内存、CPU、I/O 等），并通过 PEI Foundation 管理 PEIM（预 EFI 初始化模块）之间的协调与执行，同时将临时缓存内存（CAR）切换到主系统内存。
    - 负责生成 HOB（交接块），为后续阶段提供必要的信息。
- DXE（Driver eXecution Environment）：
    - 负责更高层次的硬件初始化和服务，如系统管理模式 (SMM)、网络、引导磁盘等，并通过 DXE 驱动程序与 EFI 系统表交互，确保平台在操作系统引导前正常运行
    - Secure Boot 确保在执行任何 EFI 应用程序之前，相关的 DXE 驱动程序会验证该应用程序的签名，以确保只有受信任的代码被加载，防止恶意软件在引导过程中执行。
- BDS（Boot Device Selection）：
    - 系统选择并启动引导设备，通常通过 UEFI 变量指定引导项。
    - 对于 Windows，BDS 阶段会加载 Windows 引导管理器（bootmgrfw.efi），并开始引导过程。
- TSL（Transient System Load）：由引导加载程序（如 Windows Boot Loader）负责，初始化操作系统的执行环境，加载内核和驱动程序，并在完成后移除引导时的 DXE 服务。
- RT（RunTime）：操作系统的运行时阶段，操作系统加载所需驱动并开始正常运行，剩余的 EFI 服务（如读取写入 UEFI 变量、关机等）由操作系统在运行时调用。

对应到 Linux 系统，我们熟悉的 GRUB 就是在 BDS 阶段加载的。`/boot/efi` 一般挂载为 EFI 分区，可以在其中找到 grub 的 EFI 文件。

```bash
$ duf
╭────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 2 local devices                                                                                │
├────────────┬────────┬────────┬────────┬───────────────────────────────┬───────┬────────────────┤
│ MOUNTED ON │   SIZE │   USED │  AVAIL │              USE%             │ TYPE  │ FILESYSTEM     │
├────────────┼────────┼────────┼────────┼───────────────────────────────┼───────┼────────────────┤
│ /          │ 464.3G │ 278.8G │ 183.1G │ [############........]  60.0% │ btrfs │ /dev/nvme1n1p2 │
│ /boot/efi  │ 511.0M │   4.4M │ 506.6M │ [....................]   0.9% │ vfat  │ /dev/nvme1n1p1 │
╰────────────┴────────┴────────┴────────┴───────────────────────────────┴───────┴────────────────╯
$ ls /boot/efi/EFI/debian
BOOTX64.CSV  fbx64.efi  grub.cfg  grubx64.efi  mmx64.efi  shimx64.efi
```

而对于 PXE 启动，应该在 DXE 阶段初始化网络设备，然后在 BDS 阶段选择网络设备启动，由网络设备固件提供的 UEFI 服务获取 PXE 引导程序，如 pxelinux 或 iPXE。

## 引导程序 `grub2`

!!! quote

    - [GNU GRUB Manual 2.12](https://www.gnu.org/software/grub/manual/grub/grub.html)
    - [基于 Grub 2.00 的 x86 内核引导流程--源代码情景分析（2） - 知乎](https://zhuanlan.zhihu.com/p/28300233)

## 内核启动参数

## initramfs 阶段

    - [Debian Wiki: BootProcess](https://wiki.debian.org/BootProcess)
    - [Debian Reference: Chapter 3. The system initialization](https://www.debian.org/doc/manuals/debian-reference/ch03.en.html)

### dracut

启动过程中遇到 dracut initqueue timeout 等问题，如何调试？我们需要了解 dracut 的基本工作原理。

dracut 是模块化的 initramfs 工具。可以在 `/usr/lib/dracut/modules.d/` 中找到各种模块，如 `95nfs`、`95iscsi` 等。每个模块的文件夹下都至少有一个 `module-setup.sh` 文件。生成 initramfs 时，它执行该文件中的 `check()`、`install()`、`installkernel()` 等函数，然后将结果打包成 initramfs。以 `nfs` 模块为例，它的：

- `check()` 函数检查了必要的二进制文件是否存在。
- `install()` 函数拷贝了一些文件到 initramfs，并在启动过程中的几个 Hook 点注册自定义脚本。

```bash title="dracut/modules.d/95nfs/module-setup.sh"
check() {
    require_any_binary rpcbind portmap || return 1
    # ...
}
install() {
    # ...
    inst_hook cmdline 90 "$moddir/parse-nfsroot.sh"
    inst_hook pre-udev 99 "$moddir/nfs-start-rpc.sh"
    inst_hook cleanup 99 "$moddir/nfsroot-cleanup.sh"
    # ...
    mkdir -m 0755 -p "$initdir/var/lib/nfs"
}
```

dracut 启动步骤如下：

- Hook: cmdline
- Hook: pre-udev
- Start Udev
- Hook: pre-trigger
- Trigger Udev
- Main Loop
    - Initqueue
    - Initqueue settled
    - Initqueue timeout
    - Initqueue online
    - Initqueue finished：在 udev 稳定后被调用，如果这里的所有脚本都返回 0，主循环将结束。可以在这里添加任意脚本，以便在 initqueue 中循环，直到发生某些 dracut 模块需要等待的事情。
- Hook: pre-mount
- Hook: mount
- Hook: pre-pivot
- Hook: cleanup
- Cleanup and switch_root：chroot 到真正的根目录，然后执行真正的 init 程序 `/sbin/init`。

以 `nfs` 模块为例，我们知道 `parse-nfsroot.sh` 在 Hook:cmdline 执行。它将一个操作注册到了 Initqueue finished：

```bash title="dracut/modules.d/95nfs/parse-nfsroot.sh"
echo '[ -e $NEWROOT/proc ]' > "$hookdir"/initqueue/finished/nfsroot.sh
```

意图是通过检查 `/proc` 是否存在来判断 NFS 根目录是否挂载成功。如果在启动过程中遇到这样的报错：

```text
dracut-initqueue[123]: Warning: dracut-initqueue timeout - still waiting for following initqueue hooks:
iniqueue/finished/nfsroot.sh: "[ -e $NEWROOT/proc ]"
```

就可以知道 NFS 根目录挂载失败了。NFS 挂载失败的原因可能是网络问题、NFS 服务器问题等，可以逐一排查。

## ARM 架构

!!! quote

    - [What is the booting process for ARM? - Stack Overflow](https://stackoverflow.com/questions/6139952/what-is-the-booting-process-for-arm)
    - [ELI5: Is there any good reason why ARM systems can't use something like ACPI+UEFI to eliminate the need for device tree (DTB) files and open easier, wider OS compatibility on ARM systems? : r/hardware](https://www.reddit.com/r/hardware/comments/ymh8uu/eli5_is_there_any_good_reason_why_arm_systems/)

与 x86 架构不同，大部分 ARM 架构的硬件设备不支持 ACPI + UEFI，而是使用 Device Tree Blob（DTB）文件来描述硬件设备。虽然目前有支持 UEFI 的工作（见 [It is so disappointing that ARM and RISC-V is adopting UEFI - Hacker News](https://news.ycombinator.com/item?id=39025479)）。
