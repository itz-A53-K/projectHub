# Generated by Django 4.1.4 on 2023-02-12 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='images',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
