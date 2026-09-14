import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from services.games import GameEngineFactory

def test_dual_capture():
    print("🎮 Тест: одна шашка, два варианта взятия...")
    
    engine = GameEngineFactory.get_engine('russian_checkers')
    state = engine.get_initial_state()
    
    for r in range(8):
        for c in range(8):
            state['board'][r][c] = None
    
    # Белая на d4 (4,3), чёрная на e5 (3,4), белая на f4 (4,5)
    state['board'][4][3] = {'color': 'white', 'is_king': False}
    state['board'][3][4] = {'color': 'black', 'is_king': False}
    state['board'][4][5] = {'color': 'white', 'is_king': False}
    state['turn'] = 'white'
    
    print("Позиция:")
    print("  Белая d4 (4,3)")
    print("  Чёрная e5 (3,4)")
    print("  Белая f4 (4,5)")
    
    captures = engine.get_all_capture_moves(state, 'white')
    print(f"\nВсе взятия для белых: {captures}")
    
    cap_d4 = engine._get_capture_moves(state, 4, 3)
    print(f"\nВзятия для d4 (4,3): {cap_d4}")
    
    cap_f4 = engine._get_capture_moves(state, 4, 5)
    print(f"Взятия для f4 (4,5): {cap_f4}")
    
    move1 = {'from': [4, 3], 'to': [2, 5]}
    print(f"\nХод d4 → f6: {move1}")
    print(f"  Допустим? {engine.validate_move(state, move1)}")
    
    move2 = {'from': [4, 5], 'to': [2, 3]}
    print(f"\nХод f4 → d6: {move2}")
    print(f"  Допустим? {engine.validate_move(state, move2)}")

if __name__ == '__main__':
    test_dual_capture()