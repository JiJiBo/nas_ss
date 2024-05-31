#!/bin/bash

# 停止服务
./stop_services.sh

# 检查停止服务是否成功
if [ $? -ne 0 ]; then
  echo "停止服务失败"
  exit 1
fi

# 启动服务
./start_services.sh

# 检查启动服务是否成功
if [ $? -ne 0 ]; then
  echo "启动服务失败"
  exit 1
fi

echo "服务重启成功"

