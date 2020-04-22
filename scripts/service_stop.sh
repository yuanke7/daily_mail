#!/usr/bin/env bash

# 获取当前正在运行的 docker 容器
container_ids=($(docker ps | awk '{print $1}'))

for cid in ${container_ids}; do
  if [ "${cid}" = "CONTAINER" ]; then
    continue
  else
    docker stop "${cid}"
    echo "Stopped container: ${cid}"
  fi
done
