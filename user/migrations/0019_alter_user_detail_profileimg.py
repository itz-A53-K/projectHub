# Generated by Django 4.1.4 on 2023-02-17 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_order_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_detail',
            name='profileImg',
            field=models.ImageField(blank=True, default='/static/user/img/person-circle.png', null=True, upload_to='Profile_Image'),
        ),
    ]