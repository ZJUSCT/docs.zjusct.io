---
tags:
  - 不完善
---

# 环境管理：Lmod

## 安装

!!! quote

    - [Lmod Doc: Installing Lua and Lmod](https://lmod.readthedocs.io/en/latest/030_installing.html)

官方文档中提供了详细的安装配置，按照文档完成以下任务即可：

- 使用包管理器安装 Lua

```bash
sudo apt update
sudo apt -y build-dep lmod
lua_ver=$(which lua | xargs realpath -e | xargs basename)
sudo apt -y install lib${lua_ver}-dev tcl-dev
```

- 下载 Lmod 源码并构建安装（或者直接 clone 仓库）

```bash
git clone https://github.com/TACC/Lmod.git
cd Lmod
./configure --prefix=/opt/apps
make
make install
```

- 链接 Lmod 为各个 Shell 提供的启动脚本到系统路径

```bash
ln -s /opt/apps/lmod/lmod/init/profile        /etc/profile.d/z00_lmod.sh
ln -s /opt/apps/lmod/lmod/init/cshrc          /etc/profile.d/z00_lmod.csh
ln -s /opt/apps/lmod/lmod/init/profile.fish   /etc/fish/conf.d/z00_lmod.fish
```

- 确认各个 shell 下 Lmod 正确运行

这里需要作一些调整，`/etc/profile.d` 下的文件只会在用户登录时执行一次，而使用 MPI 等执行脚本时往往是 non-interactive non-login shell，因此需要配置使任何情况下 shell 都能加载 Lmod。

```bash title="/etc/bash.bashrc"
if [ -d /etc/profile.d ]; then
  for i in /etc/profile.d/*.sh; do
    if [ -r $i ]; then
      . $i
    fi
  done
fi
```

```zsh title="/etc/zsh/zshrc"
if [ -d /etc/profile.d ]; then
  setopt no_nomatch
  for i in /etc/profile.d/*.sh; do
    if [ -r $i ]; then
      . $i
    fi
  done
  setopt nomatch
fi
```

## 维护

Lmod 稳定版约每年更新一次，按照官方文档的指引，可以在新版本发布后进行升级：

- `make pre-install`：构建新版本，进行测试
- `make install`：测试通过后，替换旧版本的链接

## 概念

### one name 规则

- 一种 module 可以有多个版本，但只能有一个处于活动状态
- 有一些关键组件，只能加载一种实现，比如编译器、MPI
    - 它们会在 modulefile 中带上 `family` 字段，比如 `family("compiler")`。

### Module 层次结构

!!! quote

    - [How to use a Software Module hierarchy - Lmod](https://lmod.readthedocs.io/en/latest/080_hierarchy.html)

`MODULEPATH` 下的文件应当按照软件层次结构组织。按官方文档描述，应分为三层 `/opt/apps/modulefiles/{Core,Compiler,MPI}`：

- Core 目录用于那些不依赖于编译器或 MPI 实现的模块。
    - 编译器的模块文件被放置在 Core 目录中。
- Compiler 目录用于仅依赖于编译器的软件包。
    - MPI 实现的模块文件被放置在 Compiler 目录下，因为它们只依赖于编译器。
- MPI 目录用于依赖于 MPI-编译器配对的软件包。

举例如下：

```text
modulefiles
├── Core
│   ├── gcc
│   │   ├── 4.8.5.lua
│   │   ├── 5.4.0.lua
│   │   └── 7.3.0.lua
│   └── oneapi
│       ├── 2021.1.1.lua
│       └── 2021.2.0.lua
├── Compiler
│   └── oneapi
│       ├── 2021.1.1
│       │   ├── openmpi
│       │   │   ├── 4.0.5.lua
│       │   │   └── 4.1.0.lua
│       │   └── mpich
│       │       ├── 3.3.2.lua
│       │       └── 3.4.1.lua
│       └── 2021.2.0
│           ├── openmpi
│           │   ├── 4.0.5.lua
│           │   └── 4.1.0.lua
│           └── mpich
│               ├── 3.3.2.lua
│               └── 3.4.1.lua
└── MPI
    └── oneapi
        └── 2021.1.1
            ├── openmpi
            │   ├── 4.0.5
            │   │   └── hpl
            │   │       ├── 2.3.lua
            │   │       └── 2.4.lua
            │   └── 4.1.0
            │       └── hpl
            │           ├── 2.3.lua
            │           └── 2.4.lua
            └── mpich
                ├── 3.3.2
                │   └── hpl
                │       ├── 2.3.lua
                │       └── 2.4.lua
                └── 3.4.1
                    └── hpl
                        ├── 2.3.lua
                        └── 2.4.lua
```

## 编写 Module file

[An Introduction to Writing Modulefiles](https://lmod.readthedocs.io/en/latest/015_writing_modules.html)

Modulefile 放置在 `MODULEPATH` 下的子目录中。目录名就是 module 名，文件名是版本名。比如 `ddt` 软件的 modulefile 可能是这样的：

```text
/apps/modulefiles/ddt/5.0.1.lua
```

一些常用函数如下：

```lua
-- 帮助
help([[
    text
]])
whatis("Description: text")
-- 环境变量
setenv("NAME", "VALUE")
prepend_path("PATH", "/path/to/bin")
append_path("LD_LIBRARY_PATH", "/path/to/lib")
pushenv("NAME", "VALUE")
-- 依赖
load("module1", "module2")
try_load("module1", "module2")
always_load("module1", "module2")
prereq("module1", "module2")
prereq(atleast("module1", "1.2.3"))
```

## 用户自定义 module

[Advanced User Guide for Personal Modulefiles](https://lmod.readthedocs.io/en/latest/020_advanced.html)

我们在集群中设置默认 `MODULEPATH` 指向 `/opt/apps/modulefiles`，提供通用的软件包。用户可以在自己的目录下创建 `modulefiles`，按文档将其添加到 `MODULEPATH` 中，即可同时使用自己的 module 和集群提供的 module。
