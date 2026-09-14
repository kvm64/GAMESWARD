from django.urls import path
from . import games, accounts

urlpatterns = [
    path('auth/login/', accounts.login, name='login'),
    path('games/available/', games.available_games, name='available_games'),
    path('games/rooms/create/', games.create_room, name='create_room'),
    path('games/rooms/<int:room_id>/start/', games.start_game, name='start_game'),
    path('games/<int:game_id>/move/', games.make_move, name='make_move'),
    path('games/<int:game_id>/state/', games.get_game_state, name='get_game_state'),
]