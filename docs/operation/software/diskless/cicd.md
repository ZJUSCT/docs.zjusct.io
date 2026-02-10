---
tags:
  - 不完善
---

# 自动构建：Jenkins

!!! abstract

    在 [NFS Root](nfsroot.md) 的基础上，我们使用 Jenkins 进行无盘系统的自动化构建。

    Jenkins 运维见 [集群服务/Jenkins](../service/jenkins.md)，本文不再赘述 Jenkins 的安装和配置。

## 为什么需要 CI/CD？

在使用 CI/CD 前，运维人员手动进入根文件系统进行操作，没有完善的记录和版本控制。随着时间积累，运维人员也逐渐遗忘操作流程，各类配置往往难以复现和迁移。而 CI/CD 可以：

- 节省人力成本：只需要修改脚本，由 CI/CD 自动检测、构建、测试、部署。
- 完善的记录和版本控制，结果可复现。
- 方便迁移和升级：CI/CD 平台可以在各种环境中部署。

CI/CD 配置文件见 [:simple-gitlab: zjusct/ops/conf-diskless](https://git.zju.edu.cn/zjusct/ops/conf-diskless)。

## 源码分析：`jenkins.debian.net`

Debian 的质量管理（Quality Assurance, QA）团队使用 Jenkins 在 [`jenkins.debian.net`](https://jenkins.debian.net/) 上进行系统构建测试，其中包括基于 `chroot` 的测试。相关配置文件见 [:simple-gitlab: qa/jenkins.debian.net](https://salsa.debian.org/qa/jenkins.debian.net)。

核心文件为 [`bin/chroot-installation.sh`](https://salsa.debian.org/qa/jenkins.debian.net/-/blob/master/bin/chroot-installation.sh)。

开头的 `common-init` 非常有意思：将脚本自身拷贝为一个临时文件然后执行。这样做在生产环境中可以避免脚本在执行过程中被修改导致失败。

```bash title="common-functions.sh"
common_init(){
#...
if [ "${0:0:5}" != "/tmp/" ] ; then
#...
    # mktemp some place for us...
    TTT="$(mktemp --tmpdir=/tmp jenkins-script-XXXXXXXX)"
    if [ -z "$TTT" ] ; then
        echo "Failed to create tmpfile, aborting. (Probably due to read-only filesystem…)"
        exit 1
    fi
    # prepare cleanup
    trap common_cleanup INT TERM EXIT
    # cp $0 to /tmp and run it from there
    cp $0 $TTT
    chmod +x $TTT
#...
fi
```

下面这段代码做 `chroot` 前的准备：

```bash title="chroot-installation.sh"
bootstrap() {
    echo "Bootstraping $1 into $CHROOT_TARGET now."
    set -x
    sudo mmdebstrap $1 $CHROOT_TARGET $MIRROR
    set +x
    prepare_bootstrap $1
    execute_ctmpfile
}
```

> mmdebstrap: In contrast to debootstrap it **uses apt to resolve dependencies** and is thus able to use more than one mirror and resolve more complex dependency relationships.

`prepare_bootstrap` 将一些配置写入 `chroot` 后使用的临时文件：

```bash title="chroot-installation.sh"
prepare_bootstrap() {
    # 将 EOF 中的内容写入到 $CTMPFILE 临时文件，用于系统配置初始化
    cat >> $CTMPFILE <<-EOF
    # 加入脚本头部内容（即 #!/bin/bash）
    $SCRIPT_HEADER
    set -x
    # 挂载 /proc 文件系统，提供进程和内核信息访问
    mount /proc -t proc /proc
    # 创建 policy-rc.d 文件，以防止服务在安装时自动启动
    # 文件内容设置为简单的 shell 脚本，直接退出并返回 101 状态码
    echo -e '#!/bin/sh\nexit 101' > /usr/sbin/policy-rc.d
    chmod +x /usr/sbin/policy-rc.d
    # 设置 apt 代理服务器地址
    echo 'Acquire::http::Proxy "http://ionos14-amd64.debian.net:3128";' > /etc/apt/apt.conf.d/80proxy
    # 配置 apt 调试信息输出，用于依赖解析和安装过程的调试
    cat > /etc/apt/apt.conf.d/80debug << APTEOF
    # solution calculation
    Debug::pkgDepCache::Marker "true";
    Debug::pkgDepCache::AutoInstall "true";
    Debug::pkgProblemResolver "true";
    # installation order
    Debug::pkgPackageManager "true";
    APTEOF
    # 添加源代码仓库，指定版本为传入参数 $1 的发行版版本
    echo "deb-src $MIRROR $1 main" > /etc/apt/sources.list.d/$1-src.list
    apt-get update
    # 预配置 man-db 包的 auto-update 选项为 false，防止安装时自动更新手册页
    echo "man-db man-db/auto-update boolean false" | debconf-set-selections
    # 启用 dpkg 的 unsafe-io 模式（允许并发 I/O 操作），提高安装速度
    mkdir -p /etc/dpkg/dpkg.cfg.d
    echo force-unsafe-io > /etc/dpkg/dpkg.cfg.d/02dpkg-unsafe-io
    set +x
EOF
}
```

`execute_ctmpfile` 的内容就比较简单了。核心是其中的 `sudo chroot` 命令，将 `$TMPFILE` 脚本在 `chroot` 环境中执行：

```bash title="chroot-installation.sh"
execute_ctmpfile() {
    echo "echo xxxxxSUCCESSxxxxx" >> $CTMPFILE
    set -x
    chmod +x $CTMPFILE
    set -o pipefail        # see eg http://petereisentraut.blogspot.com/2010/11/pipefail.html
    (sudo chroot $CHROOT_TARGET $TMPFILE 2>&1 | tee $TMPLOG) || true
    RESULT=$(grep "xxxxxSUCCESSxxxxx" $TMPLOG || true)
    if [ -z "$RESULT" ] ; then
        RESULT=$(grep -E "Failed to fetch.*(Unable to connect to|Connection failed|Size mismatch|Cannot initiate the connection to|Bad Gateway|Service Unavailable|Hash Sum mismatch)" "$TMPLOG" || true)
        if [ -n "$RESULT" ] ; then
            echo
            echo "$(date -u) - Warning: Network problem detected."
            echo "$(date -u) - trying to workaround temporarily failure fetching packages, sleeping 5min before trying again..."
            sleep 5m
            echo
            sudo chroot $CHROOT_TARGET $TMPFILE
        else
            echo "Failed to run $TMPFILE in $CHROOT_TARGET."
            exit 1
        fi
    fi
    rm $CTMPFILE
    set +o pipefail
    set +x
}
```

## 自动构建根文件系统

我们修改 `jenkins.debian.net` 的配置，进行简化，适配我们的集群。

- `common-functions.sh` 和 `chroot-installation.sh` 两个文件保持原有的基本结构，方便同学们比较学习。
- 由于 Jenkins 可以保证构建过程中脚本文件不被修改，因此去掉 `common_init` 中的自拷贝操作。
- 将 `chroot-installation.sh` 中的功能模块拆分到 `modules` 下的脚本，而不是直接写在 `chroot-installation.sh` 中。
- 扩展 `prepare_bootstrap` 为 `prepare_module`，用于加载模块。
- `execute_ctmpfile` 从 `chroot` 修改为 `systemd-nspawn`，提供更好更方便的虚拟化和隔离性。

此外有一些约定：

- `modules-headers.sh` 提供了各个模块常用的工具：
    - 使用 `alias`，为 `apt-get`、`curl`、`wget` 等常用工具设置自动确认、自动重试、抑制输出等选项。
    - 包装了从 URL 和 GitHub 安装软件包的函数。
    - 常用环境变量提取。

### 发布命名规则

`chroot-installation.sh` 的 `cleanup_all()` 负责构建过程最后的文件移动操作。最开始构建的根文件系统使用 `$RELEASE.$TIMESTAMP` 命名。根据构建情况，将被移动到：

- `$RELEASE.error`：构建失败，用以排查问题。
- `$RELEASE.latest`：构建成功，用于测试。
- `$RELEASE`：测试通过，用于生产。

这些目录都会覆盖，因此不会有历史构建的残留。但如果在 Jenkins 中 Abort 任务（比如因为命令行交互而阻塞构建过程），则会残留 `$RELEASE.$TIMESTAMP` 目录。

### 内核版本发现

在 `systemd-nspawn` 环境中，内核仍然是宿主机的内核，因此无法通过 `uname -r` 等命令获取到目标系统安装的内核。我们尝试了一些方案：

- 查询 `/lib/modules` 目录，其中可能有非内核版本名称的目录，比如 Ubuntu 中有 `kenrel` 目录，需要过滤。

    ```bash
    KERNEL_VERSION=$(ls -1 /lib/modules | sort -V | grep '[0-9]' | tail -n 1)
    ```

    但是**这个目录可能不存在**。

- 使用 `dpkg` 查询安装的内核版本，通常为 `linux-image-` 开头的包。

    ```bash
    KERNEL_VERSION=$(dpkg --list | grep linux-image | awk '{print $2}' \
        | grep -oP '\d+\.\d+\.\d+-\d+-amd64' | sort -V | tail -n 1)
    ```

    但是 **`linux-image-` 也可能不存在**。比如在 Debian sid 中，`dracut` 与 `initramfs-tools` 冲突，而 `linux-image` 依赖 `initramfs-tools`，导致被卸载：

    ```text
    Unpacking dracut-core (103-2) ...
    dpkg: initramfs-tools: dependency problems, but removing anyway as you requested:
     linux-image-6.11.7-amd64 depends on initramfs-tools (>= 0.120+deb8u2) | linux-initramfs-tool; however:
      Package initramfs-tools is to be removed.
      Package linux-initramfs-tool is not installed.
      Package initramfs-tools which provides linux-initramfs-tool is to be removed.
    ```

- 目前我们采取了一个并不完美的方法。因为只有 `dracut` 需要指定内核版本，而它安装时会在 `/boot` 下生成携带内核版本名的文件，我们可以从其中提取：

    ```bash
    KERNEL_VERSION=$(for file in /boot/vmlinuz-*; do echo "${file#/boot/vmlinuz-}"; done | sort -V | tail -n 1)
    ```

### 发行版本发现

使用 Systemd 管理的系统都会提供 `/etc/os-release` 文件，其中包含了系统的发行版本信息。我们可以从中提取：

```bash
. /etc/os-release
```

其中最常用的是 `ID`（系统名称，如 `debian`、`ubuntu`）、`VERSION_CODENAME`（发行版本代号，如 `bullseye`、`focal`）。

需要注意的是，Debian sid 与 testing 的 `VERSION_CODENAME` 一致，需要借助 `PRETTY_NAME` 进行区分。

```bash
case $ID in
debian)
    # sid 的 VERSION_CODENAME 和 testing 相同，需要特殊处理
    if echo "$PRETTY_NAME" | grep -q sid; then
        VERSION_CODENAME=sid
    fi
    ;;
ubuntu)
    ;;
*)
    echo "OS not supported"
    exit 1
    ;;
esac
```

### 架构发现

`dpkg` 提供了 `dpkg --print-architecture` 命令，可以获取当前系统的架构。

不过众所周知，架构的名称非常多样，比如 `amd64`、`x86_64`、`x64` 等。很多时候还是要自行处理。

### `init` 进程发现

!!! quote

    - [boot - How to know if I am using systemd on Linux? - Super User](https://superuser.com/questions/1017959/how-to-know-if-i-am-using-systemd-on-linux)

我们需要判断 `init` 进程，以确定某些功能是否可用，比如 `systemd`。

```bash
ps --no-headers -o comm 1
```

与普通发行版要么是 `systemd` 要么是 `init` 不同，容器中的情况比较神奇：

- Docker 中为 [:simple-github: `tini`](https://github.com/krallin/tini)，一个妙妙小工具。
- `systemd-nspawn`
    - 不带参数的为默认 Shell，大部分情况为 `bash`。
    - 带可执行文件则直接为文件名，比如带 `/root/test.sh` 则直接为 `test.sh`。
- `chroot` 与切换前一致。

## Squid 缓存

由于系统构建需要大量的网络资源，我们使用 [Squid](https://www.squid-cache.org/) 作为缓存服务器，加速构建过程。

### 基础配置

Squid 自带的配置文件 `squid.conf` 中包含了大量的注释，请自行查阅。一般默认配置包含下面的内容：

```text
acl localnet src 0.0.0.1-0.255.255.255  # RFC 1122 "this" network (LAN)
acl localnet src 10.0.0.0/8             # RFC 1918 local private network (LAN)
acl localnet src 100.64.0.0/10          # RFC 6598 shared address space (CGN)
acl localnet src 169.254.0.0/16         # RFC 3927 link-local (directly plugged) machines
acl localnet src 172.16.0.0/12          # RFC 1918 local private network (LAN)
acl localnet src 192.168.0.0/16         # RFC 1918 local private network (LAN)
acl localnet src fc00::/7               # RFC 4193 local private network range
acl localnet src fe80::/10              # RFC 4291 link-local (directly plugged) machines
acl SSL_ports port 443
acl Safe_ports port 80          # http
acl Safe_ports port 21          # ftp
acl Safe_ports port 443         # https
acl Safe_ports port 70          # gopher
acl Safe_ports port 210         # wais
acl Safe_ports port 1025-65535  # unregistered ports
acl Safe_ports port 280         # http-mgmt
acl Safe_ports port 488         # gss-http
acl Safe_ports port 591         # filemaker
acl Safe_ports port 777         # multiling http
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access allow localhost manager
http_access deny manager
http_access allow localhost
http_access deny to_localhost
http_access deny to_linklocal
include /etc/squid/conf.d/*.conf
http_access deny all
http_port 3128
coredump_dir /var/spool/squid
refresh_pattern ^ftp:           1440    20%     10080
refresh_pattern -i (/cgi-bin/|\?) 0     0%      0
refresh_pattern \/(Packages|Sources)(|\.bz2|\.gz|\.xz)$ 0 0% 0 refresh-ims
refresh_pattern \/Release(|\.gpg)$ 0 0% 0 refresh-ims
refresh_pattern \/InRelease$ 0 0% 0 refresh-ims
refresh_pattern \/(Translation-.*)(|\.bz2|\.gz|\.xz)$ 0 0% 0 refresh-ims
refresh_pattern .               0       20%     4320
```

- `acl` 指令定义了一些 ACL。
- `http_access` 指令根据这些 ACL 进行访问控制，**它们的顺序很重要**。
- `http_port` 指令定义了 Squid 监听的端口。
- `refresh_pattern` 指令定义了缓存的刷新策略。

### 中间人代理 HTTPS

!!! quote

    - [在 Squid 服務中配置 SSL Bumping](https://support.kaspersky.com/kwts/6.1/zh-HantTW/166244.htm)：实测正确的方法，按照这个文档配置即可。
    - [Intercept HTTPS CONNECT messages with SSL-Bump | Squid Web Cache wiki](https://wiki.squid-cache.org/ConfigExamples/Intercept/SslBumpExplicit)
    - [Feature: Squid-in-the-middle SSL Bump | Squid Web Cache wiki](https://wiki.squid-cache.org/Features/SslBump)

Squid 作为 HTTP 服务器，从原理上讲是无法代理 HTTPS 流量的。我们可以在其日志中看到它对 CONNECT 方法的处理为 `TCP_TUNNEL` 而不是期望的 `GET` 等 HTTP 方法：

```text
1736900429.951 181115 172.18.0.1 TCP_TUNNEL/200 654989992 CONNECT registrationcenter-download.intel.com:443 - HIER_DIRECT/23.200.143.19 -
```

为了代理 HTTPS 流量，Squid 使用中间人方法：

- 代理服务器（Squid）拦截 CONNECT 请求，但不会直接建立到目标服务器的加密通道。相反，它生成一个伪造的证书，声称自己就是目标服务器。
- 客户端看到 Squid 返回的伪造证书后，与代理服务器建立一个加密的 TLS 会话。
- Squid 再与实际目标服务器建立真实的 TLS 加密连接。这一步是透明的，目标服务器并不知道流量已经被拦截。
- 代理服务器解密客户端和目标服务器之间的通信。此时，数据是明文的。
- 在解密和处理完成后，代理服务器会重新加密数据：
    - 向客户端：使用伪造证书加密。
    - 向目标服务器：使用目标服务器的真实证书加密。

Squid 为每个网站动态生成证书，我们需要为其提供签发这些证书的 CA。

> `ssl-bump`
>
> For each CONNECT request allowed by ssl_bump ACLs, establish secure connection with the client and with the server, decrypt HTTPS messages as they pass through Squid, and treat them as unencrypted HTTP messages, becoming the man-in-the-middle.
>
> `generate-host-certificates[=<on|off>]`
>
> Dynamically create SSL server certificates for the destination hosts of bumped CONNECT requests. When enabled, the cert and key options are used to sign generated certificates. Otherwise generated certificate will be selfsigned.
>
> If there is a CA certificate lifetime of the generated certificate equals lifetime of the CA certificate. If generated certificate is selfsigned lifetime is three years. This option is enabled by default when ssl-bump is used. See the ssl-bump option above for more information.

除了按照参考文献中的第一个文档配置外，有一些变更：

- `SINGLE_DH_USE` 等选项已被弃用，参考 [[squid-users] Transition from squid3.5 to squid4; ciphers don't work anymore, ERROR: Unknown TLS option SINGLE_DH_USE](https://lists.squid-cache.org/pipermail/squid-users/2018-February/017640.html)。
