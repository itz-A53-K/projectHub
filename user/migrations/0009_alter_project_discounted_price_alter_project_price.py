# Generated by Django 4.1.4 on 2023-02-13 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_rename_images_project_default_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='discounted_price',
            field=models.FloatField(blank=True, default='Free', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='price',
            field=models.FloatField(blank=True, default='Free', null=True),
        ),
    ]
