from django.conf.urls import url,include
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^users.html$', views.users),
    url(r'^user/add.html$', views.user_add),
    url(r'^user/edit/(\d+).html$', views.user_edit),
]
