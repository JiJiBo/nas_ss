# 后台模块

- 数据库模块
- 页面模块
- 后台任务模块
- 爬虫模块
- 用户模块

# 前端模块

- 登录页面
- 配置页面
- 小说列表
- 小说详情
- 播放列表
- 后台播放模块

# 如何开始
## 装包
```angular2html
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

```
## 迁移数据库

```angular2html
python manage.py inspectdb>./my_sql_db/models.py
```

## 如何创建数据库

- 参见 sql/sql.sql 文件

# 如何运行
```angular2html
celery  -A nas_ss flower
celery -A nas_ss worker -l info
python manage.py runserver 0.0.0.0:8000 
```


# 导出依赖

```
pip freeze > requirements.txt
```