from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager
from django.conf import settings

import myadmin


# Create your models here.


# class MyUser(AbstractUser):
#     user_type = models.CharField(u'中文名', max_length=32, blank=False, null=True, default='0')
#
#     class Meta:
#         verbose_name = u'用户详情'
#         verbose_name_plural = u"用户详情"

class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user')


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        # if not email:
        #     raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
            email=UserManager.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):
        user = self.create_user(name, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserInfo(AbstractUser):
    # user_type = models.ForeignKey('UserType', default=1, verbose_name='用户类型')
    user_class = models.ManyToManyField('Class', verbose_name='班级', blank=True)
    phone = models.CharField(max_length=11, verbose_name='电话号码')
    qq = models.CharField(max_length=24, verbose_name='QQ号码')
    auths = models.ForeignKey(to='myadmin.Authority', verbose_name='权限', null=True, blank=True, related_name='auth')
    objects = UserManager()
    permission = models.ManyToManyField(to='myadmin.Permission', null=True, blank=True)
    permissiongroup = models.ManyToManyField(to='myadmin.PermissionGroup', null=True, blank=True)

    def get_all_permissions(self, user_obj=None, obj=None):
        # 获取所有权限集合
        all_permissions = []
        permission = self.permission.all()
        if permission:
            all_permissions.extend(permission)
        permission_group = self.permissiongroup.all()
        for i in permission_group:
            for k in i.Permissions.all():
                all_permissions.append(k)
        return set(all_permissions)

    def has_perm(self, request, perm=None, obj=None):
        # 判断是否有权限访问当前地址
        have_perm = False
        all_permissions = self.get_all_permissions()
        url = request.get_full_path()
        method = request.method
        for i in all_permissions:
            if i.url_type == 0:
                if i.url == url and i.get_method_display() == method:
                    have_perm = True
            else:
                from django.core.urlresolvers import resolve
                if i.url == resolve(request.path).url_name and i.get_method_display() == method:
                    have_perm = True
        return have_perm


class Class(models.Model):
    # 班级类型
    name = models.CharField(max_length=32, verbose_name='班级名')
    area = models.IntegerField(choices=[
        (0, '北京校区'),
        (1, '上海校区'),
        (2, '广州校区'),
    ], default=0, verbose_name='校区')
    status = models.IntegerField(choices=[
        (0, '未启用'),
        (1, '报名中'),
        (2, '上课中'),
        (3, '已结课'),
    ], default=0, verbose_name='状态')
    date = models.DateTimeField(blank=True, verbose_name='开课时间')

    class Meta:
        # verbose_name加s
        verbose_name_plural = '班级'

    def __str__(self):
        return self.name


class Student2Class(models.Model):
    student = models.ForeignKey('Student')
    stu_class = models.ForeignKey('Class')
    status = models.IntegerField(default=0)

    class Meta:
        # 防止重复报名
        unique_together = [
            ('student', 'stu_class'),
        ]


class Student(models.Model):
    # 学员
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    stu_class = models.ManyToManyField(Class, through='Student2Class', through_fields=('student', 'stu_class'))
    # 报名状态
    status = models.IntegerField(choices=[
        (0, '未报名'),
        (0, '已报名'),
        (0, '老学员'),
    ], default=0)


class Teacher(models.Model):
    # 老师
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    teach_class = models.ManyToManyField('Class', default=1)


class Seller(models.Model):
    # 销售
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)


class Manage(models.Model):
    # 销售
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)


class Score(models.Model):
    student = models.ForeignKey('Student')
    stu_class = models.ForeignKey('Class')


class Record(models.Model):
    # 成绩
    student = models.ForeignKey('Student')
    stu_class = models.ForeignKey('Class')
    content = models.CharField(max_length=256)
    record = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class Attendance(models.Model):
    # 考勤
    student = models.ForeignKey('Student')
    stu_class = models.ForeignKey('Class')
    subject = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=[
        (0, '正常'),
        (0, '迟到'),
        (0, '旷课'),
    ], default=0)


class Talk(models.Model):
    send = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='send')
    receive = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receive')
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=0)


