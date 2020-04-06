from django.db import models
from member.models import Member
from plan.models import Plan

# Create your models here.
class Lesson(models.Model):
    date = models.DateField('受講日', blank=False)
    hour = models.IntegerField('受講時間(h)', blank=False, default=0)
    charge_yen = models.IntegerField('支払金額', blank=False, default=0)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, verbose_name='顧客名')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, verbose_name='ジャンル')

