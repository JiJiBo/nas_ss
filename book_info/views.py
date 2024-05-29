from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from my_sql_db.models import SmallSay, Bgm, Voice
from utils.utils.Result import *
from utils.utils.TokenUtils import get_user_id


# Create your views here.
@csrf_exempt
def get_all_novels(request):
    """获取所有小说信息并进行分页"""
    if request.method == 'GET':
        # 查询所有小说信息
        all_novels = SmallSay.objects.all()

        # 分页
        page_number = request.GET.get('page')
        user_id = get_user_id(request)
        print(user_id)
        if user_id is not None:
            all_novels = all_novels.filter(userid=user_id)
        paginator = Paginator(all_novels, 10)  # 每页显示 10 条数据
        try:
            novels_page = paginator.page(page_number)
        except PageNotAnInteger:
            # 如果页数不是一个整数，返回第一页
            novels_page = paginator.page(1)
        except EmptyPage:
            # 如果页数超出范围，返回最后一页
            novels_page = paginator.page(paginator.num_pages)

        # 构造返回数据
        novels_data = []
        for novel in novels_page:
            novel_data = {
                'id': novel.id,
                'name': novel.name,
                'link': novel.link,
                'last_updated': novel.last_updated.strftime("%Y-%m-%d %H:%M:%S") if novel.last_updated else None,
                'background_music': novel.background_music,
                'download_progress': novel.download_progress,
                'conversion_progress': novel.conversion_progress,
                'conversion_max': novel.conversion_max,
                'download_max': novel.download_max,
                'add_back_progress': novel.add_back_progress,
                'add_back_max': novel.add_back_max,
                'voice': novel.voice,
                'time': novel.time,
                # 其他字段按需添加
            }
            novels_data.append(novel_data)

        return getOkResult({'count': paginator.count, 'results': novels_data})
    else:
        return getErrorResult('no support method')


@csrf_exempt
def get_all_bgm(request):
    if request.method == 'GET':
        # 查询所有小说信息
        all_bgm = Bgm.objects.all()

        # 构造返回数据
        bgms_data = []
        for bgm in all_bgm:
            bgm_data = {
                'id': bgm.id,
                'bgm': bgm.bgm,
                'path': bgm.path,
                'time': bgm.time,
                # 其他字段按需添加
            }
            bgms_data.append(bgm_data)

        return getOkResult({'count': len(bgms_data), 'results': bgms_data})
    else:
        return getErrorResult('no support method')


@csrf_exempt
def get_all_voice(request):
    if request.method == 'GET':
        # 查询所有小说信息
        all_voice = Voice.objects.all()

        # 构造返回数据
        voices_data = []
        for voice in all_voice:
            voice_data = {
                'id': voice.id,
                'name': voice.name,
                'value': voice.value,
                'msg': voice.msg,
                'time': voice.time,
                # 其他字段按需添加
            }
            voices_data.append(voice_data)

        return getOkResult({'count': len(voices_data), 'results': voices_data})
    else:
        return getErrorResult('no support method')
