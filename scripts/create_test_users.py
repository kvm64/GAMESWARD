"""
Создание тестовых пользователей для GAMESWARD.

Использование:
    python scripts/create_test_users.py
"""
import os
import sys
import django

# Настройка Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Список тестовых пользователей
TEST_USERS = [
    {'username': 'test_opponent', 'password': 'test12345'},
    {'username': 'test_player2',  'password': 'test12345'},
    {'username': 'test_player3',  'password': 'test12345'},
]


def create_test_users():
    """Создаёт тестовых пользователей, если их нет."""
    print("🔧 Создание тестовых пользователей...")

    for data in TEST_USERS:
        username = data['username']
        password = data['password']

        if User.objects.filter(username=username).exists():
            print(f"⏭  Пользователь '{username}' уже существует — пропускаем.")
            continue

        User.objects.create_user(username=username, password=password)
        print(f"✅ Пользователь '{username}' создан (пароль: {password}).")

    print("🎉 Готово!")


if __name__ == '__main__':
    create_test_users()