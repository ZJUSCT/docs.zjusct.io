---
tags:
  - 不完善
---

# 编译/构建系统

## GNU Make

```makefile
all: hello.exe

hello.exe: hello.o
	gcc -o hello.exe hello.o

hello.o: hello.c
	gcc -c hello.c

clean:
	rm hello.o hello.exe
```

- 使用 ++tab++ 缩进命令。

!!! failure "必须使用制表符缩进"

    如果没有使用制表符缩进，会得到 `makefile:4: *** missing separator. Stop`

每个规则都有三个部分：一个目标、一个必需品列表和一个命令

```makefile
target: pre-req-1 pre-req-2 ...
	command
```

- 运行 `make` 时默认启动 `all` 的生成。

`make` 检查一个规则时，先查找必须品列表中的文件。如果文件不存在，则寻找生成文件的规则；如果所有文件都比目标旧，则不会执行生成命令（提示 `Nothing to be done`）。

- 注释：`#` 直到行尾

- 规则语法：

```makefile
target1 [target2 ...]: [pre-req-1 pre-req-2 ...]
  	[command1
  	command2
  	....]
```

- 伪目标（人工目标）：只执行命令，不生成文件。标准伪目标有：`all`、 `clean`、 `install`。
- 变量：`$` 开头，用圆括号或花括号包裹。如 `$(CC)`。
- 自动变量：
    - `$@`：目标文件名
    - `$*`：目标文件名（不带扩展名）
    - `$<`：第一个必需品的文件名
    - `$^`：所有必须品的文件名（用空格分隔，去除重复）
    - `$+`：所有必须品的文件名（用空格分隔，不去除重复）
    - `$?`：所有比目标新的必须品的文件名
- 虚拟路径：
    - `VPATH`：设定寻找依赖项和目标文件的路径，如 `VPATH = src include`
    - `vpath`：设定某类文件的寻找路径，如 `vpath %.c src`
- 模式：

    ```makefile
    %.o: %.c
    	$(COMPILE.c) $(OUTPUT_OPTION) $<
    ```

    - `%` 匹配文件名

## GNU Autotools

!!! info ""

    - [Tutorial](https://www.lrde.epita.fr/~adl/autotools.html)
    - [Doc](https://www.gnu.org/software/automake/manual/html_node/Autotools-Introduction.html)

历史较为悠久的项目都会使用 GNU Autotools 来构建项目，标准流程为：

```bash
./configure && make && make install
```

需要熟悉的工具是 Autoconf 和 `autoreconf`，其他工具一般不需要直接操作。

### 文件结构

在 `./configure` 阶段可以使用 `--prefix=/path/to/dir` 参数指定安装路径，默认为 `/usr/local`。

构建工具将在该目录下生成文件，标准架构如下：

```text
prefix
├── bin
├── include
├── lib
├── share
│   ├── man
│   ├── info
│   ...
...
```

### Autoconf

`./configure` 自动检测系统中的环境变量、库、头文件等，基于 `configure.ac` 等文件生成 `Makefile` 等文件。

可以指定的变量：

```text
CC
CFLAGS
CXX
CXXFLAGS
LDFLAGS
CPPFLAGS (for both C and C++)
```

使用 `./configure --help` 查看帮助。

??? note "觉得在命令行中指定参数不方便？"

    如果觉得写命令行参数太长，可以把变量指定到 `config.site` 文件中：

    ```text title="config.site"
    test -z "$CC" && CC=gcc-3
    test -z "$CPPFLAGS" && CPPFLAGS=-I$HOME/usr/include
    test -z "$LDFLAGS" && LDFLAGS=-L$HOME/usr/lib
    ```

    运行 `./configure` 时应当会提示如 `configure: loading site script /home/adl/usr/share/config.site`。

??? note "不需要在源文件目录中构建"

    `./configure` 在哪里运行，程序、目标文件和库文件就在哪里生成。因此，可以任何你希望的地方开始构建项目。

    ```bash
    mkdir build && cd build
    /nfs/src/amhello-1.0/configure
    make
    ```

    这样可以方便地使用一份源代码为多个平台构建项目。

??? note "交叉编译"

    使用 `--host` 参数指定目标体系结构。

    ```bash
    ./configure --host=i586-mingw32msvc
    ```

    `--target` 参数用于构建编译工具，指定编译工具的目标体系结构。

### Automake

`automake` 接受 `Makefile.am` 文件，生成 `Makefile.in` 文件。

可以指定的变量：

```text
DESTDIR
```

一些通用的 target：

```text
all
install
clean
distclean
```

### Libtool

`libtool` 用于处理库文件，可以生成 `.la` （libtool archive）文件。和它有关的操作都会被翻译为真实的库文件。

!!! warning "库文件是可移植性的地狱"

    在不同平台上，库文件类型不同、编译选项不同。

    在 Linux 上，静态库为 `.a` 文件，动态库为 `.so` 文件。编译选项 `-fPIC` 用于生成位置无关代码，`-shared` 用于生成动态库。

在安装时可以使用下面的参数控制库文件生成：

```text
--enable-shared
--disable-shared
--enable-static
--disable-static
```

### 附：编写模板文件

为了使用 GNU Autotools 构建项目，至少需要编写下面的文件：

- `configure.ac`
- `Makefile.am`
- `src/Makefile.am`

`autoconf` 会按合适的顺序执行所有自动化工具。

```bash
autoreconf --install
```

## CMake
