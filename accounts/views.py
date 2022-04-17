import imp
from django.shortcuts import redirect, render, resolve_url
from django.views import generic
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden


class UserDetailView(generic.DetailView):
    model = get_user_model()
    template_name = 'account/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object:
            return redirect(resolve_url('games:list'))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)