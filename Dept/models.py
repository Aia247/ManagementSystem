from django.db import models


class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")

    # 有约束
    # t0, 与表关联  to_field, 表中的一列关联
    # 生成数据列 depart_id

    # 级联删除
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)

    # 置空
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True,
                               on_delete=models.SET_NULL)

    gender_choices = (
        (0, "女"),
        (1, "男"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

    def __str__(self):
        return self.name


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):
    """ 任务 """
    task = models.CharField(verbose_name="任务", max_length=32)
    status_choices = {
        (1, "一般"),
        (2, "重要"),
        (3, "紧急"),
    }
    status = models.SmallIntegerField(verbose_name="级别", choices=status_choices, default=1)
    user = models.ForeignKey(verbose_name="负责人", to="UserInfo", on_delete=models.CASCADE)
