import jwt
import datetime

from nas_ss.settings import SECRET_KEY


def create_jwtToken(openid):
    expire_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }

    payload = {
        'openid': openid,
        "exp": expire_time
    }
    result = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256', headers=headers)
    return result


def identify_token(token):
    try:
        verified_payload = jwt.decode(token, key=SECRET_KEY, algorithms="HS256")
        # 验证通过返回payload中的信息
        return verified_payload
    # 不通过返回报错
    except jwt.ExpiredSignatureError:
        print('token已失效')
        return False
    except jwt.DecodeError:
        print('token认证失败')
        return False
    except jwt.InvalidTokenError:
        print('非法的token')
        return False
