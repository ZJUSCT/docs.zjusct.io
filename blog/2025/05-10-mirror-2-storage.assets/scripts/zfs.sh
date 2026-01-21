#!/usr/bin/env bash
set -xe

test()
{
    mkdir "$1"
    cd "$1"
    zpool status | tee zpool
    zfs create -V 100T storage/block
    fio --filename=/dev/zvol/storage/block ../mix.fio \
        --output=mix.json --output-format=json
    fio --filename=/dev/zvol/storage/block ../crystal.fio \
        --output=crystal.json --output-format=json
    zpool destroy storage
    wipefs -a /dev/sd*
}

(zpool create storage /dev/sd[a-l] /dev/sd[s-z] /dev/sda[a-j]
test raid0)
(zpool create storage raidz3 /dev/sd[a-l] /dev/sd[s-z] /dev/sda[a-j]
test raidz3-30)
(zpool create storage raidz2 /dev/sd[a-j] raidz2 /dev/sd[k-l] /dev/sd[s-z] raidz2 /dev/sda[a-j]
test raidz2-10px3)
(zpool create storage draid2:12d:30c:2s /dev/sd[a-l] /dev/sd[s-z] /dev/sda[a-j]
test draid2-12d-30c-2s)
(zpool create storage raidz3 /dev/sd[a-j] raidz3 /dev/sd[k-l] /dev/sd[s-z] raidz3 /dev/sda[a-j]
test raidz3-10px3)
(zpool create storage draid2:7d:30c:3s /dev/sd[a-l] /dev/sd[s-z] /dev/sda[a-j]
test draid2-7d-30c-3s)
(zpool create storage raidz2 /dev/sd[a-f] raidz2 /dev/sd[g-l] raidz2 /dev/sd[s-x] raidz2 /dev/sd[y-z] /dev/sda[a-d] raidz2 /dev/sda[e-j]
test raidz2-6px5)
(zpool create storage draid2:5d:30c:2s /dev/sd[a-l] /dev/sd[s-z] /dev/sda[a-j]
test draid2-5d-30c-2s)
