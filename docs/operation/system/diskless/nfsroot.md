---
tags:
  - 不完善
---

# 核心机制：NFS Root

!!! abstract

    本文讲解以下内容：

    - 如何在一个运行的 Linux 系统上构建其他发行版的根文件系统
    - 如何使用 `systemd-nspawn` 从根文件系统中启动一个虚拟化环境进行配置
    - 如何修改 `initramfs` 以支持 NFSRoot、OverlayFS 等功能

由一个服务器承载并共享的根文件系统，是无盘系统的核心。它包含了操作系统的核心文件，如内核、库、配置文件等。无盘集群中的其他节点通过 NFS Root 挂载该文件系统，实现无盘启动。

## 生成根文件系统：`mmdebstrap`

!!! quote

    - [Debian Wiki: SystemBuildTools](https://wiki.debian.org/SystemBuildTools#bootstrap)
    - [Ubuntu Wiki: Base](https://wiki.ubuntu.com/Base)
    - [Archlinux Wiki: Install Arch Linux from existing Linux](https://wiki.archlinux.org/title/Install_Arch_Linux_from_existing_Linux)
    - [Debian Wiki: Debootstrap](https://wiki.debian.org/Debootstrap)，可以指定版本、架构、源等。

各发行版一般有相应工具为不同版本、不同架构生成根文件系统，用于制作无盘系统、Docker 等。我们将使用这些工具生成根文件系统，在此基础上进行配置。下面以 Debian 为例，使用 `mmdebstrap` 工具生成根文件系统。

!!! info "关于 `debootstrap`"

    `debootstrap` 比 `mmdebstrap` 更常见，Debian Wiki 也上有关于它的详细教程。我们使用的 `mmdebstrap` 与之类似，但使用 `apt` 来解决依赖关系，因此可以使用多个镜像源并解决更复杂的依赖关系。在 [Debian CI/CD 平台](https://jenkins.debian.net/) 上，它被用于生成测试环境，因此我们也选用它。

    不过 `mmdebstrap` 也有一些问题（因为使用了 APT 和系统的 keyring）。比如在 Debian 系统上安装 Ubuntu 就需要预先安装 `ubuntu-keyring`，否则产生如下错误：

    ```text
    I: running apt-get update...
    Get:1 <https://mirrors.zju.edu.cn/ubuntu> oracular InRelease [265 kB]
    Err:1 <https://mirrors.zju.edu.cn/ubuntu> oracular InRelease
    The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 871920D1991BC93C
    Reading package lists...
    W: GPG error: <https://mirrors.zju.edu.cn/ubuntu> oracular InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 871920D1991BC93C
    E: The repository '<https://mirrors.zju.edu.cn/ubuntu> oracular InRelease' is not signed.
    E: apt-get update --error-on=any -oAPT::Status-Fd=<$fd> -oDpkg::Use-Pty=false failed
    ```

    详见 [:simple-github: Missing security updates in images created with debootstrap · Issue #534 · systemd/mkosi](https://github.com/systemd/mkosi/issues/534#issuecomment-709002846)

下面的命令生成一个基本的根文件系统。

```bash
mmdebstrap stable /pxe/rootfs/debian/stable http://mirrors.zju.edu.cn/debian
```

!!! warning "应当重新配置 APT 源"

    在上面命令行中指定的版本会被写入到 APT 源，因此不建议使用 `stable` 等通用版本号，应该指定具体的版本号。而且生成的 APT 源只会包含 `main` 部分，应当重新配置完整的镜像源。

## 进入根文件系统：`systemd-nspawn`

!!! quote

    - [Debian Wiki: systemd-nspawn](https://wiki.debian.org/nspawn)
    - [Pid Eins: systemd for Administrators, Part VI Changing Roots](https://0pointer.net/blog/projects/changing-roots.html)

!!! info "关于 `chroot`"

    - [systemd-nspawn vs chroot and bind mount? - Unix & Linux Stack Exchange](https://unix.stackexchange.com/questions/457815/systemd-nspawn-vs-chroot-and-bind-mount)

    更多教程会通过 `chroot` 进入根文件系统，但这种方式会导致一些问题，如 `systemd` 无法正常启动。进阶的方法是使用 `systemd-nspawn` 从根文件系统启动一个轻量化的容器，与宿主机的环境隔离，这样就能完成 `systemd` 等关键服务的配置。要使用 `systemd-nspawn`，需要在宿主机上安装 `systemd-container` 包。

!!! info "关于 Linux 命名空间"

    - [Namespaces in operation, part 1: namespaces overview [LWN.net]](https://lwn.net/Articles/531114/)
    - [揭秘容器 (一)：内核空间 chroot & namespace - 潘忠显](https://panzhongxian.cn/cn/2023/10/demystifying-containers-part-i-kernel-space/)

    命名空间（Namespace）是 Linux 内核提供的一种机制，用于隔离系统资源。通过命名空间，我们可以在一个进程中创建一个隔离的环境，使得这个进程看到的系统资源是有限的。这项机制为容器虚拟化等技术提供了基础（Docker、LXC 等）。从 2013 年发布的 Linux v3.8 开始，非特权进程可以创建命名空间，在其中拥有完整权限，为 rootless 容器提供了基础。

!!! warning "容器启动时使用的内核与宿主机一致。"

```bash
systemd-nspawn -D /pxe/rootfs/debian/bookworm
passwd
logout
systemd-nspawn -D /pxe/rootfs/debian/bookworm /sbin/init
```

首先在容器内启动一个 shell 配置用户名密码，最后一行命令在容器中运行 `/sbin/init`，以执行完整的启动过程。该命令还有很多参数，可以配置网络、挂载、环境变量等。详见 [FreeDesktop: systemd-nspawn](https://www.freedesktop.org/software/systemd/man/systemd-nspawn.html)。

接下来安装内核、一些基础的包，并配置软件源等：

```bash
apt install ca-certificates vim
# 配置软件源
apt update && apt upgrade
apt install linux-image-amd64
```

注意记录此次安装的内核版本，后续需要生成 initramfs 时会用到。

```bash
apt list --installed | grep linux
```

以 `linux-image-6.1.0-21-amd64` 为例，则内核版本为 `6.1.0-21-amd64`。

### 解决 DNS 问题

[Archlinux Wiki](https://wiki.archlinux.org/title/Systemd-nspawn#Domain_name_resolution) 上对 DNS 作了一些归纳。如果宿主机运行 `systemd-resolved`，则容器中的 `/etc/resolv.conf` 会通过复制或 bind-mount 的方式与宿主机保持一致。

然而在 nspanw 到 Ubuntu 时，常常遇到 DNS 无法解析的问题：

```text
W: Failed to fetch https://mirrors.zju.edu.cn/ubuntu/dists/oracular/InRelease  Temporary failure resolving 'mirrors.zju.edu.cn'
```

在脚本中使用 `>/etc/resolv.conf` 写入文件，却发现找不到文件：

```text
/root/20241114T000408CST.sh: line 92: /etc/resolv.conf: No such file or directory
```

这一错误十分有误导性。Ubuntu 中 `/etc/resolv.conf` 是一个符号链接，指向 `/run/systemd/resolve/stub-resolv.conf`，而链接的对象不存在。Debian 中则是一个文件。

[:simple-github: [systemd-nspawn] resolv-conf-setup fails with resolved guest in stub-mode](https://github.com/systemd/systemd/issues/15340) 解释了 DNS 失败的原因：

> So if `/etc/resolv.conf` exists as symlink, nspawn assumes the thing is managed by something smart (such as resolved inside the container) and doesn't want to break things and hence doesn't replace the thing.
> I am a bit conservative in wanting to change this behaviour. i.e. if we just blindly replace it with a regular file and then you next boot up the image in qemu or on a physical host, then resolved will be borked for good. Hence, for the automatic, implicit behaviour I think we should only replace the thing when it is a regular file (because that just means staying within the same type of setup, just with fresher data) and not when it is a symlink (because that would mean changing the type of setup).
>
> Hence I think I'll add a new mode --resolv-conf=replace-stub which is like copy-stub but replaces whatever exists regardless what it is.

然而使用 `--resolv-conf=replace-stub` 也会产生错误：

```text
Failed to copy /etc/resolv.conf to /pxe/rootfs/ubuntu/oracular.error/etc/resolv.conf, ignoring: No such file or directory
```

这是因为在 Debian 12 及以上，`systemd-resolved` 默认不安装（见 [Debiab bookworm Release Notes](https://www.debian.org/releases/bookworm/amd64/release-notes/ch-information.en.html#systemd-resolved)。安装 `systemd-resolved` 即可使用 `--resolv-conf=replace-stub` 解决 DNS 问题。

## 生成 initramfs：[:simple-github: dracut-ng/dracut-ng](https://github.com/dracut-ng/dracut-ng)

!!! quote

    - [GitHub: dracut User Manual](https://github.com/dracutdevs/dracut/blob/master/man/dracut.usage.asc)
    - [Spinics: rootnfs + rootovl (diskless client shutdown problem)](https://www.spinics.net/lists/systemd-devel/msg03202.html)

我们使用 `dracut` 工具生成 initramfs。与 Debian 默认使用的 `initramfs-tools` 相比，它可以通过模块方便地支持 OverlayFS 等功能，符合我们的需求。

简单来说，dracut-ng 是一个事件驱动的 initramfs。它认为我们挂载 rootfs 的过程本质上依赖于硬件的可用性，应当基于 udev 事件而不是硬编码的脚本来执行任务。这使得 dracut-ng 更加灵活，可以适应各种硬件环境。

dracut 能够选择向 initramfs 中添加/删除 module 以实现不同的功能。module 添加后不一定就会被执行，可以通过内核启动参数来控制。这也就意味着可以通过内核启动参数更改根文件系统等，而不需要重新生成 initramfs。

如[启动过程](../basic/boot.md)中所述，引导程序会加载 initramfs 到内存中作为根文件系统，启动其中的 `/sbin/init` 进行初始化，再切换到真正的根文件系统。

!!! warning "`dracut` 默认使用当前活跃的内核。如果按上文 chroot 方式启动，则可能活跃的内核与安装的内核不一致，出现 `dracut: Cannot find module directory` 错误。此时应当使用 `--kver` 参数指定内核版本。"

```bash
apt install network-manager
# dracut-network 模块依赖于 network-manager
# 若没有安装，则可能出现 dracut: dracut module 'nfs' depends on 'network', which can't be installed 等错误
# 导致 dpkg 持续失败
# 参考 https://github.com/dracutdevs/dracut/issues/1756
apt install dracut dracut-network
KERNEL_VERSION='6.1.0-21-amd64'
dracut --list-modules --kver $KERNEL_VERSION
```

可以选择在配置文件中添加需要的模块：

```text title="/etc/dracut.conf.d"
# rootovl.conf
filesystems+=" overlay "
# 11-ifcfg.conf，这个文件可能已经存在
add_dracutmodules+=" ifcfg "
```

也可以在命令行中指定/添加：

```bash
# 仅指定
dracut -m "nfs network base overlayfs" --kver $KERNEL_VERSION --force
# 默认+添加
dracut --add overlayfs --kver $KERNEL_VERSION --force
```

关于 `dracut` 的内核参数，可以查看 [`man dracut.cmdline`](https://man7.org/linux/man-pages/man7/dracut.cmdline.7.html)。

## 分享根文件系统：NFS

完成根文件系统的创建后，应当配置 NFS 服务，以便其他节点可以挂载该文件系统。见 [磁盘和文件系统#NFS](../basic/filesystem.md#nfs)。
