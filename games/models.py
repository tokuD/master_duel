from distutils.command.upload import upload
from ntpath import realpath
from termios import TIOCCONS
import uuid
from django.db import models
from django.conf import settings
from django.forms import ValidationError
from django.urls import reverse, reverse_lazy


class GameCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='試合カテゴリ')

    def __str__(self):
        return self.title


class DeckThema(models.Model):
    name = models.CharField(max_length=200, verbose_name='テーマ名')

    def __str__(self):
        return self.name


class Game(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    category = models.ForeignKey(to=GameCategory, on_delete=models.PROTECT, verbose_name='試合カテゴリ', related_name='games')
    player1 = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='player1', related_name='game_player1')
    player2 = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='対戦相手', related_name='game_player2')
    start_at = models.DateTimeField(verbose_name='開始日時', auto_now_add=True)

    def __str__(self):
        return "{} - {} vs. {}".format(self.category.title, self.player1, self.player2)

    def get_absolute_url(self):
        return reverse('games:detail', kwargs={'pk': self.pk})

    def get_pk(self):
        return str(self.pk)


class SubmittedDeck(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE, related_name='submitted_deck', verbose_name='試合')
    player = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='player', related_name='submitted_deck')
    thema = models.ForeignKey(to=DeckThema, related_name='submitted_deck', verbose_name='テーマ名', on_delete=models.PROTECT)
    image1 = models.ImageField(upload_to='decks/', verbose_name='デッキ画像')
    image2 = models.ImageField(upload_to='decks/', verbose_name='デッキ画像', blank=True)

    def __str__(self):
        return self.game.__str__() + " ({})".format(self.player)


class GameResult(models.Model):
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE, related_name='game_result', verbose_name='試合')
    win_player = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='勝者', related_name='game_result_win')
    loose_player = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='敗者', related_name='game_result_loose')
    win_and_loose_thema = models.CharField(max_length=200, verbose_name='テーマ勝敗')

    def __str__(self):
        return self.game.__str__() + " 結果"
