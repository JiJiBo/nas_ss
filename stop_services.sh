#!/bin/bash

# 停止 Django 开发服务器
killall -q -9 python
killall -q -9 celery

echo "All services stopped successfully."