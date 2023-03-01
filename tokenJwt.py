import jwt
import datetime


# 构造header
headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}

SALT = "o7l8_t9bf"

def create_token(user, password):
    """
    生成jwt
    :param user: user
    :param password: password
    :return: token
    """
    # 构造payload
    payload = {
        'user': user,
        'password': password,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 超时时间
    }
    result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
    return result



def verify_jwt(token, secret=SALT):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.exceptions.ExpiredSignatureError:  # 'token已失效'
        return 1
    except jwt.DecodeError:  # 'token认证失败'
        return 2
    except jwt.InvalidTokenError:  # '非法的token'
        return 3
