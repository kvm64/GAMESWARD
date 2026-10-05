from rest_framework import serializers
from .models import Invitation, Room, Session, Game


class InvitationSerializer(serializers.ModelSerializer):
    from_user_username = serializers.CharField(source='from_user.username', read_only=True)
    to_user_username = serializers.CharField(source='to_user.username', read_only=True)

    # НОВЫЕ поля для авто-открытия игры у отправителя
    room_id = serializers.SerializerMethodField()
    game_id = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = [
            'id', 'from_user', 'from_user_username',
            'to_user', 'to_user_username',
            'game_type', 'invitation_type', 'status',
            'message', 'created_at', 'expires_at',
            'room_id', 'game_id',
        ]
        read_only_fields = ['status', 'created_at']

    def get_room_id(self, obj):
        """ID комнаты, если приглашение принято."""
        return obj.room.id if obj.room else None

    def get_game_id(self, obj):
        """ID игры в комнате, если приглашение принято."""
        if not obj.room:
            return None
        game = Game.objects.filter(session__room=obj.room).order_by('-id').first()
        return game.id if game else None


class RoomSerializer(serializers.ModelSerializer):
    player_white_username = serializers.CharField(source='player_white.username', read_only=True)
    player_black_username = serializers.CharField(source='player_black.username', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'game_type',
            'player_white', 'player_white_username',
            'player_black', 'player_black_username',
            'status', 'time_mode', 'metadata',
            'created_at', 'started_at', 'finished_at'
        ]
        read_only_fields = ['status', 'created_at']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'room', 'started_at', 'ended_at', 'is_active']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'id', 'session', 'game_number',
            'initial_fen', 'moves', 'current_fen',
            'status', 'result',
            'started_at', 'finished_at',
            'is_paused', 'metadata'
        ]