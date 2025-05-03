# 系统运维

系统运维负责集群架构的设计和维护。系统运维解决的问题是：

- 考虑数十台物理服务器，如何管理它们？
- 用户账户、数据存储怎么做？
- 怎么保证系统服务的灾备和高可用？

系统运维文档比较多，因为涉及软件和硬件中很多基础、重要的环节。

## 集群架构设计

!!! quote

    - [Bootstrapping an Infrastructure - NASA](http://www.infrastructures.org/papers/bootstrap/bootstrap.html)
    - [Plan your installation - FAI](https://fai-project.org/fai-guide/#plan)

在动手操作之前，应当投入一定时间进行详细的设计规划。比如参考文献中就提出了以下步骤：

> 1. Version Control -- CVS, track who made changes, backout
> 1. Gold Server -- only require changes in one place
> 1. Host Install Tools -- install hosts without human intervention
> 1. Ad Hoc Change Tools -- 'expect', to recover from early or big problems
> 1. Directory Servers -- DNS, NIS, LDAP
> 1. Authentication Servers -- NIS, Kerberos
> 1. Time Synchronization -- NTP
> 1. Network File Servers -- NFS, AFS, SMB
> 1. File Replication Servers -- SUP
> 1. Client File Access -- automount, AMD, autolink
> 1. Client OS Update -- rc.config, configure, make, cfengine
> 1. Client Configuration Management -- cfengine, SUP, CVSup
> 1. Client Application Management -- autosup, autolink
> 1. Mail -- SMTP
> 1. Printing -- Linux/SMB to serve both NT and UNIX
> 1. Monitoring -- syslogd, paging
