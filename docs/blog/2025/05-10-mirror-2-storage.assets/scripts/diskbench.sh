#!/usr/bin/env bash
set -xe

wipefs -a /dev/sd*
DEVICES=(
$(ls /dev/sd*)
)

mkdir diskbench
cd diskbench
for dev in "${DEVICES[@]}"; do
    devname=$(basename "$dev")
    fio --filename="$dev" ../crystal.fio \
        --output="$devname".json --output-format=json
done
