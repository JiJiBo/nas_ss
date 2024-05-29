from django.http import HttpResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

from utils.utils.Result import getErrorResult
from utils.utils.jwt import identify_token


class CheckFunctionMiddleware(MiddlewareMixin):
    # 如果所有的视图函数都要检验token，那login界面也会无法触发，所以有部分函数是可以不需要验证token的
    # 把这些函数的名字写在排除表中即可
    # 如果函数是 def func（request）：，在表中写func即可
    EXCLUDED_FUNCTIONS = ['login', 'register']

    # 这个函数在所有视图函数之前被触发，用来检验token的合法性刚好
    def process_request(self, request):
        jwtToken = request.META['NAS_TOKEN']
        # 获取函数的名称
        path = request.path
        match = resolve(path)
        request_name = match.func.__name__
        # 如果不在排除表中则触发
        if request_name not in self.EXCLUDED_FUNCTIONS:
            print("this func is not in the middleware dict")
            res = identify_token(jwtToken)
            # 检验不通过则返回错误
            if not res:
                return getErrorResult("please login", code=400)
