---
tags:
  - 完善
---

# 现代化 CLI 工具

!!! quote

    - [:simple-github: ibraheemdev/modern-unix](https://github.com/ibraheemdev/modern-unix)
    - [:simple-github: x-cmd/x-cmd](https://www.x-cmd.com/)
    - [Terminal Trove](https://terminaltrove.com/)

用户主要使用命令行用户界面（Command Line Interface，CLI）登陆集群。集群上安装了一些现代化的 CLI 工具，它们有的提高了视觉体验，有的提供了更丰富的功能，有的进行了性能优化。借助这些现代化的 CLI 工具，可以让你更高效地使用集群。

## [`aria2c`](https://github.com/aria2/aria2) (`wget`, `curl`)

aria2 是一个轻量级的多协议、多来源、跨平台下载工具，运行于命令行界面。它支持 HTTP/HTTPS、FTP、SFTP、BitTorrent 和 Metalink。

`aria2c` 是 aria2 的命令行客户端，可以视为 `wget` 和 `curl` 的替代品。最常见的用法是进行多连接下载，这也能充分利用集群的多拨带宽优势，常见情况下都能直接跑到满速：

```shell
aria2c -x16 http://example.com/file.iso
```

## [`bat`](https://github.com/sharkdp/bat) (`cat`)

`bat` 是 `cat` 命令的增强版本，使用 Rust 编写，集成了语法高亮、Git 集成和自动分页功能。

它的语法高亮支持多种编程语言和标记语言，使代码在终端中更加易读。Git 集成功能允许用户查看与索引相关的修改，突出显示新增或更改的行。

`bat` 会使用类似于 `less` 的分页器自动分页内容，提高可读性。此外，`bat` 还可以显示不可打印字符，并支持文件串联，保持了基本文本查看和合并任务的实用性。

![bat](https://camo.githubusercontent.com/a9789c5200bdb0a22602643d7bf85f0f424ddd4259e763abc865609010c5e228/68747470733a2f2f696d6775722e636f6d2f724773646e44652e706e67)

??? info

    在 Debian APT 中包名为 `bat`，二进制名为 `batcat`，与之发生命名冲突的包为 `bacula-console-qt`（见 [:simple-github: Issue #656 · sharkdp/bat](https://github.com/sharkdp/bat/issues/982)）。

    为了使用方便，我们创建了别名 `bat`：

    ```shell
    ln -s /usr/bin/batcat /usr/bin/bat
    ```

## [`btop`](https://github.com/aristocratos/btop) (`top`)

`btop` 是一个终端资源监控工具，实时可视化您机器的 CPU、内存、磁盘、网络和进程的使用统计。

它使用 C++ 编写，TUI 用户界面提供清晰、交互和详细的图表，并且响应迅速。它具有电池计和过滤进程的功能，可以以树状图显示进程，显示网络使用的自适应缩放图表，以及磁盘活动的 I/O 活动等更多有用信息。

`btop` 非常适合需要即时分析系统状态，特别是监控资源密集型活动时使用。

![btop](https://github.com/aristocratos/btop/raw/main/Img/normal.png)

## [`duf`](https://github.com/muesli/duf) (`df`)

`Duf` 是一个用于以更友好的方式查看磁盘使用情况的工具，比 `df` 更快速。它使用 Go 语言编写，能够以文本和图形格式显示信息。

![duf](https://github.com/muesli/duf/raw/master/duf.png)

## [`dive`](https://github.com/wagoodman/dive)

A tool for exploring a docker image, layer contents, and discovering ways to shrink the size of your Docker/OCI image.

![dive](https://github.com/wagoodman/dive/raw/main/.data/demo.gif)

## [`eza`](https://github.com/eza-community/eza) (`ls`)

`eza` 是 Unix 和 Linux 系统中自带的 `ls` 文件列表命令行程序的替代品，小巧、快速且现代化。

它通过颜色区分文件类型和元数据，支持符号链接、扩展属性以及 Git 信息。

`eza` 是一个持续维护的分支，不要与它的旧版本 `exa` 混淆。

!!! note

    目前，`eza` 尚未进入 Debian APT 仓库。我们安装了 `exa`，它是 `eza` 的上一代版本，但已[停止维护](https://github.com/ogham/exa/issues/1243)。

![eza](https://eza.rocks/demo.gif)

你可以在自己的 shell 配置文件中添加别名：

```shell title="Gist: AppleBoiy/alias_eza.md"
alias ls='eza'
alias l='eza -lbF --git'
alias ll='eza -lbGF --git'
alias llm='eza -lbGd --git --sort=modified'
alias la='eza -lbhHigUmuSa --time-style=long-iso --git --color-scale'
alias lx='eza -lbhHigUmuSa@ --time-style=long-iso --git --color-scale'

# specialty views
alias lS='eza -1'
alias lt='eza --tree --level=2'
alias l.="eza -a | grep -E '^\.'"
```

```shell title="Gist: jponge/exa-aliases.sh"
alias l="exa --sort Name"
alias ll="exa --sort Name --long"
alias la="exa --sort Name --long --all"
alias lr="exa --sort Name --long --recurse"
alias lra="exa --sort Name --long --recurse --all"
alias lt="exa --sort Name --long --tree"
alias lta="exa --sort Name --long --tree --all"
alias ls="exa --sort Name"
```

## [`fd`](https://github.com/sharkdp/fd) (`find`)

`fd` 是一个基于 Rust 的命令行工具，旨在以简洁和高效的方式查找文件。

它被设计为比传统的 `find` 命令更易用且更快速的替代品。`fd` 以用户友好为特点，支持直观的语法、彩色输出和智能大小写搜索。

为了提高效率，它利用并行搜索，并默认遵守 `.gitignore` 规则，使开发者的文件搜索过程更加简化。

![fd](https://raw.githubusercontent.com/sharkdp/fd/refs/heads/master/doc/screencast.svg)

!!! info

    在 Debian APT 中包名为 `fd-find`，二进制名为 `fdfind`，与之发生命名冲突的包为 `fdclone`（见 [:simple-github: Issue #1009 · sharkdp/fd](https://github.com/sharkdp/fd/issues/1009)）。

    为了使用方便，我们创建了别名 `fd`：

    ```shell
    ln -s /usr/bin/fdfind /usr/bin/fd
    ```

## [`fq`](https://github.com/wader/fq) (`hexdump`)

`fq` 是一个命令行工具，类似于 `jq`，但用于处理二进制数据。它支持多种文件格式，如可执行文件、容器编解码器以及各种序列化格式等。

它具有将二进制数据显示为经过解码的树状结构的功能，并能够对数据进行转换、切片和连接，还支持嵌套格式。此外，`fq` 还包含一个交互式 REPL（Read-Eval-Print Loop，一种交互式编程环境），支持函数和名称的自动补全。

`fq` 非常适合用于查询、检查和调试二进制格式，尤其对从事调试和数据转换等领域的开发者有帮助，也可用于快速检查文件格式。

![fq](https://raw.githubusercontent.com/wader/fq/refs/heads/master/doc/demo.svg)

基本用法为 `fq . file`，`fq d file`，`fq 'some query' file`。

## [`fzf`](https://github.com/junegunn/fzf) (`grep`)

`fzf` 是一个命令行工具，提供了一种快速直观的方式来搜索和浏览文件、命令和目录，使用模糊匹配和自动补全功能。

`fzf` 可以用于任何列表，包括文件、命令历史、进程、主机名、书签、Git 提交等，并且可以与多种 Shell（如 zsh、bash 或 fish）、编辑器（如 vim 和 neovim）以及 tmux 集成。

`fzf` 具有可移植性，没有依赖关系，适用于 macOS、Windows、Linux 和 BSD 系统。

![fzf](https://raw.githubusercontent.com/junegunn/i/master/fzf-preview.png)

## [`gdu`](https://github.com/dundee/gdu) (`du`)

`gdu`（即 Go Disk Usage 的缩写）是一个快速的磁盘使用分析器，具有 TUI 界面。

它提供了磁盘使用的图形概览，显示最大的文件和文件夹，并在终端中展示可用空间及其管理功能。

推荐给系统管理员和需要快速监控和管理磁盘空间的用户，适用于 Windows、Mac 和 Linux 等任何平台。

> **`ncdu` took 7.4 seconds** to scan a home directory with around 280GB of content on an NVMe disk in the test, while **`gdu` completed the same task within milliseconds**

![gdu](https://cdn.terminaltrove.com/m/e8aca807-824e-4797-9644-fb147ea6f1e6.gif)

## [`gping`](https://github.com/orf/gping) (`ping`)

`gping` 类似于常规的 `ping` 命令，但带有图形化显示。它是一个终端应用程序，提供 `ping` 命令的实时可视化反馈。

它的功能包括多个主机的延迟测试、命令执行时间测试和颜色偏好自定义等。`gping` 跨平台可用，支持 Windows、Mac 和 Linux 系统，并且在使用完程序后提供清除终端图形的选项，确保不留杂乱信息。

`gping` 是网络、系统和 DevOps 工程师的优秀工具，也适合任何希望可视化 `ping` 输出的人。它在需要可读性和视觉沟通的环境中效果最佳。

![gping](https://github.com/orf/gping/raw/master/images/readme-example.gif)

??? info

    在 Debian APT 中，包名为 `gping`，目前进入了 testing 仓库。

## [`http`](https://github.com/httpie/cli) (`curl`, `telnet`)

HTTPie 是一个命令行 HTTP 客户端，旨在使与网络服务的 CLI 交互尽可能人性化。HTTPie 专为测试、调试以及与 API 和 HTTP 服务器的交互设计。通过 `http` 和 `https` 命令可以创建并发送任意 HTTP 请求，使用简单直观的语法，并提供格式化和彩色输出。

![httpie](https://raw.githubusercontent.com/httpie/httpie/master/docs/httpie-animation.gif)

## [`hyperfine`](https://github.com/sharkdp/hyperfine) (`time`)

`hyperfine` 是一个命令行基准测试工具。它通过多次运行提供统计分析，支持任意 Shell 命令，并在终端中提供持续的基准测试进度反馈。

其额外功能包括设置预热运行和清理缓存命令、统计离群值检测以及自定义基准测试。除了常规的基准测试，`hyperfine` 还支持将结果导出为多种格式，如 CSV、JSON、Markdown、AsciiDoc。

`hyperfine` 特别适合从事软件性能测试和优化的人，尤其是在处理大型或复杂的软件项目时。当你需要对应用程序、算法进行基准测试，或定期监控软件性能时，`hyperfine` 是一个值得拥有的工具。

![hyperfine](https://camo.githubusercontent.com/9bac9fc730637ebd007bdc51c6ec43d1e49b6f7ed92f00e087b71ec9c175fda6/68747470733a2f2f692e696d6775722e636f6d2f7a31394f5978452e676966)

## [`rg`](https://github.com/BurntSushi/ripgrep) (`grep`)

Ripgrep 是一个面向行的搜索工具，它会递归搜索当前目录中的正则表达式模式，同时遵守 `.gitignore` 规则。

Ripgrep 在 Windows、macOS 和 Linux 上均有一流的支持。

![rg](https://burntsushi.net/stuff/ripgrep1.png)

??? info

    在 Debian-based 发行版中，包名为 `ripgrep`。

## [`tig`](https://github.com/jonas/tig?ref=terminaltrove) (`git`)

`tig` 是一个基于 ncurses 的 Git 仓库用户界面工具，主要用于浏览 Git 仓库，帮助用户可视化 Git 历史。

其核心功能包括显示提交图、查看每次提交的差异，以及逐行暂存提交的功能。

此外，`tig` 还提供搜索工具、blame 视图和 cherry-pick 操作等附加功能。

![tig](https://cdn.terminaltrove.com/m/1c8cd88e-4883-452e-ad0e-756d4b3fb08c.gif)

## [`z`](https://github.com/ajeetdsouza/zoxide) (`cd`)

`zoxide` 是一个高级目录导航工具，替代 `cd` 命令，简化在常用目录之间的切换。

它基于 Rust 编写，兼容主流 Shell，能够智能排序常用目录，用户可以用更少的按键快速切换目录。

`zoxide` 跨平台支持，适用于 macOS、Windows、Linux 和 BSD 系统。

你可以按照 GitHub 上的说明在自己的 shell 中启用它。

![zoxide](https://github.com/ajeetdsouza/zoxide/raw/main/contrib/tutorial.webp)
