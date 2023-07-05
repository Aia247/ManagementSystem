from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django import forms

from Dept import models
from Dept.utils.pagination import Pagination
from Dept.utils.bootstrap import BootStrapModelForm


def pretty_list(request):
    """ 靓号列表 """

    # 数据库中获取所有靓号列表
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["mobile__contains"] = search_data
    # queryset = models.PrettyNum.objects.all().order_by("level")

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("id")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),
    }

    return render(request, "pretty_list.html", context)


# 靓号ModelForm
class PrettyModelFrom(BootStrapModelForm):
    # # 正则表达式验证手机号
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r"^1[3-9]\d{9}$", "手机号格式错误")]
    # )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"

    # 钩子方法 clean_字段
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            # 验证不通过
            raise ValidationError("手机号已存在")
        # 验证通过
        return txt_mobile


def pretty_add(request):
    """ 添加靓号 """
    if request.method == "GET":
        form = PrettyModelFrom()
        return render(request, "pretty_add.html", {"form": form})

    form = PrettyModelFrom(data=request.POST)
    # 校验成功
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")

    # 校验失败
    return render(request, "pretty_add.html", {"form": form})


def pretty_delete(request, nid):
    """ 删除靓号 """
    # 删除靓号
    models.PrettyNum.objects.filter(id=nid).delete()

    # 重定向回部门列表
    return redirect("/pretty/list/")


# 靓号编辑ModelForm
class PrettyEditModelFrom(PrettyModelFrom):
    # mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level"]


def pretty_edit(request, nid):
    """ 编辑靓号 """
    # 根据nid获取数据
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelFrom(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})

    # 获取用户POST提交的数据
    form = PrettyEditModelFrom(data=request.POST, instance=row_object)

    if form.is_valid():
        # 保存到数据库
        form.save()
        # 重定向回部门列表
        return redirect("/pretty/list/")

    return render(request, "pretty_edit.html", {"form": form})
