"""
Движок для шахмат на основе библиотеки python-chess.

python-chess обеспечивает:
- полную валидацию ходов (включая рокировку, en passant, превращение);
- определение шаха, мата, пата, ничьей;
- работу с FEN-нотацией для хранения состояния.
"""
import chess
from .base import GameEngine


class ChessEngine(GameEngine):
    """Движок для шахмат."""

    game_type = "chess"
    game_name = "Шахматы"
    players_count = 2

    def get_initial_state(self) -> dict:
        """Начальная позиция (FEN) + пустая история ходов."""
        board = chess.Board()
        return {
            'fen': board.fen(),
            'turn': 'white',                    # для совместимости с UI
            'winner': None,
            'moves_count': 0,
            'is_draw': False,
            'history': [],                      # SAN-нотация ходов
            'last_move': None,                  # для подсветки последнего хода
            'is_check': False,
            'is_checkmate': False,
            'is_stalemate': False,
        }

    def validate_move(self, state: dict, move: dict) -> bool:
        """Проверяет ход через python-chess."""
        if state.get('winner') is not None or state.get('is_draw'):
            return False

        board = chess.Board(state['fen'])

        from_sq = move.get('from')
        to_sq = move.get('to')
        promotion = move.get('promotion', None)

        if not from_sq or not to_sq:
            return False

        try:
            from_square = chess.parse_square(from_sq)
            to_square = chess.parse_square(to_sq)
        except ValueError:
            return False

        # Ход с превращением?
        if promotion:
            try:
                promotion_piece = chess.Piece.from_symbol(promotion.lower())
            except ValueError:
                return False
            uci_move = chess.Move(from_square, to_square, promotion=promotion_piece.piece_type)
        else:
            uci_move = chess.Move(from_square, to_square)

        return uci_move in board.legal_moves

    def apply_move(self, state: dict, move: dict) -> dict:
        """Применяет ход через python-chess."""
        if not self.validate_move(state, move):
            raise ValueError("Недопустимый ход")

        board = chess.Board(state['fen'])

        from_sq = move['from']
        to_sq = move['to']
        promotion = move.get('promotion', None)

        from_square = chess.parse_square(from_sq)
        to_square = chess.parse_square(to_sq)

        if promotion:
            promotion_piece = chess.Piece.from_symbol(promotion.lower())
            uci_move = chess.Move(from_square, to_square, promotion=promotion_piece.piece_type)
        else:
            # Автоматическое превращение в ферзя (если пешка дошла)
            uci_move = chess.Move(from_square, to_square)
            # Проверяем — если ход пешкой на последнюю горизонталь, добавляем promotion
            piece = board.piece_at(from_square)
            if piece and piece.piece_type == chess.PAWN and to_square in chess.SquareSet(chess.BB_RANK_1 | chess.BB_RANK_8):
                uci_move = chess.Move(from_square, to_square, promotion=chess.QUEEN)

        san = board.san(uci_move)              # SAN-нотация (e4, Nf3, O-O, ...)
        board.push(uci_move)

        # Новое состояние
        new_state = {
            'fen': board.fen(),
            'turn': 'white' if board.turn == chess.WHITE else 'black',
            'winner': None,
            'moves_count': state['moves_count'] + 1,
            'is_draw': False,
            'history': state.get('history', []) + [san],
            'last_move': {'from': from_sq, 'to': to_sq},
            'is_check': board.is_check(),
            'is_checkmate': board.is_checkmate(),
            'is_stalemate': board.is_stalemate(),
        }

        # Проверка окончания партии
        game_over = self.check_game_over(new_state)
        if game_over['is_over']:
            new_state['winner'] = game_over['winner']
            new_state['is_draw'] = (game_over['reason'] == 'draw')

        return new_state

    def check_game_over(self, state: dict) -> dict:
        """Проверяет окончание партии через python-chess."""
        board = chess.Board(state['fen'])

        if board.is_checkmate():
            # Победитель — противоположный тому, чей ход
            winner = 'black' if board.turn == chess.WHITE else 'white'
            return {'is_over': True, 'winner': winner, 'reason': 'checkmate'}

        if board.is_stalemate():
            return {'is_over': True, 'winner': None, 'reason': 'stalemate'}

        if board.is_insufficient_material():
            return {'is_over': True, 'winner': None, 'reason': 'draw'}

        if board.is_seventyfive_moves():
            return {'is_over': True, 'winner': None, 'reason': 'draw'}

        if board.is_fivefold_repetition():
            return {'is_over': True, 'winner': None, 'reason': 'draw'}

        return {'is_over': False, 'winner': None, 'reason': None}