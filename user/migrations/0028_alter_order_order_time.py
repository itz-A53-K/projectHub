# Generated by Django 4.1.4 on 2023-02-21 08:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_alter_order_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 21, 8, 18, 14, 102578, tzinfo=datetime.timezone.utc)),
        ),
    ]