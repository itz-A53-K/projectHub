# Generated by Django 4.1.7 on 2023-03-10 14:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0033_rename_proj_id_proj_image_project_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sub_category',
            field=models.CharField(choices=[('Web Development', (('Front-end Development', 'Front-end Development'), ('JavaScript', 'JavaScript'), ('AJAX', 'AJAX'), ('Node Js', 'Node Js'), ('React Js', 'React Js'), ('Angular Js', 'Angular Js'), ('Django', 'Django'), ('PHP', 'PHP'), ('C#', 'C#'))), ('Android Development', (('Java', 'Java'), ('kotlin', 'Kotlin'))), ('Cyber Security', 'Cyber Security'), ('Others', (('C', 'C'), ('C++', 'C++'), ('Python', 'Python')))], default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 20, 10, 33, 736932)),
        ),
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.CharField(choices=[('Project', 'Project'), ('Template', 'Template')], max_length=100),
        ),
    ]
