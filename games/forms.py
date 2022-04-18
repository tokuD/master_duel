from dataclasses import field
from django import forms
from django.contrib.auth import get_user_model

from . import models


class GameResultCreationForm(forms.ModelForm):

    class Meta:
        model = models.GameResult
        fields = ('win_player', 'loose_player', )


class GameCreationForm(forms.ModelForm):

    class Meta:
        model = models.Game
        fields = ('category', 'player2',)
        widgets = {
        }

class SubmittedDeckCreationForm(forms.ModelForm):
    """デッキ提出フォーム"""

    class Meta:
        model = models.SubmittedDeck
        fields = ('thema', 'image1', 'image2', )