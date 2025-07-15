---
tags:
  - stable
---

# 网络运维

<figure markdown="span">
    <center>
    ![network](index.assets/network.png){ width=50% align=center}
    </center>
</figure>

在笔者看来，网络运维之所以被称为玄学，主要有两个原因：

- 网络通信领域知识和技术繁杂，涉及的领域广泛。能泛泛地了解各种技术已经很不错，更别提深入掌握了。

    ??? example "例子：TCP 协议"

        下面这段介绍来自《TCP/IP 详解：卷 1》 ，可以看到除了最原始的一份规范文件外，还有非常多与实践相关的补充定义。仅一个 TCP 协议，就需要十多份 RFC 来定义，可以看出网络通信技术的复杂性。

        > The original specification for TCP is [RFC0793], although some errors in that RFC are corrected in the Host Requirements RFC, [RFC1122]. Since then, specifications for TCP have been revised and extended to include clarified and improved congestion control behavior [RFC5681][RFC3782][RFC3517][RFC3390][RFC3168], retransmission timeouts [RFC6298][RFC5682][RFC4015], operation with NATs [RFC5382], acknowledgment behavior [RFC2883], security [RFC6056][RFC5927][RFC5926], connection management [RFC5482], and urgent mechanism implementation guidelines [RFC6093]. There have also been a rich variety of experimental modifications covering retransmission behaviors [RFC5827][RFC3708], congestion detection and control [RFC5690][RFC5562][RFC4782][RFC3649][RFC2861], and other features. Finally, there is an effort to explore how TCP might take advantage of multiple simultaneous network-layer paths [RFC6182].

- 具体的实现和网络设备、协议、技术等相关，都是由厂商提供的，不同厂商的设备、协议、技术等都有所不同。除了基本的原理和概念，很多东西都是具体问题具体分析。

    ??? example "例子：网络设备的操作系统"

        - 华为、思科、华三等传统 ICT 厂商广泛采用命令行界面，形成了一套固定的思路。对于这些厂商的设备，只能硬着头皮学习命令行操作，使用 Web 管理只会踩坑。
        - Mikrotik 等新兴厂商的系统又是另一套思路。他们将更多的细节提供到图形界面中，一定程序上降低了学习成本，同时提供了高度的可定制性。
        - TP-Link 等厂商的产品面向家庭用户，更多的是提供简单易用的界面。对于网络运维人员来说，这些设备的功能和可自定义程度都是不够的。

    ??? example "例子：黑洞问题"

        RFC 2923 - TCP Problems with Path MTU Discovery 提及了 MTU 发现技术因为配置不当可能产生的黑洞问题。**这个问题在我们的运维过程中真实地发生了（参见 [网络技术专题/L2TP#MTU 调优](../network-technology/l2tp.md#l2tp-mtu-调优)**。RFC 2923 对该问题的评价是“非常难以调试”：

        > This failure is especially difficult to debug, as pings and some interactive TCP connections to the destination host work.  Bulk transfers fail with the first large packet and the connection eventually times out.
        >
        > This problem has been discussed extensively on the tcp-impl mailing list;  the name "black hole" has been in use for many years.

        简单来说，主机通过设置“禁止分片”标志位并发送尽可能大的数据包来执行路径 MTU 发现。如果数据包过大，路由器会返回“目标不可达 - 需要分片”的 ICMP 消息，主机根据该消息调整数据包大小。然而，由于路由器可能存在内核漏洞或配置问题，ICMP 消息可能无法正确发送，尤其是防火墙可能会阻止这些消息。这样会导致路径 MTU 发现失败，主机无法得知需要减小数据包大小，导致数据包在网络中丢失，形成“PMTUD 黑洞”。原文如下：

        > A host performs Path MTU Discovery by sending out as large a packet as possible, with the Don't Fragment (DF) bit set in the IP header.  If the packet is too large for a router to forward on to a particular link, the router must send an ICMP Destination Unreachable -- Fragmentation Needed message to the source address. The host then adjusts the packet size based on the ICMP message.
        >
        > As was pointed out in [RFC1435], routers don't always do this correctly -- many routers fail to send the ICMP messages, for a variety of reasons ranging from kernel bugs to configuration problems.  Firewalls are often misconfigured to suppress all ICMP messages.  IPsec [RFC2401] and IP-in-IP [RFC2003] tunnels shouldn't cause these sorts of problems, if the implementations follow the advice in the appropriate documents.
        >
        > PMTUD, as documented in [RFC1191], fails when the appropriate ICMP messages are not received by the originating host.  The upper- layer protocol continues to try to send large packets and, without the ICMP messages, never discovers that it needs to reduce the size of those packets.  Its packets are disappearing into a PMTUD black hole.

!!! tip "学习建议"

    避免 CSDN 等内容质量较低的网站，尽量阅读优质文档和书籍，为自己搭起一个完善的知识框架。知识框架完成后，可以进一步阅读文档和博客等，以填充细节。

    推荐阅读的书籍：

    | 中文名 | 英文名 |
    | --- | --- |
    | TCP/IP 详解 | TCP/IP Illustrated |
    | 计算机网络：自顶向下方法 | Computer Networking: A Top-Down Approach |

    这些书籍大多描述非常基础的网络技术，对于理解网络的基本原理非常有帮助。但运维工作中，基础知识并不常用，更多是应用相关。对于网络技术的应用，推荐阅读思科、华为、新华三等 ICT 厂商的介绍文档。
