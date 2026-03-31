#!/usr/bin/env bash
set -xe

DEVS=(
/dev/sda
/dev/sdaa
/dev/sdab
/dev/sdac
/dev/sdad
/dev/sdae
/dev/sdaf
/dev/sdag
/dev/sdah
/dev/sdai
/dev/sdaj
/dev/sdb
/dev/sdc
/dev/sdd
/dev/sde
/dev/sdf
/dev/sdg
/dev/sdh
/dev/sdi
/dev/sdj
/dev/sdk
/dev/sdl
/dev/sds
/dev/sdt
/dev/sdu
/dev/sdv
/dev/sdw
/dev/sdx
/dev/sdy
/dev/sdz
)

RAID_DEV=/dev/md0
LEVEL=0
NUM_DEVICES=${#DEVS[@]}
CHUNK_SIZE=512K
mdadm --create --verbose $RAID_DEV \
  --level=$LEVEL \
  --raid-devices="$NUM_DEVICES" \
  --chunk=$CHUNK_SIZE \
  ${DEVS[@]}
mdadm --detail $RAID_DEV
mdadm --detail --scan

mkdir mdadm
cd mdadm || exit
fio --filename=/dev/md0 ../mix.fio \
    --output=mix.json --output-format=json
fio --filename=/dev/md0 ../crystal.fio \
    --output=crystal.json --output-format=json

mdadm --stop $RAID_DEV
wipefs -a /dev/sd*
