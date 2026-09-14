import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from services.games import GameEngineFactory

def test_move():
    print("🎮 Тест хода белой шашки (5,4) → (4,5)...")
    
    engine = GameEngineFactory.get_engine('checkers')
    state = engine.get_initial_state()
    
    print(f"Ход: {state['turn']}")
    print(f"Шашка на (5,4): {state['board'][5][4]}")
    print(f"Клетка (4,5): {state['board'][4][5]}")
    
    move = {'from': [5, 4], 'to': [4, 5]}
    
    is_valid = engine.validate_move(state, move)
    print(f"\nХод допустим? {is_valid}")
    
    if is_valid:
        new_state = engine.apply_move(state, move)
        print(f"✅ Ход применён. Новая доска (5,4): {new_state['board'][5][4]}")
        print(f"✅ Новая доска (4,5): {new_state['board'][4][5]}")
        print(f"Теперь ход: {new_state['turn']}")

if __name__ == '__main__':
    test_move()