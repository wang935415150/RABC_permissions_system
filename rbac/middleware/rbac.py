import re
from django.shortcuts import redirect,HttpResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
class RbacMiddleware(MiddlewareMixin):
    '''
    这个中间件负责对人员所在的角色的权限的判定，和白名单生成功能
    '''
    def process_request(self,request):
        '''
        request函数放在中间件的最后一个位置，在最后一层做权限监听判定。
        :param request: 接收request.session
        :return: None
        '''
        for url in settings.PASS_URL_LIST: #遍历白名单，如果满足白名单正则，那么直接跳出中间件
            if re.match(url,request.path_info):
                return None
        permission_url_list = request.session.get(settings.SESSION_PERMISSION_URL_KEY)#从session中提取权限列表
        if not permission_url_list: #如果列表为空那么直接返回登陆
            return redirect(settings.LOGIN_URL)
        flag = False#建立一个标志默认False
        for db_url in permission_url_list:#循环遍历权限列表
            pattern = settings.URL_REGEX.format(db_url)#调用settings中的基本格式，将当前url格式化进去
            if re.match(pattern,request.path_info):#判断满足正则表达式
                flag = True#修改标志位
                break#推出循环
        if not flag:#如果不满足那么
            if settings.DEBUG:#判断当前是否实在开发环境下
                url_html = "<br/>".join(permission_url_list)#如果是返回可以进入的页面的url
                return HttpResponse('无权访问: %s' %url_html)
            else:
                return HttpResponse('无权访问')#如果不是开发环境直接提示无权