import json

from django.http import JsonResponse
from django.views import View
from backend.user.models import User, Team, Career
from backend.question.models import Solve
from django.db.models import F, FloatField, Sum, Count


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


# Create your views here.
class UserScore(View):
    board = data = code = None

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "用户排名查询成功",
                "data": self.data},
            1: {"code": 1, "msg": "用户查询结果为空"},
            10: {"code": 10, "msg": "检测到攻击"},
            401: {"code": 401, "msg": "未授权用户"},
        }[self.code]

    def query_user(self):
        # TODO: board 是一个 QuerySet 类型的数据，其类似于一个 list
        self.board = User.objects.all().order_by(F("score").desc()).\
            values("username", "score", "user_career", "belong")
        # TODO; key 即列表的键，value 即为一个 query 出来的字典
        self.data = [{k: ((Team.objects.get(id=v).team_name if v is not None else "HAVEN'T JOIN YET.")
                     # TODO: 将战队的 id 替换成为 name 指示战队名称
                     if k == "belong" else v) for k, v in value.items()}
                     for key, value in enumerate(self.board) if key < 10]
                     # TODO: if 条件决定返回数据量小于十个
        return 0 if self.data is not [] else 1

    def get(self, request):
        if not request.user.is_authenticated:
            self.code = 401
            return JsonResponseZh(self.get_ret_dict())
        self.code = self.query_user()
        return JsonResponseZh(self.get_ret_dict())

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())


class TeamScore(View):
    board = code = None
    data = []

    def get_ret_dict(self):
        return {
            0: {"code": 0, "msg": "战队排名查询成功",
                "data": self.data},
            1: {"code": 1, "msg": "战队查询结果为空"},
            10: {"code": 10, "msg": "检测到攻击"},
            401: {"code": 401, "msg": "未授权用户"},
        }[self.code]

    def query_team(self):
        self.data = []
        # TODO: board 是一个 QuerySet 类型的数据，其类似于一个 list
        self.board = User.objects.values("belong").\
            annotate(score=Sum("score"), members=Count("belong")).\
            order_by(F("score").desc())
        # TODO; key 即列表的键，value 即为一个 query 出来的字典
        for show_team in self.board:
            if show_team["belong"] is None:
                continue
            # TODO: 将战队的 id 替换成为 name 指示战队名称
            show_team["team_name"] = Team.objects.get(id=show_team["belong"]).team_name
            # TODO: 将 belong 属性名替换为 team_name 属性名
            del show_team["belong"]
            self.data.append(show_team)
            # TODO: if 条件决定返回数据量小于十个
            if len(self.data) >= 10:
                break
        return 0 if self.data is not [] else 1

    def get(self, request):
        if not request.user.is_authenticated:
            self.code = 401
            return JsonResponseZh(self.get_ret_dict())
        self.code = self.query_team()
        return JsonResponseZh(self.get_ret_dict())

    def post(self, request):
        self.code = 10
        return JsonResponseZh(self.get_ret_dict())


def refresh_board(request):
    try:
        user_board = User.objects.all().order_by(F("score").desc())[:10]
        for user in user_board:
            score = 0
            sovle_list = Solve.objects.filter(who_solve=user)
            for sovle in sovle_list:
                ranking = sovle.get_ranking()
                score += sovle.which_question.get_score(rank=ranking)
            user.score = score
        return JsonResponseZh({
            "code": 0,
            "msg": "刷新成功",
        })
    except Exception as e:
        return JsonResponseZh({
            "code": 1,
            "msg": "刷新失败",
            "error": str(e),
        })
    