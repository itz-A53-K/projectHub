# Generated by Django 4.1.4 on 2023-02-20 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_alter_user_detail_profileimg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
    ]