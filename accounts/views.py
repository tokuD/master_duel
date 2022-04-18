from django.db.models import Q
from django.shortcuts import redirect, render, resolve_url
from django.views import generic
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.contrib import messages

from games import models

class UserDetailView(generic.DetailView):
    """ユーザーページ用View"""

    model = get_user_model()
    template_name = 'account/detail.html'

    def get_context_data(self, **kwargs):
        """request userの出場した試合をgamesとして渡す"""
        context = super().get_context_data(**kwargs)
        games = models.Game.objects.all().filter(Q(player1=self.request.user)|Q(player2=self.request.user)).distinct().order_by('-start_at')
        context['games'] = games
        return context

    def get(self, request, *args, **kwargs):
        """自分以外のページならリダイレクトさせる"""
        self.object = self.get_object()
        if request.user != self.object:
            return redirect(resolve_url('games:list'))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)