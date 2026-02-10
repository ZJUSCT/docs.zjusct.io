---
tags:
  - 不完善
---

# Linux 设备驱动

## udev

### 重载 udev rules

!!! quote

    - [udevadm - freedesktop](https://www.freedesktop.org/software/systemd/man/latest/udevadm.html)
    - [kernel - How to reload udev rules without reboot? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/39370/how-to-reload-udev-rules-without-reboot)

构建无盘系统时，部分驱动（如 DOCA）可能在 `.postinst` 脚本中重载 udev rules：

```bash title="rdma-core.postinst"
if [ "$1" = "configure" ]; then
    # we ship udev rules, so trigger an update. This has to be done after
    # DEBHELPER restarts systemd to get our new service files loaded.
    udevadm trigger --subsystem-match=infiniband --action=change || true
    udevadm trigger --subsystem-match=net --action=change || true
    udevadm trigger --subsystem-match=infiniband_mad --action=change || true
fi
```

但是由于无盘系统构建处于 `systemd-nspawn` 环境，`uevent` 文件只读：

```text
Setting up rdma-core (2410mlnx54-1.2410068) ...
[0;1;31mibp1s0: Failed to write 'change' to '/sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0/infiniband/ibp1s0/uevent': Read-only file system[0m

[0;1;31mibs10: Failed to write 'change' to '/sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0/net/ibs10/uevent': Read-only file system[0m

[0;1;31missm2: Failed to write 'change' to '/sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0/infiniband_mad/issm2/uevent': Read-only file system[0m
```

!!! question

    为什么 `uevent` 文件只读，是因为容器内 `systemd-udevd` 服务没启动吗？如果使用 `init` 启动完整容器，是否仍会存在问题？

在构建过程中这一错误并不重要，只是相当于插拔了一次设备，不影响 udev rules 应用到后续的物理机启动。

## NVIDIA GPU

!!! quote

    - [NVIDIA Transitions Fully Towards Open-Source GPU Kernel Modules - NVIDIA Technical Blog](https://developer.nvidia.com/blog/nvidia-transitions-fully-towards-open-source-gpu-kernel-modules/)

目前，NVIDIA 已经全面转向开源 GPU 内核模块，这对于我们的集群运维来说是一个好消息。NVIDIA 建议从 Turing 架构开始使用开源驱动，我们的最低显卡 2080Ti 正是 Turing 架构，因此我们可以放心地迁移到开源驱动。使用包管理器安装 `cuda` 时，会自动安装相关联版本的驱动。**CUDA 12.5 及以前为闭源驱动，CUDA 12.6 及以后为开源驱动。**
