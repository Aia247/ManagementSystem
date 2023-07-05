from django.shortcuts import render, redirect
from django import forms

from Dept import models
from Dept.utils.pagination import Pagination
from Dept.utils.bootstrap import BootStrapModelForm
from Dept.utils.encrypt import md5


def user_list(request):
    """ 部门列表 """
    # 数据库中获取所有用户列表
    data_dict = {}
    search_data = request.GET.get("q", "")

    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.UserInfo.objects.filter(**data_dict).order_by("id")

    page_object = Pagination(request, queryset)
    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, "user_list.html", context)


# 用户ModelForm实例
class UserModelFrom(BootStrapModelForm):
    password = forms.CharField(
        min_length=3,
        label="密码",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = models.UserInfo
        # fields = ["name", "password", "age"]
        fields = "__all__"


def user_add(request):
    """ 添加用户ModelForm """
    if request.method == "GET":
        form = UserModelFrom()
        return render(request, "user_add.html", {"form": form})

    form = UserModelFrom(data=request.POST)
    # 校验成功
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    # 校验失败
    return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    """ 编辑用户 """
    # 根据nid获取数据
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModelFrom(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    # 获取用户POST提交的数据
    form = UserModelFrom(data=request.POST, instance=row_object)

    if form.is_valid():
        # 保存到数据库
        form.save()
        # 重定向回部门列表
        return redirect("/user/list/")

    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """ 删除用户 """
    # 删除用户
    models.UserInfo.objects.filter(id=nid).delete()

    # 重定向回部门列表
    return redirect("/user/list/")
