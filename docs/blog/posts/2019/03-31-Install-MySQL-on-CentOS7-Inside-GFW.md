---
title: 如何在墙内快速部署 CentOS 7 的 MySQL
date:
  created: 2019-03-31 10:45:19
categories: [MySQL, CentOS]
authors: [王克]
---

MySQL 被 Oracle 收购后，CentOS 的镜像仓库中提供的默认的数据库也变为了 MariaDB，所以默认没有 MySQL，需要手动安装。

其实安装 MySQL 也并不是一件很难的事情，但是由于一些实际存在的问题 (比如某墙)，让默认通过 yum 安装 MySQL 的速度太慢。这里提出一种可行的方案来快速部署 MySQL，此方案同样适用于其他 rpm 包软件的手动安装。

本文实际在讲的是，如何利用各种手段，加速和改善 yum 的安装过程。

<!-- more -->

## 传统方案……慢到怀疑人生

根据[官方指南](https://dev.mysql.com/downloads/repo/yum/)，我们执行如下命令：

```bash
# 下载源
wget "https://dev.mysql.com/get/mysql80-community-release-el7-2.noarch.rpm"
# 安装源
sudo rpm -ivh mysql80-community-release-el7-2.noarch.rpm
# 检查源是否成功安装
sudo yum repolist enabled | grep "mysql80-community*"
```

接下来就是正常的安装步骤：

```bash
sudo yum install mysql-community-server mysql
```

但是由于一些原因，下载速度基本是几 Byte/s，MySQL 服务器的大小 (加上依赖服务) 差不多有 600MB，这种方法基本不可取。手头没有特别好的而且很新的软件源，就打算手动安装。

## 手动安装法

首先依然需要下载并安装官方源。

```bash
yum install mysql-community-server
```

利用该命令我们可以获取一些 MySQl Server 以来安装顺序及其版本：

```plain
=================================================================================================
 Package                       Arch          Version              Repository                Size
=================================================================================================
Reinstalling:
 mysql-community-client        x86_64        8.0.15-1.el7         mysql80-community         25 M

 mysql-community-libs          x86_64        8.0.15-1.el7         mysql80-community          2 M

 mysql-community-common        x86_64        8.0.15-1.el7         mysql80-community        570 K

 mysql-community-server        x86_64        8.0.15-1.el7         mysql80-community        360 M

Transaction Summary
=================================================================================================
```

解压并分析 rpm 源包：

```bash
rpm2cpio mysql80-community-release-el7-2.noarch.rpm | cpio -div
vim /etc/yum.repos.d/mysql-community.repo
```

从中我们可以找到对应版本的网络路径为`http://repo.mysql.com/yum/mysql-8.0-community/el/7/x86_64/`。

打开该地址，找到对应的几个安装包：

* mysql-community-client-8.0.15-1.el7.x86_64.rpm
* mysql-community-libs-8.0.15-1.el7.x86_64.rpm
* mysql-community-common-8.0.15-1.el7.x86_64.rpm
* mysql-community-server-8.0.15-1.el7.x86_64.rpm

使用某种下载工具 (我使用的是迅雷) 下载，然后使用`scp`指令上传到服务器上：

```bash
scp mysql-community-client-8.0.15-1.el7.x86_64.rpm xxx@xx.xx.xx.xx:/root/mysql-community-client-8.0.15-1.el7.x86_64.rpm
scp mysql-community-libs-8.0.15-1.el7.x86_64.rpm xxx@xx.xx.xx.xx:/root/mysql-community-libs-8.0.15-1.el7.x86_64.rpm
scp mysql-community-common-8.0.15-1.el7.x86_64.rpm xxx@xx.xx.xx.xx:/root/mysql-community-common-8.0.15-1.el7.x86_64.rpm
scp mysql-community-server-8.0.15-1.el7.x86_64.rpm xxx@xx.xx.xx.xx:/root/mysql-community-server-8.0.15-1.el7.x86_64.rpm
```

按照先后顺序依次执行`yum`本地安装：

```bash
sudo yum localinstall mysql-community-common-8.0.15-1.el7.x86_64.rpm
sudo yum localinstall mysql-community-libs-8.0.15-1.el7.x86_64.rpm
sudo yum localinstall mysql-community-client-8.0.15-1.el7.x86_64.rpm
sudo yum localinstall mysql-community-server-8.0.15-1.el7.x86_64.rpm

sudo yum -y install mysql
```

安装成功，启动并测试服务：

```bash
systemctl start mysqld.service
systemctl status mysqld.service
```

找出默认密码：

```
grep "password" /var/log/mysqld.log >> defalut_mysql_passwd.txt
```
