from django.shortcuts import render,redirect
from . import models
def users(request):

    user_list = models.UserInfo.objects.all()

    return render(request,'rbac/users.html',{'user_list':user_list})

from django.forms import ModelForm
from django.forms import widgets as wid
from django.forms import fields as fld
class UserModelForm(ModelForm):

    # use = fld.CharField()

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        # fields = ['username','nickname',]
        # exclude = ['username',]
        # error_messages = {
        #     "username": {'required':'用户名不能为空'}
        # }
        # widgets = {
        #     "username":wid.Textarea(attrs={'class':'c1'})
        # }
        # labels = {
        #     'username':'用户名'
        # }
        # help_texts = {
        #     'username': '别瞎写，瞎写打你哦'
        # }
        #
        # field_classes = {
        #     'username': fld.EmailField
        # }

    # def clean_email(self):
    #     pass
    #
    # def clean_nickname(self):
    #     pass
    #
    # def clean(self):
    #     pass

def user_add(request):
    # 现在的你# 创建Form类：
    if request.method == 'GET':
        model_form = UserModelForm()
        return render(request,'rbac/user_add.html',{'model_form':model_form})
    else:
        model_form = UserModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect('/rbac/users.html')

        return render(request, 'rbac/user_add.html', {'model_form': model_form})


def user_edit(request,pk):
    obj = models.UserInfo.objects.filter(pk=pk).first()
    if not obj:
        return redirect('/rbac/users.html')
    if request.method == 'GET':
        model_form = UserModelForm(instance=obj)
        return render(request,'rbac/user_edit.html',{'model_form':model_form})
    else:
        model_form = UserModelForm(request.POST,instance=obj)
        if model_form.is_valid():
            model_form.save()
            return redirect('/rbac/users.html')
        return render(request, 'rbac/user_edit.html', {'model_form': model_form})




