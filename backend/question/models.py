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

    init_score = models.IntegerField(default=200)
    # TODO: arg_p 是一个控制分数计算的概率参数
    # TODO: arg_p 属于 [0,1]，默认值是 0.6
    # TODO: arg_p 越小，分数极差越大，第一个解出题目的人最终得分越高
    arg_p = models.FloatField(default=0.6)
    solve_by = models.ManyToManyField(User, through="Solve")
    flag = models.CharField(max_length=128)

    def set_flag(self, text_flag):
        self.flag = text_flag

    def check_flag(self, text_flag):
        return self.flag == text_flag

    def get_score(self, rank=None):
        """
        $$ Score_{k} = \frac{p^k}{\sum_{i=1}^{n} p^i} * total $$
        """
        n = self.solve_by.count()
        if rank is None:
            # TODO: 如果没有传入 Rank, 则返回结果表示
            # TODO: 当下一个 Solve 插入时，它可能得到的分数是多少
            n += 1
            k = n
        else:
            # TODO: 如果传入了 Rank 进行计算则使用，第 k 个解出的人实际得分
            k = rank
        p = self.arg_p
        curscore = ( (p ** (k-1))*(1 - p)/(1 - p ** n) )*self.init_score
        return int(curscore)


class Solve(models.Model):
    who_solve = models.ForeignKey(User, on_delete=models.CASCADE)
    which_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def get_ranking(self):
        ranking = Solve.objects.filter(which_question=self.which_question,
                                       time__lte=self.time).count()
        return ranking

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
