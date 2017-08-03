from django.shortcuts import render, HttpResponse, reverse, redirect
from myadmin import myadm
from myadmin.create_modelform import create_modelforms
from myadmin import models
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    return render(request, 'myadmin/index.html', {'obj': myadm.registry})


def table_obj(request, app_name, table_name):
    # 表管理
    obj = myadm.registry[app_name][table_name]
    # 处理前端提交的action
    if request.method == "POST":
        action = request.POST.get('action')
        selected_action = request.POST.getlist('selected_action')
        # 判断用户选择状态
        if all([action, selected_action]):
            act = obj.get_action().get(action)
            # 防止用户篡改前端
            if act:
                queryset = obj.model.objects.filter(id__in=selected_action)
                # 执行action
                act(obj, request, queryset)
            else:
                messages.error(request, "action not find")
        else:
            if not action:
                messages.error(request, "action not selected")
            if not selected_action:
                messages.error(request, "{} not selected".format(obj.model._meta.verbose_name_plural))

    # 前端的排序
    o = request.GET.get('o')
    if o:
        data = obj.model.objects.order_by(o)
    else:
        # Model 中的排序
        if obj.ordering:
            data = obj.model.objects.order_by(*obj.ordering)
        else:
            data = obj.model.objects.all()
    # 分页
    paginator = Paginator(data, 1)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'myadmin/manage.html',
                  {'obj': myadm.registry[app_name][table_name], 'o': o, 'data': data, 'contacts': contacts})


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
