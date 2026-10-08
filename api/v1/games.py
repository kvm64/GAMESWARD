from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.games.models import Room, Session, Game
from apps.games.serializers import RoomSerializer, GameSerializer
from services.games import GameEngineFactory


@api_view(['GET'])
def available_games(request):
    """Список доступных игр."""
    games = GameEngineFactory.get_available_games()
    return Response(games)


@api_view(['POST'])
def create_room(request):
    """Создать комнату для игры."""
    game_type = request.data.get('game_type')
    opponent_id = request.data.get('opponent_id')

    if not game_type or not opponent_id:
        return Response(
            {'error': 'Нужны game_type и opponent_id'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        engine = GameEngineFactory.get_engine(game_type)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    room = Room.objects.create(
        game_type=game_type,
        player_white=request.user,
        player_black_id=opponent_id,
        status='waiting',
    )

    return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def start_game(request, room_id):
    """Начать игру в комнате."""
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response({'error': 'Комната не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if room.status != 'waiting':
        return Response({'error': 'Игра уже начата'}, status=status.HTTP_400_BAD_REQUEST)

    engine = GameEngineFactory.get_engine(room.game_type)
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

    return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def make_move(request, game_id):
    """Сделать ход в игре."""
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({'error': 'Игра не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if game.status != 'active':
        return Response({'error': 'Игра не активна'}, status=status.HTTP_400_BAD_REQUEST)

    move = request.data.get('move')
    if not move:
        return Response({'error': 'Нужен move'}, status=status.HTTP_400_BAD_REQUEST)

    room = game.session.room
    engine = GameEngineFactory.get_engine(room.game_type)
    state = game.metadata.get('state')

    if not engine.validate_move(state, move):
        return Response({'error': 'Недопустимый ход'}, status=status.HTTP_400_BAD_REQUEST)

    new_state = engine.apply_move(state, move)

    game.metadata = {**game.metadata, 'state': new_state}
    game.moves = game.moves + [move]

    game_over = engine.check_game_over(new_state)
    if game_over['is_over']:
        game.status = 'finished'
        if game_over.get('reason') == 'draw':
            game.result = 'draw'
        else:
            game.result = game_over.get('winner') or 'draw'

    game.save()

    return Response(GameSerializer(game).data)


@api_view(['GET'])
def get_game_state(request, game_id):
    """Получить текущее состояние игры."""
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({'error': 'Игра не найдена'}, status=status.HTTP_404_NOT_FOUND)

    room = game.session.room

    # Определяем символ текущего игрока (универсально для всех игр)
    COLORED_GAMES = ['russian_checkers', 'chess']

    if room.player_white == request.user:
        my_symbol = 'white' if room.game_type in COLORED_GAMES else 'X'
    elif room.player_black == request.user:
        my_symbol = 'black' if room.game_type in COLORED_GAMES else 'O'
    else:
        my_symbol = None

    return Response({
        'game': GameSerializer(game).data,
        'state': game.metadata.get('state'),
        'my_symbol': my_symbol,
        'game_type': room.game_type,
        'player_white': room.player_white.username,
        'player_black': room.player_black.username,
    })


@api_view(['POST'])
def resign_game(request, game_id):
    """Сдаться в игре."""
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({'error': 'Игра не найдена'}, status=status.HTTP_404_NOT_FOUND)

    if game.status != 'active':
        return Response({'error': 'Игра уже завершена'}, status=status.HTTP_400_BAD_REQUEST)

    room = game.session.room
    COLORED_GAMES = ['russian_checkers', 'chess']

    if room.player_white == request.user:
        winner = 'black' if room.game_type in COLORED_GAMES else 'O'
    elif room.player_black == request.user:
        winner = 'white' if room.game_type in COLORED_GAMES else 'X'
    else:
        return Response({'error': 'Вы не участник игры'}, status=status.HTTP_403_FORBIDDEN)

    game.status = 'finished'
    game.result = winner
    game.save()

    return Response({
        'status': 'ok',
        'winner': winner,
        'reason': 'resign',
    })