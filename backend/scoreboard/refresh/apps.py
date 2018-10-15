from backend.user.models import User
from backend.question.models import Solve
from django.db.models import F


def refresh(all=False, user=None, board=False):
    refresh_list = []
    if all:
        refresh_list = list(User.objects.all())
    else:
        if user is not None:
            refresh_list.append(user)
        if board:
            user_board = User.objects.all().order_by(F("score").desc())[:10]
            refresh_list += list(user_board)

    for u in refresh_list:
        score = 0
        sovle_list = Solve.objects.filter(who_solve=u)
        for s in sovle_list:
            ranking = s.get_ranking()
            score += s.which_question.get_score(rank=ranking)
        u.score = score
        u.save()
