from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # 排除不需要登录就能访问的页面
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 读取用户的session信息，如果能读到则继续
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 如果没有登录，回到登录页面
        return redirect("/login/")
