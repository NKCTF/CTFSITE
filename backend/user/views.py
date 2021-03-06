from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from base64 import b64decode

# TODO: 导入用于第三方登录的一些包
from random import choice as random_choice
from requests import post as send_post, get as send_get
from urllib.parse import quote as url_quote

from .models import User
# TODO: 导入用于导入 secret_key 的环境变量
from .config import *
from os import environ as environ_var

# TODO: 导入检查密码和用户名的包
import backend.user.check.views as check


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class Login(View):
    ret_dict = {
        0: {"code": 0, "msg": "登录成功"},
        1: {"code": 1, "msg": "用户名或密码错误"},
        10: {"code": 10, "msg": "检测到攻击"},
    }

    def get(self, request):
        return JsonResponseZh(self.ret_dict[10])

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponseZh(self.ret_dict[0])
        else:
            return JsonResponseZh(self.ret_dict[1])


@method_decorator(csrf_exempt, name="dispatch")
class AuthLogin(View):
    client_id = "70e981bf5cf61e2d59ac"
    # TODO: 此处 secret_key 不应该放在发行版开源
    client_secret = environ_var.get("github_client_secret")
    token_host = {
        "github": "https://github.com/login/oauth/access_token",
    }
    api_host = {
        "github": "https://api.github.com/user",
    }
    access_token = token_type = error = message_type = None
    auth_id = username = email = None

    def render_context(self, code):
        """通过 code 返回一个渲染的参数列表"""
        return {
            0: {
                "type": self.message_type,
                "code": 0,
                "msg": "验证登录成功",
                "username": self.username,
                "email": self.email,
            },
            1: {
                "type": self.message_type,
                "code": 1,
                "msg": "发生错误",
                "error": self.error,
            },
            10: {
                "code": 10,
                "msg": "检测到攻击",
            }
        }[code]

    def get_token(self, request):
        """从第三方服务提供方获得 token"""
        code = request.GET.get("code")
        redirect = b64decode(request.GET.get('redirect')).decode('utf-8')
        # TODO: consume the state, if not present, don't proceed
        state = request.GET.get("state")
        post_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": redirect,
            "state": state, "code": code,
        }
        data = send_post(f"{self.token_host['github']}",
                         json=post_data, headers={"accept": "application/json"}).json()
        self.access_token = data.get("access_token")
        self.token_type = data.get("token_type")
        self.error = data.get("error")
        pass

    def get_user_msg(self):
        """根据得到的 token 获取用户的信息"""
        headers = {
            'Accept': 'application/json',
            'Authorization': f'token {self.access_token}'
        }
        response = send_get(self.api_host["github"], headers=headers)
        data = response.json()
        self.auth_id = data.get("id")
        self.username = data.get("login")
        self.email = data.get("email") or "not_open@github.com"

    def get(self, request):
        self.message_type = request.GET.get('type')
        self.get_token(request)
        self.get_user_msg()
        if self.error is not None:
            # TODO: 若果返回了错误,则渲染错误界面
            return render(request, "auth/result.html", self.render_context(1))
        try:
            # TODO: 根据 auth_id 查找用户, 如果存在直接登录用户
            user = User.objects.get(auth_id=self.auth_id, auth_type=self.token_type)
            login(request, user)
        except User.DoesNotExist:
            # TODO: 如果用户不存在, 穷举找到一个合法的用户名插入数据库, 并登录用户
            try:
                User.objects.get(username=self.username)
                number = 0
                while True:
                    User.objects.get(username=self.username + str(number))
                    number = number + 1
            except User.DoesNotExist:
                newer = User(username=self.username, email=self.email,
                             auth_id=self.auth_id, auth_type=self.token_type)
                newer.save()
                login(request, newer)
        # TODO: 渲染成功界面
        return render(request, "auth/result.html", self.render_context(0))

    def post(self, request):
        return render(request, "auth/result.html", self.render_context(10))


@method_decorator(csrf_exempt, name="dispatch")
class Signup(View):
    ret_dict = {
        0: {"code": 0, "msg": "注册成功"},
        1: {"code": 1, "msg": "用户名或密码不合法"},
        10: {"code": 10, "msg": "检测到攻击"},
    }
    username = password = code = None

    def is_valid(self):
        u_check = check.Username(username=self.username)
        p_check = check.Password(username=self.username, password=self.password)
        return (u_check.check() == 0) and (p_check.check() == 0)

    def get(self, request):
        """如果是 get 方式请求，会调用这个函数"""
        return JsonResponseZh(self.ret_dict[10])

    def post(self, request):
        """如果是 post 方式请求，会调用这个函数"""
        self.username = request.POST.get("username")
        self.password = request.POST.get("password")
        if self.is_valid():
            newer = User.objects.create(username=self.username)
            newer.set_password(self.password)
            newer.save()
            # TODO: 注册成功后登录用户
            login(request, newer)
            self.code = 0
        else:
            self.code = 1
        return JsonResponseZh(self.ret_dict[self.code])


def user_auth_in(request):
    host = request.META.get('HTTP_HOST')
    message_type = request.GET.get('type')
    # TODO: generate a state
    state = 'safe_string'
    location_host = 'https://github.com/login/oauth/authorize'
    client_id = '70e981bf5cf61e2d59ac'
    return HttpResponse(
        f"<script>"
        f"const url = new URL('auth_back', "
        f"    window.location.href.replace(/\?.+$/, '').replace(/\/$/, ''));"
        f"const keys = new URL(window.location.href).searchParams;"
        f"for (let k of keys) {{"
        f"  url.searchParams.append(...k);"
        f"}}"
        f"const uri = url.href;"
        f"url.searchParams.append('redirect', btoa(uri));"
        f"const redirect = encodeURIComponent(url.href);"
        f"setTimeout(function() {{"
        f"  document.location = `{location_host}?client_id={client_id}&redirect_uri=${{redirect}}&type={message_type}&state={state}&allow_signup=false`;"
        f"}}, 100);"
        f"</script>"
    )


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponseZh({"code": 0, "msg": "注销成功"})
    else:
        return JsonResponseZh({"code": 401, "msg": "用户未登录"})
