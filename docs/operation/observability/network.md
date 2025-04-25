---
tags:
  - 完善
---

# 网络观测

!!! quote

    - [Network Traffic Monitoring in 2024: Discover the Top 7 Solutions](https://www.auvik.com/franklyit/blog/best-network-traffic-monitor/)
    - 华为文档

## 网络流分析（Network Flow Analysis）

!!! quote

    - [Network Flow Monitoring Explained: NetFlow vs sFlow vs IPFIX](https://www.varonis.com/blog/flow-monitoring)：对 NetFlow, sFlow, IPFIX 三种流量监控协议的介绍。
    - [配置 IPv4 原始流统计信息的输出示例 - NetEngine AR600, AR6100, AR6200, AR6300 V300R024 配置指南 - 网络管理与监控（命令行） - 华为](https://support.huawei.com/enterprise/zh/doc/EDOC1100411131/b7771e97)

四种协议的关系：

- **NetFlow**：Cisco 开发的流量监控协议。相关衍生协议一般兼容：
    - **NetStream**：Huawei 基于 NetFlow v9 开发的流量监控协议。
- **sFlow**：sampled flow，与 NetFlow 不兼容。
- **IPFIX**：由 IETF 从 NetFlow v9 标准化而来。

下文将以 NetStream 为例进行介绍。

### NetStream 基本原理

三部分：

- 网络流数据输出器 NDE（NetStream Data Exporter）：配置了 NetStream 功能的设备在 NetStream 系统中担当 NDE 角色。
- 网络流数据收集器 NSC（NetStream Collector）：运行于 Unix 或者 Windows 上的一个应用程序，负责解析来自 NDE 的报文。
- 网络流数据分析器 NDA（NetStream Data Analyzer）：从 NSC 中提取统计数据，进行进一步的加工处理后生成报表。

当流量进入 NDE 后，经历下列过程：

- 设备的 NetStream 模块按一定的采样方式进行 **NetStream 采样**：随机/固定报文间隔采样、随机/固定时间间隔采样
- 对采样数据建立 **NetStream 流**：NetStream 是一项基于“流”来提供报文统计的技术，NetStream 流就是 IP 报文（UDP、TCP、ICMP 报文）。对于 IPv4 报文，IPv4 NetStream 会根据 IPv4 报文的**目的 IP 地址、源 IP 地址、目的端口号、源端口号、协议号、服务类型 ToS（Type of Service）、输入接口或输出接口**来定义流，相同的七元组标识为同一条流。
- 按一定的老化方式对流进行 **NetStream 流老化**处理：
    - 按时老化：活跃流 30 分钟，非活跃流 30 秒
    - 由 TCP 连接的 FIN 和 RST 报文触发老化
    - 统计字节超过限制时老化：硬件的字节计数器是 32 比特，最大计数值为 4294967295，约为 3.9G 字节
    - 强制老化
- 按一定的输出方式以及相应的版本进行 **NetStream 流输出**：
    - **原始流输出**是指所有流的统计信息都要被统计。在流老化时间超时后，每条流的统计信息都要输出到 NetStream 服务器。
    - **聚合流输出**是指采用聚合流输出功能后，设备对与聚合关键项完全相同的流统计信息进行汇总，从而得到对应的聚合流统计信息，并且将该聚合统计信息发送到相应的接收聚合统计信息的 NetStream 服务器。例如：协议 - 端口聚合、目的前缀聚合。
    - 对于**灵活流输出**，其流的建立条件是按照自定义的条件设置。

以 OpenTelemetry NetFlow Receiver 为例，NetFlow v9 格式输出到 ClickHouse 中的条目如下：

```text
Timestamp:          2025-03-25 04:25:44.920000000
TimestampTime:      2025-03-25 04:25:44
TraceId:
SpanId:
TraceFlags:         0
SeverityText:
SeverityNumber:     0
ServiceName:
Body:
ResourceSchemaUrl:
ResourceAttributes: {'cloud.region':'zjusct-cluster'}
ScopeSchemaUrl:
ScopeName:          otelcol/netflowreceiver
ScopeVersion:
ScopeAttributes:    {'receiver':'netflow'}
LogAttributes:      {'destination.address':'10.78.18.247','destination.port':'11349','flow.end':'1742876744920000000','flow.io.bytes':'377','flow.io.packets':'1','flow.sampler_address':'172.25.3.254','flow.sampling_rate':'0','flow.sequence_num':'1','flow.start':'1742876744920000000','flow.time_received':'1742876776236499353','flow.type':'netflow_v9','network.transport':'udp','network.type':'ipv4','source.address':'210.32.148.87','source.port':'29915'}
```

!!! warning "选择更短的老化时间"

    NetStream 稍显不足的地方在于：无法实时监控流量。只有当流老化时，才会将流量数据发送到 NetStream 服务器，根据该结果只能得到平均速率。如果对实时性要求较高，可以选择更短的老化时间。然而系统对最短老化时间有限制，在 AR6121 上，活跃流最小老化时间 1 分钟，非活跃流最小老化时间 1 秒。

### NetStream 配置

目前 OpenTelemetry NetFlow Receiver 暂时只支持华为路由器中原始流统计信息的输出，使用协议 - 端口聚合等聚合输出会导致 IP 地址字段无法识别等问题。

在需要监控的接口上使能统计。默认固定报文间隔采样（1:100），我们选择全量采样：

```text
[Router] interface gigabitethernet 1/0/0
[Router-GigabitEthernet1/0/0] ip netstream sampler fix-packets 1 inbound
[Router-GigabitEthernet1/0/0] ip netstream sampler fix-packets 1 outbound
[Router-GigabitEthernet1/0/0] ip netstream inbound
[Router-GigabitEthernet1/0/0] ip netstream outbound
```

在全局视图下使能原始流统计信息的输出：

```shell
[Router] ip netstream tcp-flag enable
[Router] ip netstream export version 9
# 配置完下面两行即可在 OpenTelemetry NetFlow Receiver 中查看到流量数据
[Router] ip netstream export source 10.1.2.1
[Router] ip netstream export host 10.1.2.2 6000
```
