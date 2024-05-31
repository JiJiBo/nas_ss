import datetime

import pytz
from asgiref.sync import sync_to_async
from django.db import connection, transaction
from django.core.cache import cache

from my_sql_db.models import Books, SmallSay


@sync_to_async
def haveThisBookTitle(data):
    # 清除缓存
    cache.clear()

    # 解包数据
    small_say, name, get_step = data
    # 确认数据已经写入数据库
    connection.ensure_connection()

    with transaction.atomic():
        # 设置事务隔离级别为 READ COMMITTED
        with connection.cursor() as cursor:
            cursor.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")

        # 查询最新的数据
        titles = Books.objects.filter(book_id=small_say.id, name=name, get_step=get_step)

    # 打印调试信息

    # 返回查询结果
    return len(titles) > 0


# get_step 0 未下载，1 下载完成 2 转换完成 ,3 下载失败 4 转换失败 ,5 加背景成功 6 加背景失败
@sync_to_async
def saveBookMsg(data):
    path, small_say, get_step, dir, name, man_uuid, page = data
    # 获取当前时间,用中国上海时区
    now = datetime.datetime.now()
    # 获取系统时区
    local_tz = pytz.timezone('Asia/Shanghai')
    name = name
    # 将当前时间转换为系统时区时间
    local_time = now.astimezone(local_tz)
    local_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    small_say.last_updated = local_time
    books = Books.objects.filter(man_uuid=man_uuid)
    if len(books) == 0:
        Books.objects.create(path=path, book_id=small_say.id, name=name, get_step=get_step, dir=dir, time=local_time,
                             page=page, man_uuid=man_uuid)
    else:
        book = books[0]
        book.path = path
        book.name = name
        book.dir = dir
        book.man_uuid = man_uuid
        book.time = local_time
        book.get_step = get_step
        book.book_id = small_say.id
        book.page = page
        book.save()
    if get_step == 1:
        print(name, "download_progress", "+1")
        small_say.download_progress += 1

        small_say.save()
    elif get_step == 3:
        print(name, "conversion_progress", "+1")
        small_say.conversion_progress += 1
        small_say.save()
    elif get_step == 6:
        print(name, "add_back_progress", "+1")
        small_say.add_back_progress += 1
        small_say.save()
@sync_to_async
def get_small_say(id):
    return SmallSay.objects.get(id=id)