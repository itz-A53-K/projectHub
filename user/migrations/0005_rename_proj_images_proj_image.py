# Generated by Django 4.1.4 on 2023-02-13 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_project_images_proj_images'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Proj_images',
            new_name='Proj_image',
        ),
    ]
