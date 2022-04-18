from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth import mixins

from . import models, forms



class TopView(generic.TemplateView):
    template_name = 'games/top.html'


class GameListView(generic.ListView):
    """試合一覧表示用View"""
    model = models.Game
    template_name = 'games/list.html'
    ordering = '-start_at'

    def get_context_data(self, **kwargs):
        """検索した際に入力が残るように処理"""
        context = super().get_context_data(**kwargs)
        searched = self.request.GET.get('q')
        if searched:
            context['searched'] = searched
        return context

    def get_queryset(self):
        """検索処理"""
        query = self.request.GET.get('q')
        if query:
            return models.Game.objects.filter(
                Q(category__title__icontains=query)|
                Q(player1__username__icontains=query) |
                Q(player2__username__icontains=query)
            ).distinct()
        return super().get_queryset()


class GameDetailView(generic.DetailView):
    model = models.Game
    template_name = 'games/detail.html'


class CreateGameResultView(mixins.LoginRequiredMixin, generic.CreateView):
    """試合結果入力用View"""
    model = models.GameResult
    template_name = 'games/create.html'
    form_class = forms.GameResultCreationForm

    def get_context_data(self, **kwargs):
        """勝者・敗者の選択肢を出場選手のみに設定"""
        context = super().get_context_data(**kwargs)
        game = models.Game.objects.get(pk=self.kwargs.get('pk'))
        player1_pk = game.player1.pk
        player2_pk = game.player2.pk
        context['form'].fields['win_player'].queryset = get_user_model().objects.all().filter(Q(pk=player1_pk) | Q(pk=player2_pk))
        context['form'].fields['loose_player'].queryset = get_user_model().objects.all().filter(Q(pk=player1_pk) | Q(pk=player2_pk))
        return context

class CreateGameView(mixins.LoginRequiredMixin, generic.CreateView):
    """試合登録用View"""
    model = models.Game
    template_name = 'games/create.html'
    form_class = forms.GameCreationForm

    def get_context_data(self, **kwargs):
        """player2の選択肢からrequest userを除外"""
        context = super().get_context_data(**kwargs)
        context['form'].fields['player2'].queryset = get_user_model().objects.all().exclude(pk=self.request.user.pk)
        return context

    def form_valid(self, form):
        """player1のフィールドにrequest userをセットしてからテーブルに保存"""
        self.game = form.save(commit=False)
        self.game.player1 = self.request.user
        self.game.save()
        return HttpResponseRedirect(reverse('games:detail', kwargs={'pk': self.game.get_pk()}))

#TODO:
class CreateSubmittedDeck(mixins.LoginRequiredMixin, generic.CreateView):
    """デッキ提出用View"""
    model = models.SubmittedDeck
    template_name = 'games/submit_deck.html'
    form_class = forms.SubmittedDeckCreationForm