from operator import ge
from webbrowser import get
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth import mixins

from . import models, forms



class TopView(generic.TemplateView):
    template_name = 'games/top.html'


class GameListView(generic.ListView):
    model = models.Game
    template_name = 'games/list.html'
    ordering = '-start_at'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return models.Game.objects.filter(
                Q(category__title__icontains=query)|
                Q(players__username__icontains=query)
            ).distinct()
        return super().get_queryset()


class GameDetailView(generic.DetailView):
    model = models.Game
    template_name = 'games/detail.html'


class CreateGameResultView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.GameResult
    template_name = 'games/create.html'
    form_class = forms.GameResultCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = models.Game.objects.get(pk=self.kwargs.get('pk'))
        context['form'].fields['win_player'].queryset = game.players.all()
        context['form'].fields['loose_player'].queryset = game.players.all()
        return context

class CreateGameView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Game
    template_name = 'games/create.html'
    form_class = forms.GameCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['opponent'].queryset = get_user_model().objects.all().exclude(pk=self.request.user.pk)
        return context

    def form_valid(self, form):
        game = form.save()
        opponent = form.cleaned_data.get('opponent')
        game.players.add(opponent)
        game.players.add(self.request.user)
        game.save()
        # game.save_m2m()
        print(vars(game.players))
