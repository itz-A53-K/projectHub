# Generated by Django 4.1.6 on 2023-02-17 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_alter_project_default_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_detail',
            name='profileImg',
            field=models.ImageField(default='/defaultImg/person-circle.png', upload_to='Profile_Image/%y'),
        ),
    ]
