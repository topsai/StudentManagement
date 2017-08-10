from django.shortcuts import render, HttpResponse, redirect, Http404, reverse
from manage import models
from manage.forms import user as user_forms
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user, get_user_model
from django.contrib.auth import logout as logout_user
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.core.serializers import serialize
from django.db.models import Q

User = get_user_model()


def lg(func):  # 验证用户登录装饰器
    def wrap(request, *args, **kwargs):
        # 如果未登陆，跳转到指定页面
        if not request.session.get("name"):
            # print("no login")
            return redirect('/login/')
        else:
            # print(request.session['user_type'])
            if request.session['user_type'] != 'Manage':
                return redirect('/login/')
        return func(request, *args, **kwargs)
    return wrap


@login_required
@permission_required('group.can_add', raise_exception=True)
def manage(request):
    data = models.User.objects.values_list('user_type__name').annotate(count=Count('user_type'))
    # data['student'] = student_count
    # data['teacher'] = teacher_count
    # data['seller'] = seller_count
    # data['manage'] = manage_count
    print(dict(list(data)))
    return render(request, 'pages/manage.html', {'data': dict(list(data))})


def index(request):
    return redirect('/{}/'.format(request.user.user_type.path))


def login(request):
    print('login')
    if request.method == 'GET':
        form = AuthenticationForm()

    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login_user(request, form.get_user())
            # print(form.get_user(), type(form.get_user()))
            if '?next='in request.get_full_path():
                return redirect('{}'.format(request.get_full_path().lstrip('/login/?next=')))
            else:
                return redirect('/my/')
        else:
            print(form.errors)
    else:
        return Http404
    return render(request, 'pages/login.html', {'obj': form})



def regist(request):
    form = user_forms.MyUserCreationForm()
    if request.method == 'POST':
        form = user_forms.MyUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('log_in'))
        else:
            print(form.errors)
    return render(request, 'pages/regist.html', {'obj': form})


@login_required
def talk(request):
    data = models.Talk.objects.filter(
        Q(send=request.user, receive_id=request.GET.get('id')) | Q(send=request.GET.get('id'), receive_id=request.user)
    ).order_by('time')
    return render(request, 'index.html', {'data': data})


def students(request):
    print('students ')
    obj = models.User.objects.filter(user_type=1).all()
    return render(request, 'pages/tables.html', {'obj': obj})


def logout(request):
    logout_user(request)
    return redirect('/login/')


