# Generated by Django 4.1.4 on 2023-02-22 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0032_rename_project_proj_image_proj_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proj_image',
            old_name='proj_id',
            new_name='project',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 22, 23, 23, 54, 667423)),
        ),
    ]
