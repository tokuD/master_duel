# Generated by Django 4.0.4 on 2022-04-19 14:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import games.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='game_player2', to=settings.AUTH_USER_MODEL, verbose_name='対戦相手'),
        ),
        migrations.AlterField(
            model_name='game',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 19, 14, 37, 46, 598389, tzinfo=utc), validators=[games.models.check_date], verbose_name='開始日時'),
        ),
    ]
