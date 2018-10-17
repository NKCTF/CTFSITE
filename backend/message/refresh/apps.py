
from backend.message.models import JoinRequest
from backend.user.models import Team


def refresh_request(team_list):
    for name in team_list:
        try:
            team = Team.objects.get(team_name=name)
            join = JoinRequest.objects.get(send_to=team)
            if join.send_by.belong is not None:
                join.delete()
        except Team.DoesNotExist:
            return 404
        except JoinRequest.DoesNotExist:
            pass
    return 0
