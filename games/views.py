from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth import mixins

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

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
        searched = self.request.GET.get('q') #! クエリパラメータはrequest.GETに、パスパラメータはself.kwargsに入ってる
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
        try:
            result = models.GameResult.objects.get(game=game)
            context.update({'form': forms.GameResultCreationForm(instance=result)})
        except models.GameResult.DoesNotExist:
            pass
        player1_pk = game.player1.pk
        player2_pk = game.player2.pk
        context['form'].fields['win_player'].queryset = get_user_model().objects.all().filter(Q(pk=player1_pk) | Q(pk=player2_pk))
        context['form'].fields['loose_player'].queryset = get_user_model().objects.all().filter(Q(pk=player1_pk) | Q(pk=player2_pk))
        return context

    def form_valid(self, form):
        game = models.Game.objects.get(pk=self.kwargs.get('pk'))
        try:
            result = models.GameResult.objects.get(game=game)
            self.object = result
        except models.GameResult.DoesNotExist:
            self.object = form.save(commit=False)
            self.object.game = game
        self.object.win_player = form.cleaned_data.get('win_player')
        self.object.loose_player = form.cleaned_data.get('loose_player')
        #! デッキ提出がされていない場合はエラーになってしまう
        try:
            win_deck   = models.SubmittedDeck.objects.get(game=game, player=self.object.win_player)
        except models.SubmittedDeck.DoesNotExist:
            self.object.win_player = form.cleaned_data.get('loose_player')
            self.object.loose_player = form.cleaned_data.get('win_player')
        try:
            loose_deck = models.SubmittedDeck.objects.get(game=game, player=self.object.loose_player)
        except models.SubmittedDeck.DoesNotExist: pass
        try:
            self.object.win_and_loose_thema = str(win_deck.thema) + str(loose_deck.thema)
        except: pass
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CreateGameView(mixins.LoginRequiredMixin, generic.CreateView):
    """試合登録用View"""
    model = models.Game
    template_name = 'games/create.html'
    form_class = forms.GameCreationForm

    def get_form(self):
        """日時入力にカレンダーをセット"""
        form = super().get_form()
        form.fields['start_at'].widget = DateTimePickerInput(options={'locale': 'ja'})
        return form

    def get_context_data(self, **kwargs):
        """player2の選択肢からrequest userを除外"""
        context = super().get_context_data(**kwargs)
        context['form'].fields['player2'].queryset = get_user_model().objects.all().exclude(pk=self.request.user.pk)
        return context

    def form_valid(self, form):
        """player1のフィールドにrequest userをセットしてからテーブルに保存"""
        self.object = form.save(commit=False)
        self.object.player1 = self.request.user
        self.object.save()
        #! self.objectにformを保存しないとget_success_url()が機能しない！
        return HttpResponseRedirect(self.get_success_url())


#TODO:試合開始以降は変更不可にする
class CreateSubmittedDeck(mixins.LoginRequiredMixin, generic.CreateView):
    """デッキ提出用View"""
    model = models.SubmittedDeck
    template_name = 'games/submit_deck.html'
    form_class = forms.SubmittedDeckCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = models.Game.objects.get(pk=self.kwargs.get('pk'))
        submitted_deck = models.SubmittedDeck.objects.get(game=game, player=self.request.user)
        if submitted_deck:
            context.update({'form': forms.SubmittedDeckCreationForm(instance=submitted_deck)})
        return context

    #* game, win_and_loose_thema fieldはViewで設定
    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        game = models.Game.objects.get(pk=pk)
        submitted_deck = models.SubmittedDeck.objects.get(game=game, player=self.request.user)
        if submitted_deck:
            submitted_deck.thema = form.cleaned_data.get('thema')
            submitted_deck.image1 = form.cleaned_data.get('image1')
            submitted_deck.image2 = form.cleaned_data.get('image2')
            self.object = submitted_deck
        else:
            self.object = form.save(commit=False)
            self.object.game = game
            self.object.player = self.request.user
        self.object.save()
        #! self.objectにformを保存しないとget_success_url()が機能しない！
        return HttpResponseRedirect(self.get_success_url())