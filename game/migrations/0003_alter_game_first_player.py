# Generated by Django 3.2.4 on 2021-06-10 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0002_alter_game_first_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='first_player',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='first_player', to='auth.user'),
            preserve_default=False,
        ),
    ]
