import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from services.games import GameEngineFactory

def test_win():
    print("🎮 Тест выигрыша O...")
    
    engine = GameEngineFactory.get_engine('tictactoe')
    state = engine.get_initial_state()
    
    # Играем: X на 0, O на 3, X на 2, O на 4, X на 6, O на 5 (победа O)
    moves = [0, 3, 2, 4, 6, 5]
    
    for i, cell in enumerate(moves):
        move = {'cell': cell}
        if engine.validate_move(state, move):
            state = engine.apply_move(state, move)
            print(f"\nХод {i+1} ({state['board'][cell]} на {cell}):")
            print(f"  Доска: {state['board']}")
            print(f"  Winner: {state['winner']}")
            print(f"  Turn: {state['turn']}")
            
            game_over = engine.check_game_over(state)
            print(f"  Game over: {game_over}")
    
    print("\n🎉 Тест завершён!")

if __name__ == '__main__':
    test_win()