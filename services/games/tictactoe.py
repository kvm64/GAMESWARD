from .base import GameEngine


class TicTacToeEngine(GameEngine):
    """Движок для крестиков-ноликов."""
    
    game_type = "tictactoe"
    game_name = "Крестики-нолики"
    players_count = 2
    
    # Все выигрышные комбинации
    WINNING_COMBOS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
        [0, 4, 8], [2, 4, 6],              # Диагонали
    ]
    
    def get_initial_state(self) -> dict:
        return {
            'board': [''] * 9,
            'turn': 'X',
            'winner': None,
            'moves_count': 0,
        }
    
    def validate_move(self, state: dict, move: dict) -> bool:
        # Ход — это номер клетки (0-8)
        cell = move.get('cell')
        
        if cell is None or not (0 <= cell <= 8):
            return False
        
        if state['board'][cell] != '':
            return False
        
        if state['winner'] is not None:
            return False
        
        return True
    
    def apply_move(self, state: dict, move: dict) -> dict:
        if not self.validate_move(state, move):
            raise ValueError("Недопустимый ход")
        
        # Копируем состояние
        new_state = {
            'board': state['board'].copy(),
            'turn': state['turn'],
            'winner': state['winner'],
            'moves_count': state['moves_count'] + 1,
        }
        
        cell = move['cell']
        new_state['board'][cell] = state['turn']
        
        # Проверяем окончание
        game_over = self.check_game_over(new_state)
        if game_over['is_over']:
            new_state['winner'] = game_over['winner']
        else:
            # Меняем ход
            new_state['turn'] = 'O' if state['turn'] == 'X' else 'X'
        
        return new_state
    
    def check_game_over(self, state: dict) -> dict:
        board = state['board']
        
        # Проверяем выигрышные комбинации
        for combo in self.WINNING_COMBOS:
            a, b, c = combo
            if board[a] != '' and board[a] == board[b] == board[c]:
                return {
                    'is_over': True,
                    'winner': board[a],
                    'reason': 'win',
                }
        
        # Проверяем ничью
        if '' not in board:
            return {
                'is_over': True,
                'winner': None,
                'reason': 'draw',
            }
        
        return {
            'is_over': False,
            'winner': None,
            'reason': None,
        }