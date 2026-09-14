from abc import ABC, abstractmethod


class GameEngine(ABC):
    """Базовый интерфейс для всех игровых движков.
    
    Каждая игра (шахматы, шашки, крестики-нолики) реализует этот интерфейс.
    Это позволяет GAMESWARD работать с любой игрой единообразно.
    """
    
    # Тип игры (уникальный код): 'chess', 'checkers', 'tictactoe'
    game_type = "base"
    
    # Название игры для отображения
    game_name = "Базовая игра"
    
    # Количество игроков
    players_count = 2
    
    @abstractmethod
    def get_initial_state(self) -> dict:
        """Возвращает начальное состояние игры.
        
        Пример для крестиков-ноликов:
        {
            'board': ['', '', '', '', '', '', '', '', ''],
            'turn': 'X',
            'winner': None,
        }
        """
        pass
    
    @abstractmethod
    def validate_move(self, state: dict, move: dict) -> bool:
        """Проверяет, допустим ли ход.
        
        Возвращает True, если ход легальный, иначе False.
        """
        pass
    
    @abstractmethod
    def apply_move(self, state: dict, move: dict) -> dict:
        """Применяет ход и возвращает новое состояние.
        
        Не изменяет исходное состояние — возвращает копию.
        """
        pass
    
    @abstractmethod
    def check_game_over(self, state: dict) -> dict:
        """Проверяет, закончилась ли игра.
        
        Возвращает:
        {
            'is_over': bool,
            'winner': 'X' | 'O' | None,
            'reason': 'win' | 'draw' | None,
        }
        """
        pass
    
    def get_state_for_player(self, state: dict, player: str) -> dict:
        """Возвращает состояние игры для конкретного игрока.
        
        По умолчанию — полное состояние. Переопределяется в играх
        со скрытой информацией (например, морской бой).
        """
        return state