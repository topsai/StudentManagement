from django.db import models

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '菜单'
        verbose_name = '菜单'

    def __str__(self):
        return self.name


class Authority(models.Model):
    name = models.CharField(max_length=32)
    menu = models.ManyToManyField('Menu', related_name='au')

    class Meta:
        verbose_name_plural = '权限'

    def __str__(self):
        return self.name
