# Generated by Django 4.1.7 on 2023-03-19 20:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0036_project_project_file_alter_order_order_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 20, 1, 51, 16, 305249)),
        ),
    ]
