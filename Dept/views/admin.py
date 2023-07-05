from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from Dept import models
from Dept.utils.pagination import Pagination
from Dept.utils.bootstrap import BootStrapModelForm
from Dept.utils.encrypt import md5


def admin_list(request):
    """ 管理员列表 """
    # 数据库中获取所有管理员列表
    queryset = models.Admin.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
    }
    return render(request, "admin_list.html", context)


class AdminModelFrom(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


def admin_add(request):
    """ 添加管理员 """
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelFrom()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminModelFrom(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")

    return render(request, "change.html", {"form": form, "title": title})


class AdminEditModelFrom(BootStrapModelForm):
    # confirm_password = forms.CharField(
    #     label="确认密码",
    #     widget=forms.PasswordInput,
    # )

    class Meta:
        model = models.Admin
        fields = ["username"]
        # fields = ["username", "password", "confirm_password"]
        # widgets = {
        #     "password": forms.PasswordInput
        # }


def admin_edit(request, nid):
    """ 编辑管理员 """
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    title = "编辑管理员"

    if request.method == "GET":
        form = AdminEditModelFrom(instance=row_object)
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminEditModelFrom(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})


def admin_delete(request, nid):
    """ 删除用户 """
    # 删除用户
    models.Admin.objects.filter(id=nid).delete()

    # 重定向回部门列表
    return redirect("/admin/list/")
