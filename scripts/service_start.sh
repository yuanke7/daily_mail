#!/usr/bin/env bash

# 获取当前存在的 docker 容器
mapfile -t container_ids < <((docker ps -a -q | awk '{print $1}'))

# 重新启动实例
for cid in "${container_ids[@]}"; do
  docker start "${cid}"
  echo "Started container: ${cid}"
done
