# Generated by Django 2.1 on 2018-08-11 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='123456', max_length=32),
        ),
    ]
