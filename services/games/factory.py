from .base import GameEngine
from .tictactoe import TicTacToeEngine
from .russian_checkers import RussianCheckersEngine


class GameEngineFactory:
    """Фабрика игровых движков.
    
    Возвращает нужный движок по типу игры.
    """
    
    _engines = {
        'tictactoe': TicTacToeEngine,
        'russian_checkers': RussianCheckersEngine,
        # 'chess': ChessEngine,       # будет добавлено позже
    }
    
    @classmethod
    def get_engine(cls, game_type: str) -> GameEngine:
        """Возвращает экземпляр движка для указанной игры."""
        engine_class = cls._engines.get(game_type)
        if not engine_class:
            raise ValueError(f"Неизвестный тип игры: {game_type}")
        return engine_class()
    
    @classmethod
    def get_available_games(cls) -> list:
        """Возвращает список доступных игр."""
        return [
            {
                'type': engine_class.game_type,
                'name': engine_class.game_name,
                'players_count': engine_class.players_count,
            }
            for engine_class in cls._engines.values()
        ]
    
    @classmethod
    def register_engine(cls, game_type: str, engine_class):
        """Регистрирует новый движок (для расширения)."""
        cls._engines[game_type] = engine_class