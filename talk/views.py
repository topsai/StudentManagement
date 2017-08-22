# from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from manage import models
# Create your views here.

User = get_user_model()
seller = models.Seller.objects.all()
def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('talk:user_list'))
        else:
            print(form.errors)
    return render(request, 'log_in.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect(reverse('talk:log_in'))


def user_list(request):
    # users = User.objects.select_related('logged_in_user')
    # for user in users:
    #     user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
    return render(request, 'user_list.html', {'users': seller})

from django.contrib.auth import get_user_model
# User = get_user_model()
def sign_up(request):
    form = get_user_model()
    if request.method == 'POST':
        form = get_user_model(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('talk:log_in'))
        else:
            print(form.errors)
    return render(request, 'sign_up.html', {'form': form})