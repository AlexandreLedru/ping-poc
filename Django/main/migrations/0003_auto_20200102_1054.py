# Generated by Django 3.0 on 2020-01-02 10:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200102_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 2, 10, 54, 11, 246192), verbose_name='date published'),
        ),
    ]
