# Generated by Django 4.0.4 on 2022-04-17 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeckThema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='テーマ名')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_at', models.DateTimeField(auto_now_add=True, verbose_name='開始日時')),
            ],
        ),
        migrations.CreateModel(
            name='GameCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='試合カテゴリ')),
            ],
        ),
        migrations.CreateModel(
            name='SubmittedDeck',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image1', models.ImageField(upload_to='decks/', verbose_name='デッキ画像')),
                ('image2', models.ImageField(blank=True, upload_to='decks/', verbose_name='デッキ画像')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_deck', to='games.game', verbose_name='試合')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='submitted_deck', to=settings.AUTH_USER_MODEL, verbose_name='player')),
                ('thema', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='submitted_deck', to='games.deckthema', verbose_name='テーマ名')),
            ],
        ),
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('win_and_loose_thema', models.CharField(max_length=200, verbose_name='テーマ勝敗')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_result', to='games.game', verbose_name='試合')),
                ('loose_player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='game_result_loose', to=settings.AUTH_USER_MODEL, verbose_name='敗者')),
                ('win_player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='game_result_win', to=settings.AUTH_USER_MODEL, verbose_name='勝者')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='games', to='games.gamecategory', verbose_name='試合カテゴリ'),
        ),
        migrations.AddField(
            model_name='game',
            name='opponent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='opponent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(related_name='game', to=settings.AUTH_USER_MODEL, verbose_name='対戦者'),
        ),
    ]
