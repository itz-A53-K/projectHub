# Generated by Django 4.1.4 on 2023-02-13 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_project_free'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='free',
            field=models.BooleanField(default=False),
        ),
    ]