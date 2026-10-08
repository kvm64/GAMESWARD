from django.urls import path
from . import games, accounts, invitations

urlpatterns = [
    # Аутентификация
    path('auth/login/', accounts.login, name='login'),
    path('users/', accounts.list_users, name='list_users'),

    # Игры
    path('games/available/', games.available_games, name='available_games'),
    path('games/rooms/create/', games.create_room, name='create_room'),
    path('games/rooms/<int:room_id>/start/', games.start_game, name='start_game'),
    path('games/<int:game_id>/move/', games.make_move, name='make_move'),
    path('games/<int:game_id>/state/', games.get_game_state, name='get_game_state'),
    path('games/<int:game_id>/resign/', games.resign_game, name='resign_game'),

    # Приглашения
    path('invitations/create/', invitations.create_invitation, name='create_invitation'),
    path('invitations/incoming/', invitations.incoming_invitations, name='incoming_invitations'),
    path('invitations/outgoing/', invitations.outgoing_invitations, name='outgoing_invitations'),
    path('invitations/<int:invitation_id>/accept/', invitations.accept_invitation, name='accept_invitation'),
    path('invitations/<int:invitation_id>/decline/', invitations.decline_invitation, name='decline_invitation'),
]