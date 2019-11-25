from django.db import models


class FilterValue(models.Model):
    value = models.CharField('Значение',max_length=255,blank=True,null=True)
    boolValue = models.BooleanField('Значение Да/Нет', null=True)
    house = models.ForeignKey('pages.House', blank=True, null=True,on_delete=models.CASCADE, verbose_name='Помещение',related_name='houses')
    filter = models.ForeignKey('pages.CategoryFilter', blank=True, null=True,on_delete=models.CASCADE, verbose_name='Фильтр',related_name='cat_filter')
