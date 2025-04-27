---
tags:
  - 完善
---

# 环境变量与 Shell

??? quote

    - [Why is /etc/profile not invoked for non-login shells? - AskUbuntu](https://askubuntu.com/questions/247738/why-is-etc-profile-not-invoked-for-non-login-shells)

对于 SSH 登录、远程执行命令、本机登录等不同场景，环境变量可能不同，这常常引起许多困惑。本篇文章根据相关资料总结一下环境变量的加载过程。

## Shell 的模式

??? quote

    - [login/non-login and interactive/non-interactive shells [duplicate] - StackExchange](https://unix.stackexchange.com/questions/170493/login-non-login-and-interactive-non-interactive-shells)
    - [Why is /etc/profile not invoked for non-login shells? - AskUbuntu](https://askubuntu.com/questions/247738/why-is-etc-profile-not-invoked-for-non-login-shells)
    - [`ssh <host>` is a login shell, but `ssh <host> <command>` is not? - SuperUser](https://superuser.com/questions/1224938/ssh-host-is-a-login-shell-but-ssh-host-command-is-not)

### login/non-login shell

login/non-login shell 的区别在于是否需要输入用户名密码。让我们举一些例子：

- 从控制台登录系统，需要输入用户名密码，这是 login shell。
- 使用 `su` 切换用户，需要输入指定用户的密码，这是 login shell。
- 使用 `ssh` 登录远程系统，需要输入密码，这是 login shell。
- 使用 `bash` 启动新的 shell，这是 non-login shell。
- 在**图形界面**下打开终端（如 konsole、gnome-terminal），这是 non-login shell。因为你已经通过如 GDM、KDM、LightDM 等图形化登录界面登录了系统。

可以看出，要启动 non-login shell，首先要有已经登录的用户。

### interactive/non-interactive shell

interactive/non-interactive shell 的区别是该 Shell 是否接受用户输入。让我们举一些例子：

- 从控制台登录系统，输入命令，这是 interactive shell。
- 使用 `bash -c 'echo hello'` 执行命令，这是 non-interactive shell。
- 使用 `bash` 启动新的 shell，这是 interactive shell。
- 使用 `bash` 启动新的 shell 执行脚本，这是 non-interactive shell。

值得注意的是，即使脚本中使用 `read` 等命令向用户请求输入，也是 non-interactive shell。因为这并不是 Shell 本身的交互，而是脚本中命令的交互。

### 两者的组合

`bash` 选项可以控制 shell 的模式：

- `-l`：login shell（虽然使用 `bash -l` 还是不需要输入用户名密码，但可以看到环境变量确实按 login shell 加载了）
- `-c`：non-interactive shell

!!! tip

    可以使用下面的命令[启动一个干净的 bash](https://unix.stackexchange.com/questions/48994/how-to-run-a-program-in-a-clean-environment-in-bash)：

    ```shell
    env -i bash --noprofile --norc
    ```

可以使用下列命令检查当前的 shell 模式：

- `echo $-`：
    - 包含 `i` 表示 interactive shell
    - 不包含 `i` 表示 non-interactive shell
- `shopt login_shell`：
    - `login_shell` 为 `on` 表示 login shell
    - `login_shell` 为 `off` 表示 non-login shell

使用 SSH 远程执行命令时，OpenSSH 将启动一个 non-login、non-interactive shell。

## Shell 启动时加载的文件

??? quote

    - [Zsh/Bash startup files loading order (.bashrc, .zshrc etc.) - WordPress](https://shreevatsa.wordpress.com/2008/03/30/zshbash-startup-files-loading-order-bashrc-zshrc-etc/)

`/etc/profile` 被认为是只在用户登录（login shell）时执行一次的文件。这导致我们使用 SSH 远程执行命令或使用 MPI 通过 SSH 启动进程时（为 non-login non-interactive shell），放置在 `/etc/profile` 中的相关环境变量均不会生效。对于不同的 Shell，应当查找其对应的启动文件，以确保环境变量的正确加载。

### Bash

??? quote

    - [Bash Startup Files - GNU](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html)

| 模式 | 文件 |
| --- | --- |
| login | `/etc/profile`<br>`~/.bash_profile`<br>`~/.bash_login`<br>`~/.profile` |
| interactive non-login | `~/.bashrc` |
| non-interactive non-login | 环境变量 `BASH_ENV` 指定的文件 |
| remote non-interactive | `~/.bashrc` |

??? info "关于 Bash 远程执行命令时加载文件的进一步探讨"

    [bash/shell.c - GitHub](https://github.com/bminor/bash/blob/master/shell.c#L1124)

    ```c title="shell.c"
        /* If we were run by sshd or we think we were run by rshd, execute
        ~/.bashrc if we are a top-level shell. */
    #if 1   /* TAG:bash-5.3 */
        if ((run_by_ssh || isnetconn (fileno (stdin))) && shell_level < 2)
    #else
        if (isnetconn (fileno (stdin) && shell_level < 2)
    #endif
    ```

    [bash/config-top.h - GitHub](https://github.com/bminor/bash/blob/master/config-top.h#L109)

    ```c title="config-top.h"
    /* Define this if you want bash to try to check whether it's being run by
    sshd and source the .bashrc if so (like the rshd behavior).  This checks
    for the presence of SSH_CLIENT or SSH2_CLIENT in the initial environment,
    which can be fooled under certain not-uncommon circumstances. */
    /* #define SSH_SOURCE_BASHRC */
    ```

    `SSH_SOURCE_BASHRC` 默认为 undefined。那唯一的条件就是，如果stdin 为网络连接，则会加载 bashrc。

    判断网络连接的方式为，测试下 getpeername 会不会报错：[bash/netconn.c - GitHub](https://github.com/bminor/bash/blob/master/lib/sh/netconn.c#L44)

### Fish

??? quote

    - [Configuration files - Fish Shell](https://fishshell.com/docs/current/language.html#configuration)

!!! warning "Fish 不会读取 `/etc/profile`"

- Configuration snippets:
    - `~/.config/fish/conf.d/`
    - `/etc/fish/conf.d/`
    - `~/.local/share/fish`
    - `/usr/share/fish/vendor_conf.d`
    - `/usr/local/share/fish/vendor_conf.d`
- System-wide configuration files: `/etc/fish/config.fish`
- User configuration: `~/.config/fish/config.fish`

Fish 文档说明，不论以何种方式启动，都会按照上述顺序加载配置文件。但实际操作时，发现 non-interactive 时似乎不会加载 snippets。总之，对于 Fish，要保证所有情况下加载，应当将配置直接写入 `/etc/fish/config.fish`。

### Zsh

??? quote

    - [Startup Files - SourceForge](https://zsh.sourceforge.io/Intro/intro_3.html)
    - [ZSH startup file headaches - GitHub](https://gist.github.com/pbrisbin/45654dc74787c18e858c)

- `/etc/zsh/zshenv`
- `~/.zshenv`
- `/etc/zsh/zprofile` (if login shell)
- `~/.zprofile`   (if login shell)
- `/etc/zsh/zshrc`    (if interactive)
- `~/.zshrc`      (if interactive)
- `/etc/zsh/zlogin`   (if login shell)
- `~/.zlogin`     (if login shell)

对于 Zsh，要保证所有情况下加载，应当将配置直接写入 `/etc/zsh/zshrc`。

## 远程执行命令的方式

远程执行命令有非常多种方式，不一定涉及 Shell。

- SSH 总是通过用户的 Login Shell 执行命令，但该 Shell 的状态不一定能够是 login 的。比如，执行一个不存在的命令，会由 Login Shell 报告错误信息：

    ```shell
    $ ssh machine non-exist
    fish: Unknown command: non-exist
    ```

- Slurm 远程执行则不涉及 Shell。启动不存在的文件，可以看到是由 `execve()` 报告错误信息：

    ```shell
    $ srun non-exist
    slurmstepd: error: execve(): non-exist: No such file or directory
    ```
