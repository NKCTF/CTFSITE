from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from backend.user.models import User


class Tag(models.Model):
    WEB = "WEB",
    PWN = "PWN",
    Reverse = "Reverse"
    Crypto = "Crypto"
    MISC = "MISC"

    tag_name = models.CharField(max_length=8, unique=True, primary_key=True)


# Create your models here.
class Question(models.Model):
    question_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256)
    link = models.CharField(max_length=256, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)

    init_score = models.IntegerField(default=200)
    # TODO: arg_p 是一个控制分数计算的概率参数
    # TODO: arg_p 属于 [0,1]，默认值是 0.6
    # TODO: arg_p 越小，分数极差越大，第一个解出题目的人最终得分越高
    arg_p = models.FloatField(
        default=0.85,
        help_text=u"p 表示，当题目被第二个人做出时， 第一名分数下降到的高度。默认值 0.85"
    )
    solve_by = models.ManyToManyField(User, through="Solve")
    flag = models.CharField(max_length=512)

    def set_flag(self, text_flag):
        self.flag = text_flag

    def check_flag(self, text_flag):
        return self.flag == text_flag

    def get_score(self, rank=None):
        n = self.solve_by.count()
        p = self.arg_p
        from math import log
        c = -log(1+p, p)
        n = (n+1) if rank is None else n
        k = n if rank is None else rank
        curscore = ( ((p ** (k-1)) * (1 - p**c))/(1 - p ** (c + n - 1)) )*self.init_score
        return int(curscore)

    def __str__(self):
        return self.question_name + " of " + self.question_tag.tag_name


class Solve(models.Model):
    who_solve = models.ForeignKey(User, on_delete=models.CASCADE)
    which_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def get_ranking(self):
        ranking = Solve.objects.filter(which_question=self.which_question,
                                       time__lte=self.time).count()
        return ranking

    def get_score(self):
        return self.which_question.get_score(rank=self.get_ranking())

    def save(self, *args, **kwargs):
        user = self.who_solve
        user.score += self.which_question.get_score()
        user.save()
        super(Solve, self).save(*args, **kwargs)

    def remove(self, *args, **kwargs):
        user = self.who_solve
        user.score -= self.which_question.get_score()
        user.save()
        super(Solve, self).save(*args, **kwargs)

    class Meta:
        unique_together = ["who_solve", "which_question"]

    def __str__(self):
        return self.who_solve.username + " solves " + self.which_question.question_name
