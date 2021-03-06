# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-04 17:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log_reg', '0001_initial'),
        ('grades', '0003_student_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_assignment', to='log_reg.User'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='subject',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='teacher',
            field=models.ManyToManyField(related_name='teacher_student', to='log_reg.User'),
        ),
    ]
