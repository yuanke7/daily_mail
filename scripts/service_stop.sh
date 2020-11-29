#!/usr/bin/env bash

# 获取当前正在运行的 docker 容器
mapfile -t container_ids < <((docker ps -q | awk '{print $1}'))

# 停止当前所有的实例
for cid in "${container_ids[@]}"; do
   docker stop "${cid}"
  echo "Stopped container: ${cid}"
done
