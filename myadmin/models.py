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
        permissions = (("干点啥", "权限描述"),)


class Authority(models.Model):
    name = models.CharField(max_length=32)
    menu = models.ManyToManyField('Menu', related_name='au')

    class Meta:
        verbose_name_plural = 'Authority'

    def __str__(self):
        return self.name


class Permission(models.Model):
    # 权限表
    choises = [(0, '绝对路径'), (1, '相对路径'), ]
    method_choises = [(0, 'GET'), (1, 'POST'), ]
    name = models.CharField(max_length=32, verbose_name='权限名称')  # 权限名称
    description = models.CharField(max_length=256, verbose_name='描述', null=True, blank=True)  # 权限描述
    url = models.CharField(max_length=128)
    url_type = models.BooleanField(default=0, choices=choises)
    method = models.IntegerField(choices=method_choises, default=0)
    args = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = '权限'

    def __str__(self):
        return self.name


class PermissionGroup(models.Model):
    name = models.CharField(max_length=32, verbose_name='组名')  # 权限名称
    Permissions = models.ManyToManyField(to='Permission')

    def __str__(self):
        return self.name

