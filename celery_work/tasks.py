from celery import shared_task

# 任务函数
@shared_task
def add(a, b):
    return a + b