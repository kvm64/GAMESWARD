from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Кастомная модель пользователя."""
    
    # Обязательные поля (наследуются от AbstractUser):
    # - username (логин)
    # - email (почта)
    # - password (пароль)
    
    # Необязательные поля
    patronymic = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    bio = models.TextField(blank=True, verbose_name="О себе")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    
    # Системные поля
    last_seen = models.DateTimeField(null=True, blank=True, verbose_name="Последний визит")
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Role(models.Model):
    """Роль пользователя в определённом контексте."""
    
    CONTEXT_CHOICES = (
        ('game', 'Игры'),
        ('forum', 'Форум'),
        ('tournament', 'Турниры'),
        ('referee', 'Судейство'),
        ('system', 'Система'),
    )
    
    name = models.CharField(max_length=50, verbose_name="Название")
    code = models.CharField(max_length=50, unique=True, verbose_name="Код")
    context = models.CharField(max_length=20, choices=CONTEXT_CHOICES, verbose_name="Контекст")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_system = models.BooleanField(default=False, verbose_name="Системная роль")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"{self.name} ({self.get_context_display()})"
    
    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
        ordering = ['context', 'name']


class RoleGroup(models.Model):
    """Группа ролей для удобства назначения."""
    
    name = models.CharField(max_length=100, verbose_name="Название группы")
    description = models.TextField(blank=True, verbose_name="Описание")
    roles = models.ManyToManyField(Role, related_name='groups', verbose_name="Роли")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Группа ролей"
        verbose_name_plural = "Группы ролей"


class UserStatus(models.Model):
    """Статус пользователя (роль, назначенная пользователю)."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statuses', verbose_name="Пользователь")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Роль")
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата назначения")
    assigned_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_statuses', verbose_name="Кем назначен"
    )
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Действует до")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    def __str__(self):
        return f"{self.user.username} — {self.role.name}"
    
    class Meta:
        verbose_name = "Статус пользователя"
        verbose_name_plural = "Статусы пользователей"
        ordering = ['-assigned_at']