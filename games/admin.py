from django.contrib import admin

from . import models

class SubmittedDeckInline(admin.StackedInline):
    model = models.SubmittedDeck
    extra = 2

class GamesAdmin(admin.ModelAdmin):
    inlines = [
        SubmittedDeckInline,
    ]


admin.site.register(models.Game, GamesAdmin)
admin.site.register(models.GameCategory)
admin.site.register(models.SubmittedDeck)
admin.site.register(models.DeckThema)
admin.site.register(models.GameResult)