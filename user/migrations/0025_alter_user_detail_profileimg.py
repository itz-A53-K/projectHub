# Generated by Django 4.1.4 on 2023-02-17 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_alter_user_detail_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_detail',
            name='profileImg',
            field=models.ImageField(blank=True, default='/defaultImg/person-circle.png', null=True, upload_to='Profile_Image/'),
        ),
    ]
