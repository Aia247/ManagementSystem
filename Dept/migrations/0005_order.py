# Generated by Django 3.2.19 on 2023-07-04 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dept', '0004_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.CharField(max_length=64, verbose_name='订单号')),
                ('title', models.CharField(max_length=32, verbose_name='名称')),
                ('price', models.IntegerField(verbose_name='价格')),
                ('status', models.SmallIntegerField(choices=[(1, '待支付'), (2, '已支付')], default=1, verbose_name='状态')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dept.admin', verbose_name='管理员')),
            ],
        ),
    ]
