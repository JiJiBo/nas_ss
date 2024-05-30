import jwt
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime, timedelta

from my_sql_db.models import User


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        EXCLUDED_FUNCTIONS = ['/login', '/register']
        print(request.path)
        if not any(request.path.startswith(func) for func in EXCLUDED_FUNCTIONS):
            token = request.headers.get('Authorization')
            if token:
                try:
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                    user_id = payload.get('user_id')
                    user = User.objects.get(id=user_id)
                    request.user = user
                except jwt.ExpiredSignatureError:
                    # 刷新过期的令牌
                    try:
                        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'],
                                             options={'verify_exp': False})
                        user_id = payload.get('user_id')
                        user = User.objects.get(id=user_id)
                        exp = datetime.utcnow() + timedelta(minutes=30)  # 设置新的过期时间
                        new_payload = {
                            'user_id': user.id,
                            'username': user.username,
                            'exp': exp
                        }
                        new_token = jwt.encode(payload=new_payload, key=settings.SECRET_KEY, algorithm='HS256').decode(
                            'utf-8')
                        user.token = new_token
                        user.save()
                        request.user = user
                        return self.get_response(request)
                    except:
                        return JsonResponse({'error': 'Token is expired and cannot be refreshed'}, status=401)
                except jwt.InvalidTokenError:
                    return JsonResponse({'error': 'Invalid token'}, status=401)
            else:
                return JsonResponse({'error': 'Token is missing'}, status=401)

        response = self.get_response(request)
        return response