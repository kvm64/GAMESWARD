import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from services.games import GameEngineFactory

def test_double_capture():
    print("🎮 Тест серийного взятия...")
    
    engine = GameEngineFactory.get_engine('russian_checkers')
    state = engine.get_initial_state()
    
    # Очищаем доску
    for r in range(8):
        for c in range(8):
            state['board'][r][c] = None
    
    # Белая на (5, 2), чёрные на (4, 3) и (2, 5)
    state['board'][5][2] = {'color': 'white', 'is_king': False}
    state['board'][4][3] = {'color': 'black', 'is_king': False}
    state['board'][2][5] = {'color': 'black', 'is_king': False}
    state['turn'] = 'white'
    
    print("Позиция: белая (5,2), чёрные (4,3) и (2,5)")
    
    # Первый прыжок: (5,2) → (3,4) через (4,3)
    move1 = {'from': [5, 2], 'to': [3, 4]}
    print(f"\nПервый прыжок: {move1}")
    print(f"  Допустим? {engine.validate_move(state, move1)}")
    
    state = engine.apply_move(state, move1)
    print(f"  must_continue: {state.get('must_continue')}")
    print(f"  continue_from: {state.get('continue_from')}")
    print(f"  turn: {state['turn']}")
    print(f"  (4,3): {state['board'][4][3]}")
    print(f"  (3,4): {state['board'][3][4]}")
    
    # Второй прыжок: (3,4) → (1,6) через (2,5)
    move2 = {'from': [3, 4], 'to': [1, 6]}
    print(f"\nВторой прыжок: {move2}")
    print(f"  Допустим? {engine.validate_move(state, move2)}")
    
    state = engine.apply_move(state, move2)
    print(f"  must_continue: {state.get('must_continue')}")
    print(f"  turn: {state['turn']}")
    print(f"  (2,5): {state['board'][2][5]}")
    print(f"  (1,6): {state['board'][1][6]}")

if __name__ == '__main__':
    test_double_capture()