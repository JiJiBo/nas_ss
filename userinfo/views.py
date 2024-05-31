import json

from django.views.decorators.csrf import csrf_exempt

from my_sql_db.models import User
from nas_ss import settings
from utils.utils.Result import getErrorResult, getOkResult


@csrf_exempt
def login(request):
    print(request.method)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        password = data.get('password')
        if not name or not password:
            return getErrorResult('Name and password are required')
        user = User.objects.filter(name=name).first()
        if user is None:
            return getErrorResult('User not found')
        if not user.pass_field == password:
            return getErrorResult('Incorrect password')
        import jwt
        import datetime

        # 构造header
        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        # 构造payload
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 设置有效时间为30分钟
        payload = {
            'user_id': user.id,  # 自定义用户ID
            'username': user.name,  # 自定义用户名
            'exp': expiration_time  # 有效时间为30分钟
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256', headers=headers)
        user.token = token
        user.save()
        return getOkResult({"token": token})
    else:
        return getErrorResult('Only POST method allowed')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        password = data.get('password')
        print(name, password)
        if not name or not password:
            return getErrorResult('Name and password are required')
        if User.objects.filter(name=name).exists():
            print("User already exists")
            return getErrorResult('用户已存在')
        try:
            User.objects.create_user(name=name, pass_field=password)
            print("success")
            return getOkResult('User created successfully')
        except Exception as e:
            print("error" + str(e))
            return getErrorResult(str(e))
    else:
        print("error")
        return getErrorResult('Only POST method allowed')


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        # 通常，令牌会从请求的Authorization头部中获取
        token = request.headers.get('Authorization')
        if not token:
            return getErrorResult('Token is required for logout')

        try:
            # 解码令牌以获取用户信息
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)

            # 将用户的令牌字段清空
            user.token = None
            user.save()

            return getOkResult('You have been logged out successfully')
        except jwt.ExpiredSignatureError:
            return getErrorResult('Token is expired')
        except jwt.InvalidTokenError:
            return getErrorResult('Invalid token')
        except User.DoesNotExist:
            return getErrorResult('User not found')
    else:
        return getErrorResult('Only POST method allowed')
