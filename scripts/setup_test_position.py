import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.games.models import Game

def setup():
    # Берём последнюю игру
    game = Game.objects.order_by('-id').first()
    if not game:
        print("❌ Нет игр в БД. Начните игру в браузере.")
        return
    
    print(f"ID игры: {game.id}")
    
    board = [[None] * 8 for _ in range(8)]
    board[4][3] = {'color': 'white', 'is_king': False}  # d4
    board[3][4] = {'color': 'black', 'is_king': False}  # e5
    board[4][5] = {'color': 'white', 'is_king': False}  # f4
    
    new_state = {
        'board': board,
        'turn': 'white',
        'winner': None,
        'moves_count': 0,
        'must_continue': False,
        'continue_from': None,
    }
    
    game.metadata = {**game.metadata, 'state': new_state}
    game.save()
    
    print(f"✅ Позиция создана для игры {game.id}")
    print("   Белая d4, чёрная e5, белая f4")

if __name__ == '__main__':
    setup()