# 介绍

## 项目介绍

- 基于python、diango的小说转语音 并且加背景音的服务
- 可以给小说加上想要的背景音，并支持选取读书者的声音
- 支持用户系统，支持token认证，支持后台任务

# 如何开始

## 装包

```angular2html
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 如何创建数据库

- 参见 sql/sql.sql 文件

## 迁移数据库

```angular2html
python manage.py inspectdb>./my_sql_db/models.py
```

# 如何运行

- windows

```angular2html
celery  -A nas_ss flower
celery -A nas_ss worker -l info
python manage.py runserver 0.0.0.0:8000 
```

- linux

1. 重启

```angular2html
./restart_services.sh
```

2. 开启

```angular2html
./start_services.sh
```

3. 关闭

```angular2html
./stop_services.sh
```