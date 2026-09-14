import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.accounts.models import Role

def create_roles():
    print("🔧 Создание базовых ролей...")
    
    roles = [
        # Игровые роли
        {'name': 'Игрок', 'code': 'player', 'context': 'game', 'description': 'Участник игры'},
        {'name': 'Мастер', 'code': 'master', 'context': 'game', 'description': 'Опытный игрок, наставник'},
        {'name': 'Гость', 'code': 'guest', 'context': 'game', 'description': 'Наблюдатель'},
        
        # Форумные роли
        {'name': 'Член', 'code': 'member', 'context': 'forum', 'description': 'Участник форума'},
        {'name': 'Модератор', 'code': 'moderator', 'context': 'forum', 'description': 'Модератор форума'},
        
        # Турнирные роли
        {'name': 'Инспектор', 'code': 'inspector', 'context': 'tournament', 'description': 'Организатор турниров'},
        
        # Судейские роли
        {'name': 'Судья', 'code': 'judge', 'context': 'referee', 'description': 'Судья турниров'},
        
        # Системные роли
        {'name': 'Администратор', 'code': 'admin', 'context': 'system', 'description': 'Администратор платформы'},
    ]
    
    for role_data in roles:
        role, created = Role.objects.get_or_create(
            code=role_data['code'],
            defaults=role_data
        )
        if created:
            print(f"✅ Роль '{role.name}' создана.")
        else:
            print(f"ℹ️ Роль '{role.name}' уже существует.")
    
    print("🎉 Базовые роли созданы!")

if __name__ == '__main__':
    create_roles()