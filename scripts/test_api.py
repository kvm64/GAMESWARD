import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_api():
    print("🎮 Тест API GAMESWARD...")
    
    client = Client()
    
    # 1. Проверяем список игр (без авторизации)
    response = client.get('/api/v1/games/available/')
    print(f"\n1. Список игр: {response.status_code}")
    print(f"   {response.json()}")
    
    # 2. Авторизуемся
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        print("❌ Нет суперпользователя. Создайте: python manage.py createsuperuser")
        return
    
    client.force_login(user)
    print(f"\n2. Авторизован как: {user.username}")
    
    # 3. Создаём второго пользователя
    opponent, created = User.objects.get_or_create(
        username='test_opponent',
        defaults={'email': 'opponent@test.com'}
    )
    if created:
        opponent.set_password('test123')
        opponent.save()
        print(f"   Создан противник: {opponent.username}")
    
    # 4. Создаём комнату
    response = client.post('/api/v1/games/rooms/create/', {
        'game_type': 'tictactoe',
        'opponent_id': opponent.id,
    }, content_type='application/json')
    print(f"\n3. Создание комнаты: {response.status_code}")
    print(f"   {response.json()}")
    
    if response.status_code == 201:
        room_id = response.json()['id']
        
        # 5. Начинаем игру
        response = client.post(f'/api/v1/games/rooms/{room_id}/start/')
        print(f"\n4. Начало игры: {response.status_code}")
        game_data = response.json()
        print(f"   Игра ID: {game_data.get('id')}")
        
        game_id = game_data['id']
        
        # 6. Делаем ход
        response = client.post(f'/api/v1/games/{game_id}/move/', {
            'move': {'cell': 4},
        }, content_type='application/json')
        print(f"\n5. Ход (cell=4): {response.status_code}")
        print(f"   {response.json()}")
        
        # 7. Получаем состояние
        response = client.get(f'/api/v1/games/{game_id}/state/')
        print(f"\n6. Состояние игры: {response.status_code}")
        print(f"   {response.json()}")
    
    print("\n🎉 Тест API завершён!")

if __name__ == '__main__':
    test_api()