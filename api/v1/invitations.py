from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from apps.games.models import Invitation, Room, Session, Game
from apps.games.serializers import InvitationSerializer
from services.games import GameEngineFactory


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_invitation(request):
    """Создать приглашение на игру."""
    to_user_id = request.data.get('to_user')
    game_type = request.data.get('game_type')
    message = request.data.get('message', '')
    time_control = request.data.get('time_control', 'unlimited')
    color_preference = request.data.get('color_preference', 'random')

    if not to_user_id or not game_type:
        return Response(
            {'error': 'Нужны to_user и game_type'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if int(to_user_id) == request.user.id:
        return Response(
            {'error': 'Нельзя пригласить самого себя'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Проверяем, что игра существует
    try:
        GameEngineFactory.get_engine(game_type)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Создаём приглашение
    invitation = Invitation.objects.create(
        from_user=request.user,
        to_user_id=to_user_id,
        game_type=game_type,
        invitation_type='friendly',
        status='pending',
        message=message,
        time_control=time_control,
        color_preference=color_preference,
        expires_at=timezone.now() + timedelta(hours=24),
    )

    return Response(
        InvitationSerializer(invitation).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def incoming_invitations(request):
    """Входящие приглашения (для текущего пользователя)."""
    invitations = Invitation.objects.filter(
        to_user=request.user,
        status='pending'
    )
    return Response(InvitationSerializer(invitations, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def outgoing_invitations(request):
    """Исходящие приглашения (от текущего пользователя)."""
    invitations = Invitation.objects.filter(
        from_user=request.user
    )
    return Response(InvitationSerializer(invitations, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invitation(request, invitation_id):
    """Принять приглашение → создаётся Room + Session + Game."""
    try:
        invitation = Invitation.objects.get(id=invitation_id)
    except Invitation.DoesNotExist:
        return Response({'error': 'Приглашение не найдено'}, status=status.HTTP_404_NOT_FOUND)

    # Проверяем, что приглашение адресовано текущему пользователю
    if invitation.to_user != request.user:
        return Response({'error': 'Это не ваше приглашение'}, status=status.HTTP_403_FORBIDDEN)

    if invitation.status != 'pending':
        return Response({'error': 'Приглашение уже обработано'}, status=status.HTTP_400_BAD_REQUEST)

    # Определяем цвета
    if invitation.color_preference == 'random':
        import random
        if random.choice([True, False]):
            player_white = invitation.from_user
            player_black = invitation.to_user
        else:
            player_white = invitation.to_user
            player_black = invitation.from_user
    elif invitation.color_preference == 'white':
        player_white = invitation.from_user
        player_black = invitation.to_user
    else:  # black
        player_white = invitation.to_user
        player_black = invitation.from_user

    # Создаём комнату
    room = Room.objects.create(
        game_type=invitation.game_type,
        player_white=player_white,
        player_black=player_black,
        status='waiting',
        metadata={'time_control': invitation.time_control},
    )

    # Создаём сессию и игру
    engine = GameEngineFactory.get_engine(invitation.game_type)
    initial_state = engine.get_initial_state()

    session = Session.objects.create(room=room)
    game = Game.objects.create(
        session=session,
        game_number=1,
        status='active',
        metadata={'state': initial_state},
    )

    room.status = 'active'
    room.save()

    # Обновляем приглашение: статус + ссылка на комнату
    invitation.status = 'accepted'
    invitation.room = room              # ← НОВОЕ
    invitation.save()

    return Response({
        'status': 'ok',
        'game_id': game.id,
        'room_id': room.id,
        'game_type': invitation.game_type,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_invitation(request, invitation_id):
    """Отклонить приглашение."""
    try:
        invitation = Invitation.objects.get(id=invitation_id)
    except Invitation.DoesNotExist:
        return Response({'error': 'Приглашение не найдено'}, status=status.HTTP_404_NOT_FOUND)

    if invitation.to_user != request.user:
        return Response({'error': 'Это не ваше приглашение'}, status=status.HTTP_403_FORBIDDEN)

    if invitation.status != 'pending':
        return Response({'error': 'Приглашение уже обработано'}, status=status.HTTP_400_BAD_REQUEST)

    invitation.status = 'declined'
    invitation.save()

    return Response({'status': 'ok'})   # ← ИСПРАВЛЕНО