# 其他发行版

!!! abstract

    我们日常使用的发行版为 Debian，但在一些特殊场景下，可能需要使用其他发行版。本文记录不同发行版的安装和使用经验。

!!! tip

    笔者认为，对一个发行版，只要看它的**包管理器**和**`init`**系统就够了，其他东西都是次要的。比如 OpenEuler,它的包管理器为 `rpm`，`init` 系统为 `systemd`，那么使用上就和 RHEL 系列差不多。

    关于包管理器，Arch Wiki 上有一篇很好的对比总结：[pacman/Rosetta - ArchWiki](https://wiki.archlinux.org/title/Pacman/Rosetta)。

!!! warning

    从 2024 年开始，学校信息中心要求各单位禁止使用 RHEL 系列的发行版，包括 fedora、centos、rocky 等。因此，我们不再建议使用这些发行版。

## OpenEuler 欧拉

### OpenEuler 安装

#### 使用 `dnf` 进行 chroot 安装

!!! quote

    - [Root on NFS: Installing system using dnf --installroot - Fedora Discussion](https://discussion.fedoraproject.org/t/root-on-nfs-installing-system-using-dnf-installroot/132194)
    - [Create Fedora rootfs to chroot in with dnf - gist](https://gist.github.com/gotha/5af164ac790bf5e42af5edd45f7b04b3)

!!! error

    很遗憾，OpenEuler 现在不建议使用 `dnf` 进行 chroot 安装。

    OpenEuler 自己的 `dnf` 使用 ndb，与新版 `dnf` 使用 sqlite 不同。因此使用新版 `dnf` 进行 chroot 安装后，OpenEuler 的 `dnf` 读取不到任何安装的软件。需要进去重新使用 `dnf` 安装各类软件，造成文件覆写，并不优雅。

    在 [rpm后端数据库为何选择ndb而不是sqlite · Issue #I5MAW5 · src-openEuler/rpm - Gitee.com](https://gitee.com/src-openeuler/rpm/issues/I5MAW5) 中，OpenEuler 开发者表示 OpenEuler 的 `dnf` 将坚持使用落后的 ndb，希望实现软件依赖自闭环。这一态度不好评价。

    该方法仍然适用于其他基于 `dnf` 的发行版，比如 Fedora、RockyLinux 等。

以宿主机为 Debian 为例，安装 `dnf` 和 `rpm` 包，在宿主机配置好 openEuler 源：

```text title="/etc/yum.repos.d/openEuler.repo"
[openEuler]
name=openEuler-$releasever-OS
baseurl=https://mirrors.zju.edu.cn/openeuler/openEuler-$releasever/OS/$basearch/
enabled=1
gpgcheck=1
gpgkey=https://mirrors.zju.edu.cn/openeuler/openEuler-$releasever/OS/$basearch/RPM-GPG-KEY-openEuler
```

然后使用 `dnf` 安装到指定目录。需要注意，应当提前挂载 `/proc` 等目录，否则安装过程中会提示 `/proc` 缺失等。此外，rpm 软件包似乎可以意识到自己处于 chroot 环境，从而跳过启动步骤。

```bash
dnf --installroot="$CHROOT_TARGET" \
    --repo=openEuler \
    --releasever="$RELEASE" \
    -y groupinstall core
```

#### 从安装镜像中提取最小系统

!!! warning "deprecated"

    在 Debian 系统上有 dnf 包，建议使用 dnf 安装方式。本方式留作备份。

除去杂七杂八的镜像，在 x86_64 架构下，OpenEuler 提供三种镜像：

- `netinst`：网络安装镜像，只包含最基本的系统。

    ```text
    .
    ├── docs
    │   ├── OpenEuler-Software-License.docx
    │   └── TRANS.TBL
    ├── EFI
    │   ├── BOOT
    │   │   ├── BOOTX64.EFI
    │   │   ├── fonts
    │   │   │   ├── TRANS.TBL
    │   │   │   └── unicode.pf2
    │   │   ├── grub.cfg
    │   │   ├── grubx64.efi
    │   │   ├── mmx64.efi
    │   │   └── TRANS.TBL
    │   └── TRANS.TBL
    ├── images
    │   ├── efiboot.img
    │   ├── install.img
    │   ├── pxeboot
    │   │   ├── initrd.img
    │   │   ├── TRANS.TBL
    │   │   └── vmlinuz
    │   └── TRANS.TBL
    ├── isolinux
    │   ├── boot.cat
    │   ├── boot.msg
    │   ├── grub.conf
    │   ├── initrd.img
    │   ├── isolinux.bin
    │   ├── isolinux.cfg
    │   ├── ldlinux.c32
    │   ├── libcom32.c32
    │   ├── libutil.c32
    │   ├── splash.png
    │   ├── TRANS.TBL
    │   ├── vesamenu.c32
    │   └── vmlinuz
    ├── ks
    │   ├── ks.cfg
    │   └── TRANS.TBL
    └── TRANS.TBL

    9 directories, 32 files
    ```

- 正常安装镜像：包含一些基础软件包。

    与 `netinst` 相比，多出了 `Packages` 和 `repodata` 目录，包含软件包和元数据。

    ```text
    ├── Packages
    │   ├── *.rpm
    ├── repodata
    │   ├── *.xml.zst
    │   ├── normal.xml
    │   ├── repomd.xml
    │   └── TRANS.TBL
    ├── RPM-GPG-KEY-openEuler
    ```

- `everything`：在 `Packages` 目录中包含了所有软件包，体积庞大。在 24.09 版本大小为 23.7 GB。

现在我们希望从安装镜像中找到最小系统，以便能够通过 `chroot` 进行配置。

挂载 `netinst` 版本的 `iso` 镜像，查看其中的文件：

```bash
mkdir -p /mnt/openEuler
mount -o loop openEuler-24.09-x86_64-netinst.iso /mnt/openEuler
```

- `EFI` 和 `isolinux` 显然是为了 ISO 启动引导使用的（类似于 pxelinux）
- 而真正引导进入的镜像位于 `images` 目录下
    - `pxeboot` 目录下的 `vmlinuz` 和 `initrd.img` 为 PXE 引导使用的简单内核和初始内存盘，后者先后使用 `xz` 和 `cpio` 解压后可以看到简单的根文件系统
    - `efiboot.img` 里的内容和 `EFI` 差不多，不知道是不是为了方便刷写引导到 U 盘等设备所以提供了这个镜像
    - `install.img` 是一个 `squashfs` 镜像，挂载后内容如下，提示我们 `rootfs.img` 是一个可以运行的 LiveOS 的根文件系统

        ```text
        .
        └── LiveOS
            └── rootfs.img
        ```

        `rootfs.img` 是一个 ext4 文件系统，将其解压出来就能获得我们所需的最小系统。

`install.img` 又可以直接从镜像源获取，于是获取根文件系统的过程非常简单：

```bash
MIRROR='https://mirrors.zju.edu.cn/openeuler/'
VERSION='24.09'
RELEASE="openEuler-$VERSION/"
FILEPATH='OS/x86_64/images/install.img'

CHROOT_BASE=/pxe/rootfs/openeuler
ROOTIMGPATH='LiveOS/rootfs.img'

TMPDIR=/tmp/openeuler-$TIMESTAMP
mkdir -p "$TMPDIR"
IMGFILE=$TMPDIR/install.img

wget -O "$IMGFILE" $MIRROR$RELEASE$FILEPATH
unsquashfs -d "$TMPDIR" "$IMGFILE" $ROOTIMGPATH
mkdir -p "$CHROOT_TARGET"
7z x -snld "$TMPDIR/$ROOTIMGPATH" -o"$CHROOT_TARGET"
```

!!! tip

    `7zip` 是一个非常好用的工具，可以直接解压 Ext4 和 Squashfs 等文件系统的 `.img`、ISO 文件等。

### OpenEuler 配置与管理

阅读官方文档：[openEuler 社区官网](https://docs.openeuler.org/zh/)。

- 有 DNF 和 YUM 两个包管理器，前者是后者的升级版，推荐使用 DNF。

## OpenAnolis 龙蜥
