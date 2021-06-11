# Generated by Django 3.2.4 on 2021-06-10 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='first_player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_player', to=settings.AUTH_USER_MODEL),
        ),
    ]
