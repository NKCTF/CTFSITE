from django.test import TestCase
from backend.question.models import Tag, Question, Solve
from backend.user.models import User, Career, Team


class InintDatabase(TestCase):
    def init_question(self):
        T1 = Tag.objects.create(tag_name=Tag.PWN)
        T2 = Tag.objects.create(tag_name=Tag.MISC)
        T3 = Tag.objects.create(tag_name=Tag.WEB)
        T4 = Tag.objects.create(tag_name=Tag.Crypto)
        T5 = Tag.objects.create(tag_name=Tag.Reverse)

        Q1 = Question(question_tag=Tag.MISC, question_name="签到题", description="flag 是 NKCTF{HELLO}")
        Q1.set_flag("NKCTF{HELLO}")
        Q1.save()

    def init_career(self):
        C1 = Career.objects.create(career_name=Career.PWN)
        C2 = Career.objects.create(career_name=Career.MISC)
        C3 = Career.objects.create(career_name=Career.WEB)
        C4 = Career.objects.create(career_name=Career.Crypto)
        C5 = Career.objects.create(career_name=Career.Almighty)
