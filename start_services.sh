#!/bin/bash

# 更新代码库
git pull

# 检查是否已经在 py310 环境中
if [[ "$CONDA_DEFAULT_ENV" != "py310" ]]; then
    # 激活 conda 环境
    source /root/miniconda3/bin/activate py310
    conda activate py310
fi

# 启动 Django 开发服务器
nohup python manage.py runserver [::]:8000 > out.log 2>&1 &

# 启动 Celery Flower
nohup celery -A nas_ss flower > outflower.log 2>&1 &

# 启动 Celery worker
nohup celery -A nas_ss worker -l info > outworker.log 2>&1 &

echo "All services started successfully."
