---
tags:
  - 不完善
---

# 目录服务：LDAP

!!! quote

    - [LDAP.com](https://ldap.com/)
    - [RFC 4510 - Lightweight Directory Access Protocol (LDAP): Technical Specification Road Map](https://datatracker.ietf.org/doc/html/rfc4510)
    - [Chapter 3 LDAP Schemas, ObjectClasses and Attributes - zytrax](https://www.zytrax.com/books/ldap/ch3/)

!!! tip

    阅读本文前，你最好已经修读过《数据库系统》或者了解数据库系统的基本概念。

LDAP 轻量目录访问协议（Lightweight Directory Access Protocol）是一种用于访问和维护分布式目录信息服务的协议。LDAP 是一种客户端 - 服务器协议，客户端通过 LDAP 协议向服务器请求信息，服务器通过 LDAP 协议返回信息。

## 目录服务 Directory Service

目录服务是一个储存、组织和提供信息访问服务的软件系统。在软件工程中，一个目录是指一组名字和值的映射。它允许根据一个给出的名字来查找对应的值，与词典相似。像词典中每一个词也许会有多个词义，在一个目录中，一个名字也许会与多个不同的信息相关联。类似地，就像一个词会有多个不同的发音和多个不同的词义，目录中的一个名字可能会有多个不同类型的值。

目录也许只提供范围非常小的节点类型和数值类型，也可能对任意的或可扩展的一组类型提供支持。在一个电话目录中，节点就是姓名而数值项就是电话号码。在 DNS 中，节点是域名而数值项是 IP 地址（还有别名，邮件服务器名等等）。在一个网络操作系统的目录中，节点是那些由操作系统所管理的资源，包括用户、计算机、打印机和其它共享资源。

在目录服务中，信息是按照树状结构组织的，这与 MySQL 等关系型数据库的表状结构不同。树状结构的每一个节点都可以包含多个子节点，每一个节点都可以包含多个属性，每个属性都有一个名字和一个或多个值。

## LDAP 数据模型

在 LDAP 中，树称为目录信息树（Directory Information Tree，DIT），每个节点称为条目（Entry）。

### 条目（Entry）

LDAP 条目是关于实体的信息集合。每个条目由三个主要组成部分构成：

- 区分名（Distinguished Name，DN）
- 属性集合
- 对象类集合

目录服务条目（Directory Service Entry，DSE）是一个特殊的条目，它提供关于目录服务器内容和功能的信息。LDAP 定义了两种类型的 DSE：

- 根 DSE（Root DSE）：根 DSE 是 LDAP 目录树的顶层，它提供了关于 LDAP 服务器的基本信息，如支持的 LDAP 版本、支持的身份验证方法、支持的扩展等。
- 配置 DSE（Config DSE）：配置 DSE 包含有关目录服务器配置的信息，例如服务器支持的模式（schema）和其他配置参数。

这些 DSE 在 LDAP 服务器中不存储在通常意义上的目录数据中，而是作为 LDAP 协议的一部分提供给客户端查询和获取信息的接口。

### DN

DN 唯一标识该条目及其在 DIT 层次结构中的位置。LDAP 条目的 DN 类似于文件系统上的文件路径。

LDAP DN 由零个或多个相对区分名（Relative Distinguished Name，RDN）组成，每个 RDN 由一个或多个（通常只有一个）属性 - 值对组成。如果一个 RDN 有多个属性 - 值对，它们用加号分隔。

!!! example

    ```text
    uid=john.doe
    ```

    这是一个由 `uid` 属性和 `john.doe` 值组成的 RDN。

    ```text
    givenName=John+sn=Doe
    ```

    这是一个由 `givenName` 和 `sn` 两个属性组成的 RDN。

- 由零个 RDN 组成的 DN 称为空 DN，它表示 Root DSE。
- 对于具有多个 RDN 的 DN，每个 RDN 按照向树的根部靠近的顺序表示层次结构的级别，RDN 之间用逗号分隔。

!!! example

    ```text
    uid=john.doe,ou=People,dc=example,dc=com
    ```

    该 DN 有四个 RDN，其父 DN 为 `ou=People,dc=example,dc=com`。

### 属性

属性保存条目的数据。每个属性具有一个属性类型、零个或多个属性选项，以及组成实际数据的一组值。

- 属性类型（attribute type）：可以看作是数据库的 schema。
    - 对象标识符（Object Identifier，OID）：属性类型必须有一个 OID，以及零个或多个可用于引用该类型属性的名称。
    - 属性语法（attribute syntax）：指定可以存储在该类型属性中的数据类型。
    - 匹配规则（matching rule）：指定如何比较属性值。
    - 还可以指示属性在同一条目中是否允许具有多个值，并且属性是否用于保存用户数据（用户属性）或用于服务器操作（操作属性）
- 属性选项（attribute options）：不作介绍

### 对象类

### 模式（Schema）

LDAP Schema 至少包含以下元素：

- 属性语法（Attribute Syntaxes）定义了可以在目录服务器中表示的数据类型。
- 匹配规则（Matching Rules）定义了可以针对 LDAP 数据执行的比较类型。
- 属性类型（Attribute Types）定义了可能存储在条目中的具名信息单元。
- 对象类（Object Classes）定义了属性类型的命名集合，可以在包含该类的条目中使用，以及哪些属性类型是必需的而不是可选的。

## LDAP 协议

## LDAP 部署与配置

### ID 约定

因为某些服务在系统早期启动，此时 SSSD 服务暂未启动，依赖于 `/etc` 目录下的用户（组）信息。为了防止和 LDAP 中的信息冲突导致问题，需要对齐本地文件和 LDAP 中的 ID 分配。

!!! example

    我们在使用 Docker 时遇到了这个问题。`docker` 用户组在安装时会分配一个 GID，比如可能是 `996`。这与我们在 LDAP 中为 `docker` 组设定的 GID `700` 不一致。

    `docker.socket` 在 SSSD 之前启动，且无法改变这一顺序，因为有 `sssd.service` -> `socket.target` -> `docker.socket` 这条依赖链。`docker.socket` 启动时使用 `docker` 用户组创建套接字，此时创建的套接字的 GID 是 `996`。

    等 SSSD 服务启动，此后查询 `docker` 用户组，得到的 ID 就都是 `700` 了，与套接字上的 GID 不一致，视为不同用户组。因此会出现即使用户在 `docker` 组里，使用 `docker` 命令仍然遇到 `docker.sock: connect: permission denied` 的令人困惑的问题。

用户组 GID 划分如下：

| 范围 | 描述 |
| --- | --- |
| `0-200, 900-999` | 保留给本地文件 `/etc/group`，此范围外的 GID 都在 LDAP 中 |
| `700-899` | 需要在集群中统一的软件用户组，比如 `docker`、`munge`、`slurm` 等 |
| `1000-1999` | 用户对应的用户组 |
| `2000-2999` | 项目对应的用户组 |
| `3000` | 全体队员所属用户组 `Teamers` |
