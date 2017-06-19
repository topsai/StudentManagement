from django.db import models

# Create your models here.


class Class(models.Model):
    # 班级类型
    name = models.CharField(max_length=32)
    area = models.IntegerField(choices=[
        (0, '北京校区'),
        (1, '上海校区'),
        (2, '广州校区'),
    ], default=None)
    # teachers = models.ManyToManyField('Teacher')


# class User(models.Model):
#     name = models.CharField(max_length=32)
#     pwd = models.CharField(max_length=32)
#     type = models.IntegerField(choices=[
#         (0, '学生'),
#         (0, '老师'),
#         (0, '销售'),
#         (0, '管理员'),
#     ], default=0)


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
