from django.shortcuts import render,HttpResponse,redirect
from rbac import models as rbac_models
from rbac.service.init_permission import init_permission
import re

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        user_obj = rbac_models.UserInfo.objects.filter(username=user, password=pwd).first()
        if not user_obj:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            init_permission(request,user_obj)
            return redirect('/index.html')


def index(request):
    from django.conf import settings
    print(request.session[settings.SESSION_PERMISSION_URL_KEY])
    print(request.session[settings.SESSION_PERMISSION_MENU_URL_KEY])
    return HttpResponse('Index')


def test(request):
    return render(request,'test.html')



