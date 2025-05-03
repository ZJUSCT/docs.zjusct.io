# macOS 运维

我们有一台 Mac Mini M4 Pro，它是一台非常强大的服务器。本文记录 macOS 上的运维经验。很多资料来自 Apple 官方开发者网站：[Apple Developer](https://developer.apple.com/)。

## launchd

!!! quote

    - [About Daemons and Services - Apple Developer](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/Introduction.html)：官方文档，虽然是 2016 年 OS X 的 Archive，但依然很有参考价值。
    - [macOS launchctl commands – rakhesh.com](https://rakhesh.com/mac/macos-launchctl-commands/)：一个精简的入门教程，包含 launchctl 命令和服务示例。
    - [A launchd Tutorial](https://www.launchd.info/)：一个完善的 launchd 教程。

launchd 是 MacOS 的服务管理器，类似于 Linux 的 systemd（它们都是系统启动时内核运行的第一个进程）。

- luanchd 服务分为两类：

    | 服务类型 | 描述 | 目录 |
    | --- | --- | --- |
    | Daemon | 系统级别的服务，不需要用户登录就可以运行 | `/System/Library/LaunchDaemons` 或 `/Library/LaunchDaemons` |
    | Agent | 用户服务，需要用户登录才能运行 | `~/Library/LaunchAgents` |

- launchd 的命令行工具是 `launchctl`，常用命令有：

    ```bash
    sudo launchtl load /Library/LaunchDaemons/otelcol-contrib.plist
    sudo launchctl start otelcol-contrib
    sudo launchctl list | grep otelcol-contrib
    sudo launchctl stop otelcol-contrib
    sudo launchctl unload /Library/LaunchDaemons/otelcol-contrib.plist
    ```

- 服务配置文件是 plist 格式的文件。以 OpenTelemetry 为例，配置文件如下：

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
            <key>Label</key>
            <string>otelcol-contrib</string>
            <key>RunAtLoad</key>
            <true/>
            <key>KeepAlive</key>
            <true/>
            <key>Program</key>
            <string>/usr/local/bin/otelcol-contrib</string>
            <key>ProgramArguments</key>
            <array>
                    <string>/usr/local/bin/otelcol-contrib</string>
                    <string>--config=/etc/otelcol-contrib/config.yaml</string>
            </array>
            <key>EnvironmentVariables</key>
            <dict>
                    <key>OTEL_BEARER_TOKEN</key>
                    <string>your_key_here</string>
                    <key>OTEL_CLOUD_REGION</key>
                    <string>zjusct-cluster</string>
            </dict>
            <key>StandardOutPath</key>
            <string>/var/log/otelcol-contrib.log</string>
            <key>StandardErrorPath</key>
            <string>/var/log/otelcol-contrib-err.log</string>
    </dict>
    </plist>
    ```

    完整定义见 launchd.plist(5) manual page。可以使用 `plutil` 命令检查 plist 文件语法是否正确。修改配置文件后需要 `unload` 再 `load` 服务。

- 其他：
    - 配置为 `KeepAlive` 的服务会尝试保持运行，不管是异常退出还是手动停止都会重启。launchctl 没有 `restart`，但对于这样的服务 `stop` 就相当于 `restart`。

## 文件系统

!!! quote

    - [About Files and Directories - Apple Developer](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/Introduction/Introduction.html)

macOS 的文件系统布局与 UNIX 有一些显著的不同：

- APFS 下，根目录只读，无法创建文件/目录。可以使用 `synthetic.conf` 将文件夹映射到根目录，见 [finder - Unable to create folder in root of 'Macintosh HD'? - Ask Different](https://apple.stackexchange.com/questions/388236/unable-to-create-folder-in-root-of-macintosh-hd)。

其他：

- 同样使用 `/etc/fstab` 挂载 NFS，但参数有所不同，比如不支持 `default` 选项。

## 网络

!!! quote

    - [mac network commands cheat sheet](https://gree2.github.io/mac/2015/07/18/mac-network-commands-cheat-sheet)
