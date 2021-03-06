# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QTSurvey', '0007_auto_20170221_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomDemographicField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=256)),
                ('surveyID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='QTSurvey.Survey')),
            ],
        ),
        migrations.RemoveField(
            model_name='customdemographic',
            name='field',
        ),
        migrations.RemoveField(
            model_name='customdemographic',
            name='value',
        ),
        migrations.AddField(
            model_name='customdemographic',
            name='response',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customdemographic',
            name='demographicField',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='QTSurvey.CustomDemographicField'),
            preserve_default=False,
        ),
    ]
