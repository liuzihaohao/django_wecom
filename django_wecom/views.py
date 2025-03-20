from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests, time
import urllib.parse
from .models import User

# 企微 access_token 获取
access_token = ""
access_token_expire = 0
def get_access_token():
    global access_token
    global access_token_expire
    if access_token_expire > time.time():
        return access_token
    res = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={settings.WECOM_CORPID}&corpsecret={settings.WECOM_SECRET}").json()
    access_token = res["access_token"]
    access_token_expire = time.time() + res["expires_in"] - 20
    return access_token

def login(request):
    """
    登陆
    """
    # 公共评价机登陆使用 token
    token = request.GET.get("token")
    if token:
        tmp = kiosk_challenge.get(token)
        if tmp:
            auth.login(request, Kiosk.objects.get(id=tmp).user)
            return redirect("/")
        else:
            raise PermissionDenied

    # 如果已经登陆 直接跳转
    if request.user.is_authenticated:
        return redirect("/")

    # 判断当前用户是否在企微里打开，如果是返回跳转认证链接，如果不是返回二维码登陆页面
    user_agent = request.META.get('HTTP_USER_AGENT')

    if "wxwork" in user_agent:
        return redirect(
            f"https://open.weixin.qq.com/connect/oauth2/authorize?appid={settings.WECOM_CORPID}\
&redirect_uri={urllib.parse.quote(settings.WECOM_redirect_uri)}&response_type=code&scope=snsapi_base&agentid={settings.WECOM_AGENTID}&state={urllib.parse.quote(request.GET.get('next', '/'))}\
#wechat_redirect" # state 中传要跳转到的页面
        )
    
    obj = locals()
    obj["WECOM_CORPID"] = settings.WECOM_CORPID
    obj["WECOM_AGENTID"] = settings.WECOM_AGENTID
    obj["WECOM_redirect_uri"] = settings.WECOM_redirect_uri

    return render(request, "ct_auth/login.html", obj)

def callback(request):
    """
    企微回调接口
    """
    # 如果已经认证 直接跳转
    if request.user.is_authenticated:
        return redirect("/")

    # 企微返回的 code
    code = request.GET.get("code",None)
    if not code:
        return HttpResponseForbidden()

    # 调用接口获取用户信息
    res = requests.get(
        url=f"https://qyapi.weixin.qq.com/cgi-bin/auth/getuserinfo?access_token={get_access_token()}&code={code}"
    ).json()
    if res["errcode"] != 0:
        return HttpResponseForbidden(res["errmsg"])
    
    userid = res["userid"]
    
    # 使用 userid 调取真实姓名
    res = requests.get(
        url=f"https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={get_access_token()}&userid={userid}"
    ).json()
    if res["errcode"] != 0:
        return HttpResponseForbidden("企微认证错误")
    realname = res["name"]
    
    # 如果不存在 在数据库中创建一条记录
    User.objects.get_or_create(
        username = userid,
        id = userid,
        real_name = realname,
    )

    # auth 模块的登陆接口
    auth.login(request, User.objects.get(id=userid))

    # 接收 state 传来要跳转的页面
    return redirect(request.GET.get('state', '/'))

@login_required
def logout(request):
    """
    登出
    """

    auth.logout(request)

    return redirect("/")

@login_required
def clearpassword(request, uid):
    """
    管理后台 清除密码
    """

    # 判断是否有权限
    if not request.user.has_perm("django_wecom.change_user"):
        raise PermissionDenied

    if uid == 1:
        messages.add_message(request, messages.ERROR, "不能清空超级管理员的密码")
        return redirect('/admin/django_wecom/user/1/change/')

    obj = User.objects.get(id=uid)
    obj.set_unusable_password() # 置空
    obj.save()
    messages.add_message(request, messages.SUCCESS, "已清除密码")

    return redirect(f'/admin/django_wecom/user/{uid}/change/')