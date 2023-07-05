from io import BytesIO

from django.shortcuts import render, redirect, HttpResponse
from django import forms

from Dept import models
from Dept.utils.bootstrap import BootStrapForm
from Dept.utils.encrypt import md5
from Dept.utils.code import check_code


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        error_messages={'required': "用户名不能为空"},
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        error_messages={'required': "密码不能为空"},
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        error_messages={'required': "验证码不能为空"},
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """ 登录 """

    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)

    if form.is_valid():
        # 验证码校验
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})

        # 用户名、密码校验
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()

        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})

        del request.session["image_code"]
        request.session["info"] = {"id": admin_object.id, "name": admin_object.username}
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/admin/list/")

    return render(request, "login.html", {"form": form})


def image_code(request):
    """ 生成图像验证码 """
    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 验证码写入session中，验证时获取
    request.session["image_code"] = code_string
    # 60s超时
    request.session.set_expiry(60)

    # 内存中存入图片
    stream = BytesIO()
    img.save(stream, "png")
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect("/login/")
