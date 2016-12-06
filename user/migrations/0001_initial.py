# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-05 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('yiban_id', models.CharField(max_length=100, unique=True, verbose_name='易班id')),
                ('nickname', models.CharField(max_length=16, verbose_name='昵称')),
                ('sex', models.CharField(choices=[('F', '女'), ('M', '男'), ('U', '保密')], default='U', max_length=1, verbose_name='性别')),
                ('is_admin', models.BooleanField(default=False, verbose_name='管理员')),
            ],
            options={
                'verbose_name': '用户（开发用）',
                'verbose_name_plural': '用户(开发用)',
            },
        ),
    ]