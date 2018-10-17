from django.http import JsonResponse
from django.views import View
from backend.user.models import Team, User
from backend.message.models import JoinRequest


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


class UserInformation(View):
    code = data = crt_user = None

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "获取信息成功",
                "data": self.data},
            10: {"code": 10, "msg": "检测到攻击"},
            401: {"code": 401, "msg": "未授权用户"},
        }[self.code]

    def get_user_msg(self):
        self.data = {
            "username": self.crt_user.username,
            "email": self.crt_user.email,
            "score": self.crt_user.score,
            "qq": self.crt_user.qq,
            "github": self.crt_user.github,
            "description": self.crt_user.description,
            "user_career": getattr(self.crt_user.user_career, 'career_name', None),
            # TODO: apply_for -> JoinRequest 所有邮件中当前用户发出，目标战队的名称
            "apply_for": [it.send_to.team_name for it in
                          JoinRequest.objects.filter(send_by=self.crt_user)],
        }
        return 0

    def get(self, request):
        if not request.user.is_authenticated:
            self.code = 401
            return JsonResponseZh(self.get_ret_dict())
        self.crt_user = request.user
        self.code = self.get_user_msg()
        return JsonResponseZh(self.get_ret_dict())

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())


class TeamInformation(View):
    code = crt_user = t_obj = None
    data = {}
    ret_dict = {
        0: {"code": 0, "msg": "获取信息成功"},
        1: {"code": 1, "msg": "您尚未加入战队"},
        10: {"code": 10, "msg": "检测到攻击"},
        401: {"code": 401, "msg": "未授权用户"},
    }

    def get_team_msg(self):
        self.t_obj = self.crt_user.belong
        if self.t_obj is None: return 1
        self.data["team_name"] = getattr(self.t_obj, "team_name", None)
        self.data["team_description"] = getattr(self.t_obj, "team_description", None)
        self.data["join_date"] = self.crt_user.join_date.strftime("%H:%M:%S in %Y,%m,%d") \
            if self.crt_user.join_date is not None else None
        self.data["is_leader"] = getattr(self.crt_user, "is_leader", None)

        self.data["members"] = [it.username for it in User.objects.filter(belong=self.t_obj)]
        reqeust_list = JoinRequest.objects.filter(send_to=self.t_obj).\
            values("title", "content", "send_time", "send_by")
        for it in reqeust_list:
            it["send_by"] = User.objects.get(id=it["send_by"]).username
            it["send_time"] = it["send_time"].strftime("%H:%M:%S in %Y,%m,%d")
        self.data["application"] = list(reqeust_list)
        self.ret_dict[0]["data"] = self.data
        return 0

    def get(self, request):
        if not request.user.is_authenticated:
            self.code = 401
            return JsonResponseZh(self.ret_dict[self.code])
        self.crt_user = request.user
        self.code = self.get_team_msg()
        return JsonResponseZh(self.ret_dict[self.code])

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.ret_dict[self.code])

