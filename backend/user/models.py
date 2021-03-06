from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=128, default='Join our team!!')


class Career(models.Model):
    WEB = "WEB, 网络"
    PWN = "PWN, 二进制"
    Reverse = "Reverse, 逆向"
    Crypto = "Crypto, 密码学"
    MISC = "MISC, 杂项"
    Almighty = "Almighty, 万精油"

    career_name = models.CharField(max_length=16, unique=True, primary_key=True)


class User(AbstractUser):
    """从 Django 系统定义的抽象基类 AbstractUser 派生出我们自己的类"""
    auth_id = models.IntegerField(unique=True, null=True, blank=True)
    auth_type = models.CharField(max_length=16, null=True, blank=True)

    score = models.IntegerField(default=0)
    qq = models.CharField(max_length=16, null=True, blank=True)
    github = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=128, default='Welcome to NanKai CTF')

    belong = models.ForeignKey(Team, on_delete=models.SET_NULL,
                               related_name="work_for", null=True, blank=True)
    user_career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, blank=True)
    join_date = models.DateTimeField(null=True, blank=True)
    is_leader = models.BooleanField(default=False, null=True, blank=True)

    def create_team(self, team_name, team_description=None):
        if team_name is None:
            raise Exception("Please provide a team name")
        try:
            Team.objects.get(team_name=team_name)
            raise Exception("Team name has exist!")
        except Team.DoesNotExist:
            new_team = Team.objects.create(team_name=team_name,
                 description=(team_description or f"Welcome to {team_name}"))
            new_team.save()
        self.belong = new_team
        self.is_leader = True
        self.join_date = datetime.now()
        self.save()
        return new_team

    def score_detail(self):
        from backend.question.models import Solve
        solve_q = Solve.objects.filter(who_solve=self)
        ret = []
        for slv in solve_q:
            data = {
                "solve_question": slv.which_question.question_name,
                "ranking": slv.get_ranking(),
                "gain_score": slv.get_score(),
                "solve_time": slv.time.strftime("%H:%M:%S in %Y,%m,%d"),
            }
            ret.append(data)
        return ret
