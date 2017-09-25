from django.conf import settings
from .. import models

def init_permission(request, user_obj):
    """
    初始化用户权限
    :param request: 用户的request请求
    :param user_obj:
    :return:
    """
    permission_item_list = user_obj.roles.values('permissions__title', 'permissions__url',
                                                 'permissions__menu_id').distinct()
    # 保存当前用户有权访问的URL
    permission_url_list = []

    # 保存当前用户有权访问的URL且需要在菜单上显示
    permission_menu_list = []

    for item in permission_item_list:
        permission_url_list.append(item['permissions__url'])
        if item['permissions__menu_id']:
            temp = {'title': item['permissions__title'],
                    'url': item['permissions__url'],
                    'menu_id': item['permissions__menu_id']}
            permission_menu_list.append(temp)

    # 所有菜单
    menu_list = list(models.Menu.objects.values('id','caption', 'parent_id'))
    #将权限的url列表写入
    request.session[settings.SESSION_PERMISSION_URL_KEY] = permission_url_list

    request.session[settings.SESSION_PERMISSION_MENU_URL_KEY] = {
        #将权限权限对应的菜单写入
        settings.PERMISSION_URL_KEY: permission_menu_list,
        #将全部的菜单信息写入进去
        settings.ALL_MENU_KEY: menu_list,
    }