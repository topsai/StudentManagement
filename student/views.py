from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from manage import models

# Create your views here.
User = get_user_model()
users = models.Seller.objects.all().values_list('id', 'name')

# @login_required
def index(request):
    # users = User.objects.select_related('logged_in_user')
    # for user in users:
    #     user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
    # # return render(request, 'user_list.html', {'users': users})
    print(users)
    user= '1212313'
    return render(request, 'pages/student.html', {'users': users})
