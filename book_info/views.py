from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt

from my_sql_db.models import SmallSay, Bgm, Voice, Books
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


@csrf_exempt
def get_filtered_books(request):
    """根据book_id和get_step筛选书籍，并进行分页"""
    if request.method == 'GET':
        # 从请求中获取筛选参数
        book_id = request.GET.get('book_id')
        get_step = request.GET.get('get_step')

        # 创建查询基础
        query = Books.objects.all()

        # 根据book_id筛选
        if book_id is not None:
            query = query.filter(book_id=book_id)

        # 根据get_step筛选
        if get_step is not None:
            query = query.filter(get_step=get_step)
        query = query.order_by('page')
        # 分页设置
        page_number = request.GET.get('page', 1)  # 默认为第一页
        paginator = Paginator(query, 777)  # 每页显示10条数据

        try:
            books_page = paginator.page(page_number)
        except PageNotAnInteger:
            # 如果页数不是整数，返回第一页
            books_page = paginator.page(1)
        except EmptyPage:
            # 如果页数超出范围，返回最后一页
            return getErrorResult('out of range')

        # 构造返回数据
        books_data = [{'id': book.id,
                       'book_id': book.book_id,
                       'path': book.path,
                       'get_step': book.get_step,
                       'time': book.time,
                       'dir': book.dir,
                       'name': book.name,
                       } for book in books_page]

        return getOkResult({'count': paginator.count, 'results': books_data, })
    else:
        return getErrorResult('no support method')


@csrf_exempt
def get_a_voice(request):
    if request.method == 'GET':
        # 从请求中获取筛选参数
        voice_id = request.GET.get('voice_id')
        voice = Voice.objects.get(id=voice_id)
        voice_data = {
            'id': voice.id,
            'name': voice.name,
            'value': voice.value,
            'msg': voice.msg,
            'time': voice.time,
            # 其他字段按需添加
        }
        return getOkResult(voice_data)
    else:
        return getErrorResult('no support method')


@csrf_exempt
def get_a_bgm(request):
    if request.method == 'GET':
        # 从请求中获取筛选参数
        bgm_id = request.GET.get('bgm_id')
        bgm = Bgm.objects.get(id=bgm_id)
        bgm_data = {
            'id': bgm.id,
            'bgm': bgm.bgm,
            'path': bgm.path,
            'time': bgm.time,
        }
        return getOkResult(bgm_data)
    else:
        return getErrorResult('no support method')


@csrf_exempt
def get_novel(request):
    """获取小说信息"""
    if request.method == 'GET':
        try:
            novel_id = request.GET.get('novel_id')
            novel = SmallSay.objects.get(id=novel_id)
            download_progress = len(Books.objects.filter(book_id=novel.id, get_step=1))
            conversion_progress = len(Books.objects.filter(book_id=novel.id, get_step=3))
            add_back_progress = len(Books.objects.filter(book_id=novel.id, get_step=6))
            conversion_fail = len(Books.objects.filter(book_id=novel.id, get_step=4))
            add_back_fail = len(Books.objects.filter(book_id=novel.id, get_step=7))
            novel_data = {
                'id': novel.id,
                'name': novel.name,
                'link': novel.link,
                'last_updated': novel.last_updated.strftime("%Y-%m-%d %H:%M:%S") if novel.last_updated else None,
                'background_music': novel.background_music,
                'download_progress': download_progress,
                'conversion_progress': conversion_progress,
                'conversion_max': novel.conversion_max,
                'add_back_progress': add_back_progress,
                'add_back_max': novel.add_back_max,
                'download_max': novel.download_max,
                'conversion_fail': conversion_fail,
                'add_back_fail': add_back_fail,
                'background_music_id': novel.background_music_id,
                'voice_id': novel.voice_id,
                'voice': novel.voice,
                'time': novel.time,
                # 'book_datas': book_datas
            }
            return getOkResult(novel_data)
        except Exception as e:
            e = str(e)
            print(e)
            return getErrorResult(e)
    else:
        return getErrorResult('no support method')
