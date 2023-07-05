from django.http import JsonResponse
from django.shortcuts import render, redirect

from Dept import models
from Dept.utils.pagination import Pagination
from Dept.utils.bootstrap import BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt


class TaskModelFrom(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


def task_list(request):
    """ 任务列表 """
    form = TaskModelFrom()
    queryset = models.Task.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "form": form,
    }
    return render(request, "task_list.html", context)


@csrf_exempt
def task_add(request):
    """ 新建任务(Ajax) """
    form = TaskModelFrom(data=request.POST)
    if form.is_valid():
        form.save()

        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})


def task_delete(request):
    """ 删除任务 """
    uid = request.GET.get("uid")
    exists = models.Task.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})

    models.Task.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def task_detail(request):
    """ 任务 """
    uid = request.GET.get("uid")
    row_dict = models.Task.objects.filter(id=uid).values("task", "status", "user").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "编辑失败，数据不存在"})

    # 从数据库中获取对象
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def task_edit(request):
    """ 编辑任务 """
    uid = request.GET.get("uid")
    row_object = models.Task.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在，请刷新重试"})

    form = TaskModelFrom(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})
