import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from services.games import GameEngineFactory

def test_tictactoe():
    print("🎮 Тест крестиков-ноликов...")
    
    engine = GameEngineFactory.get_engine('tictactoe')
    state = engine.get_initial_state()
    
    print(f"Начальное состояние: {state}")
    
    # Играем: X на 0, O на 3, X на 1, O на 4, X на 2 (победа X)
    moves = [0, 3, 1, 4, 2]
    
    for cell in moves:
        move = {'cell': cell}
        if engine.validate_move(state, move):
            state = engine.apply_move(state, move)
            print(f"Ход {state['board'][cell]} на {cell}: {state}")
            
            game_over = engine.check_game_over(state)
            if game_over['is_over']:
                print(f"🏆 Игра окончена! Победитель: {game_over['winner']}")
                break
    
    print("🎉 Тест пройден!")

if __name__ == '__main__':
    test_tictactoe()