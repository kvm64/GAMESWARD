import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from services.games import GameEngineFactory

def test_capture():
    print("🎮 Тест взятия в русских шашках (правильная позиция)...")
    
    engine = GameEngineFactory.get_engine('russian_checkers')
    state = engine.get_initial_state()
    
    # Ситуация: белая шашка на (5,2), чёрная на (4,3), пусто на (3,4)
    # Для этого нужно "подготовить" доску вручную
    board = state['board']
    
    # Очищаем доску
    for r in range(8):
        for c in range(8):
            board[r][c] = None
    
    # Ставим белую шашку на (5, 2)
    board[5][2] = {'color': 'white', 'is_king': False}
    # Ставим чёрную шашку на (4, 3)
    board[4][3] = {'color': 'black', 'is_king': False}
    # Клетка (3, 4) пуста — туда прыгнет белая
    
    state['board'] = board
    state['turn'] = 'white'
    
    print("Доска до взятия:")
    print(f"  (5,2): {board[5][2]}")
    print(f"  (4,3): {board[4][3]}")
    print(f"  (3,4): {board[3][4]}")
    
    # Проверяем взятие: (5,2) → (3,4) через (4,3)
    capture_move = {'from': [5, 2], 'to': [3, 4]}
    print(f"\nВзятие: {capture_move}")
    print(f"  Допустимо? {engine.validate_move(state, capture_move)}")
    
    # Проверяем список всех взятий
    captures = engine.get_all_capture_moves(state, 'white')
    print(f"\nВсе взятия для белых: {captures}")
    
    # Применяем взятие
    if engine.validate_move(state, capture_move):
        new_state = engine.apply_move(state, capture_move)
        print(f"\n✅ Взятие применено!")
        print(f"  (5,2) после: {new_state['board'][5][2]}")
        print(f"  (4,3) после: {new_state['board'][4][3]}")  # Должно быть None
        print(f"  (3,4) после: {new_state['board'][3][4]}")  # Белая шашка

if __name__ == '__main__':
    test_capture()