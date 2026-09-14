import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from services.games import GameEngineFactory

def test_capture_2():
    print("🎮 Тест взятия белой (4,7) через (3,6) на (2,5)...")
    
    engine = GameEngineFactory.get_engine('russian_checkers')
    state = engine.get_initial_state()
    
    # Очищаем доску
    for r in range(8):
        for c in range(8):
            state['board'][r][c] = None
    
    # Белая на (4,7)
    state['board'][4][7] = {'color': 'white', 'is_king': False}
    # Чёрная на (3,6)
    state['board'][3][6] = {'color': 'black', 'is_king': False}
    # (2,5) пуста
    
    state['turn'] = 'white'
    
    print(f"Белая на (4,7): {state['board'][4][7]}")
    print(f"Чёрная на (3,6): {state['board'][3][6]}")
    print(f"(2,5): {state['board'][2][5]}")
    
    move = {'from': [4, 7], 'to': [2, 5]}
    print(f"\nХод: {move}")
    print(f"  Допустим? {engine.validate_move(state, move)}")
    
    captures = engine.get_all_capture_moves(state, 'white')
    print(f"\nВсе взятия для белых: {captures}")
    
    # Проверяем конкретно для (4,7)
    capture_moves = engine._get_capture_moves(state, 4, 7)
    print(f"\nВзятия для (4,7): {capture_moves}")

if __name__ == '__main__':
    test_capture_2()