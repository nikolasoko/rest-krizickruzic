# Generated by Django 3.2.4 on 2021-06-11 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20210611_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_status',
            field=models.CharField(blank=True, default='open', max_length=30),
        ),
    ]
