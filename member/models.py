from django.db import models

# Create your models here.
class Member(models.Model):
    GENDER= [
        ('1', '女性'),
        ('2', '男性'),
    ]
    GENERATION = [
        ('10', '10代'),
        ('20', '20代'),
        ('30', '30代'),
        ('40', '40代'),
        ('50', '50代'),
        ('60', '60代'),
        ('70', '70代'),
    ]
    name = models.CharField('顧客名', max_length=100)
    gender = models.CharField('性別', max_length=1, choices=GENDER)
    age = models.IntegerField('年齢', blank=True, default=0)

    def __str__(self):
        return self.name
