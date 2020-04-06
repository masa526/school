from django.db import models

# Create your models here.
class Plan(models.Model):
    name = models.CharField('ジャンル', max_length=100)
    basic_charge_yen = models.IntegerField('基本料金', blank=False, default=0)
    basic_include_hour = models.IntegerField('基本に含む時間(h)', blank=False, default=0)

    def __str__(self):
        return self.name


class PlanPayg(models.Model):
    payg_start_hour = models.IntegerField('従量変動開始時間(h)', blank=False, default=0)
    payg_end_hour = models.IntegerField('従量変動終了時間(h)', blank=True, null=True )
    payg_charge_yen = models.IntegerField('従量変動料金', blank=False, default=0)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name='ジャンル')
