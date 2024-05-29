import jwt

from nas_ss import settings


def get_user_id(request):
    token = request.headers.get('Authorization')
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = payload.get('user_id')
    return user_id
