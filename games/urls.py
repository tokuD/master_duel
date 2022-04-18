from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('list/', views.GameListView.as_view(), name='list'),
    path('<uuid:pk>/', views.GameDetailView.as_view(), name='detail'),
    path('<uuid:pk>/create_result/', views.CreateGameResultView.as_view(), name='create_result'),
    path('create_game/', views.CreateGameView.as_view(), name='create_game'),
    path('<uuid:pk>/submit_deck/', views.CreateSubmittedDeck.as_view(), name='submit_deck'),
    path('', views.TopView.as_view(), name='home'),
]
