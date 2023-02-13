# Generated by Django 4.1.4 on 2023-02-12 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('proj_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('shortDesc', models.CharField(blank=True, max_length=500)),
                ('fullDesc', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('Web Development', (('Front-end Development', 'Front-end Development'), ('JavaScript', 'JavaScript'), ('AJAX', 'AJAX'), ('Node Js', 'Node Js'), ('React Js', 'React Js'), ('Angular Js', 'Angular Js'), ('Django', 'Django'), ('PHP', 'PHP'))), ('Android Development', (('Java', 'Java'), ('kotlin', 'Kotlin'))), ('Cyber Security', 'Cyber Security'), ('Others', (('C', 'C'), ('C++', 'C++'), ('C#', 'C#'), ('Python', 'Python')))], max_length=100)),
                ('used_language', models.CharField(blank=True, max_length=500, null=True)),
                ('price', models.FloatField(default='Free')),
                ('discounted_price', models.FloatField(blank=True, default='Free')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateField(auto_now=True)),
                ('images', models.CharField(max_length=500)),
                ('sourcecode_link', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]