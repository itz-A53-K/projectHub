# Generated by Django 4.1.6 on 2023-02-17 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_alter_user_detail_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_detail',
            name='profileImg',
            field=models.ImageField(upload_to='Profile_Image/%y'),
        ),
    ]