from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Вход в систему: возвращает JWT-токены."""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Нужны username и password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {'error': 'Неверные учётные данные'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    """Список пользователей (кроме текущего) с информацией о last_seen."""
    from django.utils import timezone
    
    users = User.objects.exclude(id=request.user.id).values(
        'id', 'username', 'first_name', 'last_name', 'last_seen'
    )
    
    now = timezone.now()
    result = []
    
    for user in users:
        last_seen = user['last_seen']
        if last_seen:
            diff = now - last_seen
            seconds = diff.total_seconds()
            
            if seconds < 60:
                status = "на сайте"
            elif seconds < 3600:
                minutes = int(seconds // 60)
                status = f"был {minutes} мин назад"
            elif seconds < 86400:
                hours = int(seconds // 3600)
                status = f"был {hours} ч назад"
            else:
                days = int(seconds // 86400)
                status = f"был {days} дн назад"
        else:
            status = "неизвестно"
        
        user['status'] = status
        result.append(user)
    
    return Response(result)