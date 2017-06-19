from django.shortcuts import render, HttpResponse, redirect, Http404
from manage import models
from manage.forms import user as user_forms


def lg(func):  # 验证用户登录装饰器
    def wrap(request, *args, **kwargs):
        # 如果未登陆，跳转到指定页面
        if not request.session.get("name"):
            # print("no login")
            return redirect('/login/')
        else:
            print(request.session['user_type'])
            if request.session['user_type'] != 'Manage':
                return redirect('/login/')
        return func(request, *args, **kwargs)
    return wrap


@lg
def manage(request):
    data = {}
    student_count = models.Student.objects.all().count()
    teacher_count = models.Teacher.objects.all().count()
    seller_count = models.Seller.objects.all().count()
    manage_count = models.Manage.objects.all().count()
    data['student'] = student_count
    data['teacher'] = teacher_count
    data['seller'] = seller_count
    data['manage'] = manage_count
    print(data)
    return render(request, 'pages/manage.html', data)

# class Login:
#     @staticmethod
#     def student():
#         print('login student')
#
#     @staticmethod
#     def teacher():
#         print('login teacher')
#
#     @staticmethod
#     def seller():
#         print('login seller')
#
#     @staticmethod
#     def admin():
#         print('login admin')


def index(request):
    return render(request, 'pages/index.html')


def login(request):
    # if request.method == 'GET':
    #     obj = model_form.LoginMF()
    #     return render(request, 'login.html', {'obj': obj})
    # elif request.method == 'POST':
    #     obj = model_form.LoginMF(request.POST)
    #     if obj.is_valid():
    #         data = models.UserInfo.objects.filter(**obj.cleaned_data).first()
    #         if data:
    #             print(data.name, data.user_type)
    #             request.session['name'] = data.name
    #             request.session['id'] = data.id
    #             request.session['user_type'] = data.user_type
    #             return redirect('/index/')
    #         else:
    #             print('err')
    #     else:
    #         print(obj.errors)
    #     return render(request, 'login.html', {'obj': obj, 'status': '用户名或密码错误'})
    # try:
    #     a = getattr(Login, w)
    # except:
    #     pass
    if request.method == 'GET':
        u = request.GET.get('u')

        if u == 'Student':
            p = '学生'
        elif u == 'Teacher':
            p = '老师'
        elif u == 'Seller':
            p = '销售'
        elif u == 'Manage':
            p = '管理员'
        else:
            u = 'Student'
            p = '学生'
        obj = user_forms.login_form({'u': u})
        return render(request, 'pages/login.html', {'obj': obj, 'p': p})
    elif request.method == 'POST':
        obj = user_forms.login_form(request.POST)
        if obj.is_valid():
            u = obj.cleaned_data.pop('u')
            try:
                data = getattr(models, u).objects.filter(**obj.cleaned_data).first()
                # print(obj.cleaned_data, data, getattr(models, u))
                if data:
                    print(data.name)
                    request.session['name'] = data.name
                    request.session['id'] = data.id
                    request.session['user_type'] = u
                    return redirect('/{}/'.format(u))
                else:
                    return render(request, 'pages/login.html', {'obj': obj, 'status': '用户名或密码错误'})
            except:
                return HttpResponse('err')
        else:
            data = obj.errors
            print('errors', data)


def regist(request):
    if request.method == 'GET':
        mf = user_forms.regist_form()
        return render(request, 'pages/regist.html', {'obj': mf})
    elif request.method == 'POST':
        mf = user_forms.regist_form(request.POST)
        if mf.is_valid():
            print(mf.cleaned_data)
            models.Student.objects.create(**mf.cleaned_data)
            obj = user_forms.login_form({'u': 'Student'})
            return render(request, 'pages/login.html', {'obj': obj, 'p': '学生', 'status': '注册成功,请登录。'})
        else:
            print(mf.errors)
            return render(request, 'pages/regist.html', {'obj': mf})


def students(request):
    print('students ')
    obj = models.Student.objects.all()
    return render(request, 'pages/tables.html', {'obj': obj})


def logout(request):
    request.session.clear()
    return redirect('/')
