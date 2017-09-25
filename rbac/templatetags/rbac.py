import re
import os
from django.template import Library#导入自定以标签模块
from django.conf import settings
from django.utils.safestring import mark_safe

register = Library()#生成对象


def process_menu_data(request):
    """
    生成菜单相关数据
    :param request:
    :return:返回一个列表菜单包含字典
    """
    menu_permission_list = request.session.get(settings.SESSION_PERMISSION_MENU_URL_KEY)#得到权限菜单和已经有的url菜单
    menu_list = menu_permission_list[settings.ALL_MENU_KEY]#获取到所有的菜单
    permission_list = menu_permission_list[settings.PERMISSION_URL_KEY]#获取全部的url列表
    all_menu_dict = {}#建立一个空子典
    for item in menu_list:#遍历这个菜单列表
        item['children'] = []#添加一个下一级键值对
        item['status'] = False#添加一个状态键值对默认为F，如果为False那么在前端可以不显示了
        item['open'] = False#添加一个open键值对代表，如果是True在前端就会展开
        all_menu_dict[item['id']] = item#通过id为key的方式添加到字典内

    for per in permission_list:#循环可以登陆了url列表
        per['status'] = True#添加字段
        pattern = settings.URL_REGEX.format(per['url'])#提取url
        if re.match(pattern, request.path_info):#如果满足正则表达式则可以登陆这个页面
            per['open'] = True#表示展开
        else:
            per['open'] = False

        all_menu_dict[per['menu_id']]['children'].append(per)#获取全部菜单获取到当前菜单的父id 为key在全部菜单内进行查找将当前per字典加入到子列表内

        pid = per['menu_id']#获取当前权限字典（per）的菜单id然后赋值给pid
        while pid:#如果有pid说明有父级id
            all_menu_dict[pid]['status'] = True#设置父级字典的状态为True这样前端就可以显示该字典
            pid = all_menu_dict[pid]['parent_id']#再次获取当前菜单字典的父级id给pid进行循环直到没有父级id

        if per['open']:#如果权限字典内的open是Ture，我们就需要将跟他有关联的所有父级的open进行True修改
            ppid = per['menu_id']#将当前权限字典的菜单id取出
            while ppid:#循环判断是否有父级菜单如果有进行
                all_menu_dict[ppid]['open'] = True#将父级的open进行打开
                ppid = all_menu_dict[ppid]['parent_id']#将ppid重现覆盖为当前的权限菜单的父级id进行再次循环直到没有父级id位置

    result = []#建立一个空的列表列表名 结果
    for k, v in all_menu_dict.items():#循环遍历最后的包含孩子字典的这个字典，和子字典
        if not v.get('parent_id'):#如果没有获取到父级字典说明是最上层的引导菜单
            result.append(v)#将引导菜单添加到结果列表内
        else:
            parent_id = v['parent_id']#获取当前字典的父级id
            all_menu_dict[parent_id]['children'].append(v)#将当前父级id的孩子点加到总列表内进行循环

    return result#返回一个没有父级id的列表


def process_menu_html(menu_list):
    '''生成html样式

    '''
    tpl1 = """
            <div class='rbac-menu-item'>
                <div class='rbac-menu-header'>{0}</div>
                <div class='rbac-menu-body {2}'>{1}</div>
            </div>
        """
    tpl2 = """
            <a href='{0}' class='{1}'>{2}</a>
        """

    html = ""

    for item in menu_list:#循环这个没有父级id的列表
        if not item['status']:#如果status是True那么返回的就是假代表这个判断内不执行，用来判断是否需要显示
            continue
        if item.get('url'):#获取url
            # 权限
            html += tpl2.format(item['url'],
            "rbac-active" if item['open'] else "",
            item['title'])#将url格式化到tpl2内
            #"rbac-active" if item['open'] else ""如果open是True那么表示需要添加rbac-active让这个标签激活
            #item['title']取到标签名子
        else:#获取不到url说明是菜单类型
            # 菜单
            html += tpl1.format(item['caption'],process_menu_html(item['children']), "" if item['open'] else "rbac-hide")
            #item['caption']取出菜单的名字
            #process_menu_html(item['children'])递归建立孩子列表
            #"" if item['open'] else "rbac-hide"如果这个菜单的open代表是Ture则显示出来
    return html

@register.simple_tag
def rbac_menus(request):
    # 数据库取到菜单相关数据
    result = process_menu_data(request)#获取到当前权限人的所有可以登陆的url和菜单以字典的形式返回
    # 生成HTML
    html = process_menu_html(result)#将获得到的可登录url和字典进行转换成html页面
    return mark_safe(html)#进行safe进行返回给html，这里就可以在前端进行使用了


@register.simple_tag
def rbac_css():#这个标签可以获取到我们存放的左侧导航的css位置
    file_path = os.path.join('rbac', 'theme', 'rbac.css')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题CSS文件不存在')


@register.simple_tag
def rbac_js():#这个标签可以获取到我们存放的左侧导航的js位置
    file_path = os.path.join('rbac', 'theme', 'rbac.js')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('rbac主题JavaScript文件不存在')