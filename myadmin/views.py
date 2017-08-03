from django.shortcuts import render, HttpResponse, reverse, redirect
from myadmin import myadm
from myadmin.myadm import create_modelforms
from myadmin import models
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    return render(request, 'myadmin/index.html', {'obj': myadm.registry})


def table_obj(request, app_name, table_name):
    print(request.method)
    print('-----------')
    print(request.GET)
    print(request.POST)
    print('-----------')
    # 表管理
    o = None
    obj = myadm.registry[app_name][table_name]
    # 处理action
    if request.method == "GET":

        o = request.GET.get('o')
        # Model 中的排序
        if obj.ordering:
            ret = obj.model.objects.order_by(*obj.ordering)
        else:
            ret = obj.model.objects.all()

    if request.method == "POST":
        action = request.POST.get('action')
        selected_action = request.POST.getlist('selected_action')
        if all([action, selected_action]):
            act = obj.get_action().get(action)
            if act:
                queryset = obj.model.objects.filter(id__in=selected_action)
                act(obj, request, queryset)
            else:
                messages.error(request, "action not find")
        else:
            if not action:
                messages.error(request, "action not selected")
            if not selected_action:
                messages.error(request, "{} not selected".format(obj.model._meta.verbose_name_plural))
    return render(request, 'myadmin/manage.html', {'obj': myadm.registry[app_name][table_name], 'o': o})


def table_obj_add(request, app_name, table_name):
    obj = myadm.registry[app_name][table_name]
    mf = create_modelforms(request, obj)
    if request.method == "POST":
        mf_obj = mf(request.POST)
        if mf_obj.is_valid():
            mf_obj.save()
            messages.info(request, "添加{}成功。".format(obj.model._meta.verbose_name_plural))
        return redirect(reverse('table_obj', args=[app_name, table_name]))
    mf_obj = mf()
    return render(request, 'myadmin/add.html', {'obj': mf_obj})


def table_obj_change(request, app_name, table_name, id):
    # 更改
    obj = myadm.registry[app_name][table_name]
    mf = create_modelforms(request, obj)
    data = mf(instance=obj.model.objects.get(id=id))
    return render(request, 'myadmin/change.html', {'obj': data})


def table_obj_change_delte(request, app_name, table_name, ids):
    data = myadm.registry[app_name][table_name].model.objects.filter(id__in=ids)
    if request.method == "DELETE":
        print('delete', data)
        ret = data.delete()
        print(ret)
        messages.info(request, '删除成功')
        return HttpResponse(reverse('table_obj', args=[app_name, table_name]))

    return render(request, 'myadmin/delete.html', {'obj': data})


def app_obj(request, app_name):
    return render(request, 'myadmin/app.html', )
