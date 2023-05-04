# Generated by Django 4.1.7 on 2023-03-19 19:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0035_project_created_by_alter_order_order_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_file',
            field=models.FileField(blank=True, null=True, upload_to='projectFile/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 19, 19, 26, 48, 715184)),
        ),
        migrations.AlterField(
            model_name='project',
            name='sub_category',
            field=models.CharField(choices=[('Web Development', (('Front-end Development', 'Front-end Development'), ('Backend', 'Backend'), ('Full-Stack', 'Full-Stack'))), ('Android Development', (('Java', 'Java'), ('kotlin', 'Kotlin'))), ('Cyber Security', 'Cyber Security'), ('Others', (('C', 'C'), ('C++', 'C++'), ('Python', 'Python')))], max_length=100),
        ),
    ]