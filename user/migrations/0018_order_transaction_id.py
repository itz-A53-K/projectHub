# Generated by Django 4.1.4 on 2023-02-17 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_alter_user_detail_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(default=0, max_length=300),
            preserve_default=False,
        ),
    ]
