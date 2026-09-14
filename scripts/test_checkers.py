import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from services.games import GameEngineFactory

def test_checkers():
    print("🎮 Тест русских шашек...")
    
    engine = GameEngineFactory.get_engine('russian_checkers')
    state = engine.get_initial_state()
    
    print(f"Начальное состояние: ход {state['turn']}")
    
    # Простой ход белой шашкой: с (5, 0) на (4, 1)
    move = {'from': [5, 0], 'to': [4, 1]}
    
    if engine.validate_move(state, move):
        state = engine.apply_move(state, move)
        print(f"✅ Ход выполнен: (5,0) → (4,1)")
        print(f"Теперь ход: {state['turn']}")
    else:
        print("❌ Ход недопустим")
    
    # Проверяем список доступных игр
    print("\n📋 Доступные игры:")
    for game in GameEngineFactory.get_available_games():
        print(f"  - {game['name']} ({game['type']}), игроков: {game['players_count']}")
    
    print("\n🎉 Тест пройден!")

if __name__ == '__main__':
    test_checkers()