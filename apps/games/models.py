from django.db import models
from django.conf import settings


class Invitation(models.Model):
    """Приглашение на игру."""
    
    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('accepted', 'Принято'),
        ('declined', 'Отклонено'),
        ('expired', 'Истекло'),
        ('cancelled', 'Отменено'),
    )
    
    TYPE_CHOICES = (
        ('challenge', 'Вызов на дуэль'),
        ('friendly', 'Дружеская игра'),
        ('tournament', 'Турнирная партия'),
    )
    
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sent_invitations', verbose_name="От кого"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='received_invitations', verbose_name="Кому"
    )
    game_type = models.CharField(max_length=50, default='chess', verbose_name="Тип игры")
    invitation_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='friendly', verbose_name="Тип приглашения")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    message = models.TextField(blank=True, verbose_name="Сообщение")
    
    # НОВЫЕ поля:
    time_control = models.CharField(max_length=20, default='unlimited', verbose_name="Контроль времени")
    color_preference = models.CharField(max_length=10, default='random', verbose_name="Предпочтение цвета")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Истекает")
    
    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.get_status_display()})"
    
    class Meta:
        verbose_name = "Приглашение"
        verbose_name_plural = "Приглашения"
        ordering = ['-created_at']

class Room(models.Model):
    """Комната для игры двух игроков."""
    
    STATUS_CHOICES = (
        ('waiting', 'Ожидание'),
        ('active', 'Активна'),
        ('paused', 'Отложена'),
        ('finished', 'Завершена'),
        ('archived', 'Архивирована'),
    )
    
    TIME_MODE_CHOICES = (
        ('limited', 'С ограничением времени'),
        ('unlimited', 'Без ограничения времени'),
    )
    
    game_type = models.CharField(max_length=50, default='chess', verbose_name="Тип игры")
    player_white = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='rooms_as_white', verbose_name="Белые"
    )
    player_black = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='rooms_as_black', verbose_name="Чёрные"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name="Статус")
    time_mode = models.CharField(max_length=20, choices=TIME_MODE_CHOICES, default='unlimited', verbose_name="Режим времени")
    
    metadata = models.JSONField(default=dict, verbose_name="Метаданные")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Начало")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="Окончание")
    
    def __str__(self):
        return f"Комната {self.id}: {self.player_white.username} vs {self.player_black.username}"
    
    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        ordering = ['-created_at']


class Session(models.Model):
    """Сеанс игры (временной контейнер)."""
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='sessions', verbose_name="Комната")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Начало")
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name="Окончание")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    def __str__(self):
        return f"Сеанс #{self.id} (Комната {self.room.id})"
    
    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"


class Game(models.Model):
    """Игра (партия)."""
    
    STATUS_CHOICES = (
        ('waiting', 'Ожидание'),
        ('active', 'Активна'),
        ('paused', 'Отложена'),
        ('checkmate', 'Мат'),
        ('stalemate', 'Пат'),
        ('draw', 'Ничья'),
        ('resigned', 'Сдача'),
        ('timeout', 'Просрочка времени'),
        ('abandoned', 'Прервана'),
        ('finished', 'Завершена'),
    )
    
    RESULT_CHOICES = (
        ('white_win', 'Победа белых'),
        ('black_win', 'Победа чёрных'),
        ('draw', 'Ничья'),
        ('undefined', 'Не определён'),
    )
    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='games', verbose_name="Сеанс")
    game_number = models.IntegerField(default=1, verbose_name="Номер партии")
    
    initial_fen = models.CharField(max_length=200, blank=True, verbose_name="Начальная позиция")
    moves = models.JSONField(default=list, verbose_name="Ходы")
    current_fen = models.CharField(max_length=200, blank=True, verbose_name="Текущая позиция")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting', verbose_name="Статус")
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='undefined', verbose_name="Результат")
    
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Начало")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="Окончание")
    
    is_paused = models.BooleanField(default=False, verbose_name="Отложена")
    metadata = models.JSONField(default=dict, verbose_name="Метаданные")
    
    def __str__(self):
        return f"Игра #{self.id} (Сеанс {self.session.id})"
    
    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ['-started_at']