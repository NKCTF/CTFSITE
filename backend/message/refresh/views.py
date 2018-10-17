from django.http import JsonResponse
from backend.user.models import User, Team
from . import apps


def JsonResponseZh(json_data):
    """
    因为返回含中文的 Json 数据总是需要设置 {'ensure_ascii': False}，所以直接在此集成
    :param json_data: 需要返回的数据
    """
    return JsonResponse(json_data, json_dumps_params={'ensure_ascii': False})


def refresh_team(request):
    if not request.user.is_authenticated:
        return JsonResponseZh({
            "code": 403,
            "msg": "未授权用户",
        })

    team_name = request.GET.get("team_name")
    if team_name is None:
        return JsonResponseZh({
            "code": 1,
            "msg": "参数错误",
            "error": "未提供 team_name 参数"
        })

    ret_code = apps.refresh_request([team_name])
    if ret_code == 0:
        return JsonResponseZh({
            "code": 0,
            "msg": "刷新成功"
        })
    elif ret_code == 404:
        return JsonResponseZh({
            "code": 404,
            "msg": "给定战队不存在",
        })