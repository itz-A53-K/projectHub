# Generated by Django 4.1.7 on 2023-03-11 17:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_project_sub_category_alter_order_order_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_by',
            field=models.CharField(blank=True, default='Team Members', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 11, 23, 1, 46, 322253)),
        ),
    ]
