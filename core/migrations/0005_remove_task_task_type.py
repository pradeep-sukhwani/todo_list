# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-15 09:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_task_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_type',
        ),
    ]