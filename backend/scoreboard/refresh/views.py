from django.http import JsonResponse
from django.views import View

from backend.user.models import User
from . import apps


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


attack_msg = {
    "code": 10,
    "msg": "检测到攻击",
}


class rAll(View):
    def get(self, request):
        try:
            apps.refresh(all=True)
            return JsonResponseZh({
                "code": 0,
                "msg": "刷新全体分数成功",
            })
        except Exception as e:
            return JsonResponseZh({
                "code": 1,
                "msg": "刷新全体分数失败",
                "error": str(e),
            })

    def post(self, request):
        return JsonResponseZh(attack_msg)


class rUser(View):
    error_msg = {
        "code": 1,
        "msg": "刷新用户分数失败",
    }
    success_msg = {
        "code": 0,
        "msg": "刷新用户分数成功",
    }

    def get(self, request):
        username = request.GET.get("username")
        if username is None:
            self.error_msg["error"] = "请提供一个需要刷新的用户名"
            return JsonResponseZh(self.error_msg)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.error_msg["error"] = "需要刷新的用户名不存在"
            return JsonResponseZh(self.error_msg)

        try:
            apps.refresh(user=user)
            return JsonResponseZh(self.success_msg)
        except Exception as e:
            self.error_msg["error"] = str(e)
            return JsonResponseZh(self.error_msg)

    def post(self, request):
        return JsonResponseZh(attack_msg)


class rBoard(View):
    def get(self, request):
        try:
            apps.refresh(board=True)
            return JsonResponseZh({
                "code": 0,
                "msg": "刷新排行榜分数成功",
            })
        except Exception as e:
            return JsonResponseZh({
                "code": 1,
                "msg": "刷新排行榜分数失败",
                "error": str(e),
            })

    def post(self, request):
        return JsonResponseZh(attack_msg)