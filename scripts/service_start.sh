#!/usr/bin/env bash

# 获取当前存在的 docker 容器
container_ids=($(docker ps -a | awk '{print $1}'))

for cid in ${container_ids}; do
  if [ "${cid}" = "CONTAINER" ]; then
    continue
  else
    docker start "${cid}"
    echo "Started container: ${cid}"
  fi
done
