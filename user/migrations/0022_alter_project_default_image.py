# Generated by Django 4.1.4 on 2023-02-17 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_alter_proj_image_image_alter_user_detail_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='default_image',
            field=models.ImageField(blank=True, null=True, upload_to='Project_Image/'),
        ),
    ]
