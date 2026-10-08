from .base import GameEngine


class RussianCheckersEngine(GameEngine):
    """Движок для русских шашек."""

    game_type = "russian_checkers"
    game_name = "Русские шашки"
    players_count = 2
    BOARD_SIZE = 8
    MOVES_WITHOUT_CAPTURE_LIMIT = 15  # Ничья, если 15 ходов без взятий

    def get_initial_state(self) -> dict:
        board = [[None] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]

        for row in range(3):
            for col in range(self.BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = {'color': 'black', 'is_king': False}

        for row in range(5, 8):
            for col in range(self.BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = {'color': 'white', 'is_king': False}

        return {
            'board': board,
            'turn': 'white',
            'winner': None,
            'moves_count': 0,
            'must_continue': False,
            'continue_from': None,
            'is_draw': False,
            'moves_without_capture': 0,
        }

    def _get_direction(self, color):
        return -1 if color == 'white' else 1

    def _get_capture_moves(self, state, row, col):
        piece = state['board'][row][col]
        if not piece:
            return []

        captures = []
        directions = [-1, 1]

        if not piece['is_king']:
            row_dirs = [self._get_direction(piece['color'])]
        else:
            row_dirs = directions

        for dr in row_dirs:
            for dc in directions:
                mid_row = row + dr
                mid_col = col + dc
                to_row = row + 2 * dr
                to_col = col + 2 * dc

                if not (0 <= to_row < 8 and 0 <= to_col < 8):
                    continue
                if not (0 <= mid_row < 8 and 0 <= mid_col < 8):
                    continue

                mid_piece = state['board'][mid_row][mid_col]
                target = state['board'][to_row][to_col]

                if mid_piece and mid_piece['color'] != piece['color'] and target is None:
                    captures.append({
                        'from': [row, col],
                        'to': [to_row, to_col],
                        'captured': [mid_row, mid_col],
                    })

        return captures

    def get_all_capture_moves(self, state, color):
        captures = []
        for row in range(8):
            for col in range(8):
                piece = state['board'][row][col]
                if piece and piece['color'] == color:
                    captures.extend(self._get_capture_moves(state, row, col))
        return captures

    def _get_simple_moves(self, state, row, col):
        """Простые ходы (без взятия) для фигуры."""
        piece = state['board'][row][col]
        if not piece:
            return []

        moves = []
        directions = [-1, 1]

        if not piece['is_king']:
            row_dirs = [self._get_direction(piece['color'])]
        else:
            row_dirs = directions

        for dr in row_dirs:
            for dc in directions:
                to_row = row + dr
                to_col = col + dc

                if not (0 <= to_row < 8 and 0 <= to_col < 8):
                    continue

                if state['board'][to_row][to_col] is None:
                    moves.append({
                        'from': [row, col],
                        'to': [to_row, to_col],
                    })
                    # Для дамки — продолжаем в том же направлении
                    if piece['is_king']:
                        r, c = to_row, to_col
                        while True:
                            r += dr
                            c += dc
                            if not (0 <= r < 8 and 0 <= c < 8):
                                break
                            if state['board'][r][c] is not None:
                                break
                            moves.append({
                                'from': [row, col],
                                'to': [r, c],
                            })

        return moves

    def get_all_simple_moves(self, state, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = state['board'][row][col]
                if piece and piece['color'] == color:
                    moves.extend(self._get_simple_moves(state, row, col))
        return moves

    def validate_move(self, state: dict, move: dict) -> bool:
        if state['winner'] is not None:
            return False

        from_pos = move.get('from')
        to_pos = move.get('to')

        if not from_pos or not to_pos:
            return False

        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if not (0 <= from_row < 8 and 0 <= from_col < 8):
            return False
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False

        piece = state['board'][from_row][from_col]

        if not piece or piece['color'] != state['turn']:
            return False

        if state['board'][to_row][to_col] is not None:
            return False

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        is_capture = abs(row_diff) == 2 and abs(col_diff) == 2

        # Если есть обязательные взятия — только они разрешены
        all_captures = self.get_all_capture_moves(state, state['turn'])
        if all_captures and not is_capture:
            return False

        if is_capture:
            capture_moves = self._get_capture_moves(state, from_row, from_col)
            for cap in capture_moves:
                if cap['to'] == [to_row, to_col]:
                    return True
            return False

        # Простой ход
        if not piece['is_king']:
            direction = self._get_direction(piece['color'])
            if row_diff != direction:
                return False
            if abs(col_diff) != 1:
                return False
        else:
            # Дамка — по диагонали, на любое расстояние, без препятствий
            if abs(row_diff) != abs(col_diff):
                return False
            dr = 1 if row_diff > 0 else -1
            dc = 1 if col_diff > 0 else -1
            steps = abs(row_diff)
            for i in range(1, steps):
                r = from_row + dr * i
                c = from_col + dc * i
                if state['board'][r][c] is not None:
                    return False

        return True

    def apply_move(self, state: dict, move: dict) -> dict:
        if not self.validate_move(state, move):
            raise ValueError("Недопустимый ход")

        new_board = [row.copy() for row in state['board']]
        from_row, from_col = move['from']
        to_row, to_col = move['to']

        row_diff = to_row - from_row
        col_diff = to_col - from_col

        piece = new_board[from_row][from_col]

        is_capture = abs(row_diff) == 2 and abs(col_diff) == 2
        if is_capture:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            new_board[mid_row][mid_col] = None

        new_board[to_row][to_col] = piece
        new_board[from_row][from_col] = None

        if piece['color'] == 'white' and to_row == 0:
            piece['is_king'] = True
        elif piece['color'] == 'black' and to_row == 7:
            piece['is_king'] = True

        # Счётчик ходов без взятий
        moves_without_capture = state.get('moves_without_capture', 0)
        if is_capture:
            moves_without_capture = 0
        else:
            moves_without_capture += 1

        new_state = {
            'board': new_board,
            'turn': state['turn'],
            'winner': None,
            'moves_count': state['moves_count'] + 1,
            'must_continue': False,
            'continue_from': None,
            'is_draw': False,
            'moves_without_capture': moves_without_capture,
        }

        if is_capture:
            further_captures = self._get_capture_moves(new_state, to_row, to_col)
            if further_captures:
                new_state['must_continue'] = True
                new_state['continue_from'] = [to_row, to_col]
                return new_state

        new_state['turn'] = 'black' if state['turn'] == 'white' else 'white'

        game_over = self.check_game_over(new_state)
        if game_over['is_over']:
            new_state['winner'] = game_over['winner']
            new_state['is_draw'] = (game_over['reason'] == 'draw')

        return new_state

    def check_game_over(self, state: dict) -> dict:
        white_count = 0
        black_count = 0
        white_kings = 0
        black_kings = 0
        white_simple = 0
        black_simple = 0

        for row in state['board']:
            for cell in row:
                if cell:
                    if cell['color'] == 'white':
                        white_count += 1
                        if cell['is_king']:
                            white_kings += 1
                        else:
                            white_simple += 1
                    else:
                        black_count += 1
                        if cell['is_king']:
                            black_kings += 1
                        else:
                            black_simple += 1

        # 1. Победа по количеству фигур
        if white_count == 0:
            return {'is_over': True, 'winner': 'black', 'reason': 'no_pieces'}
        if black_count == 0:
            return {'is_over': True, 'winner': 'white', 'reason': 'no_pieces'}

        # 2. Ничья: 15 ходов без взятий (правило русских шашек)
        if state.get('moves_without_capture', 0) >= self.MOVES_WITHOUT_CAPTURE_LIMIT:
            return {'is_over': True, 'winner': None, 'reason': 'draw'}

        # 3. Ничья по материалу:
        #    - 1 дамка против 1 дамки
        #    - 1 дамка против 1 простой
        total = white_count + black_count
        if total == 2 and white_kings == 1 and black_kings == 1:
            return {'is_over': True, 'winner': None, 'reason': 'draw'}
        if total == 2 and ((white_kings == 1 and black_simple == 1) or
                           (black_kings == 1 and white_simple == 1)):
            return {'is_over': True, 'winner': None, 'reason': 'draw'}

        # 4. Проверка на отсутствие ходов у текущего игрока (пат)
        current_color = state['turn']
        captures = self.get_all_capture_moves(state, current_color)
        simple = self.get_all_simple_moves(state, current_color)
        if not captures and not simple:
            opponent = 'black' if current_color == 'white' else 'white'
            return {'is_over': True, 'winner': opponent, 'reason': 'no_moves'}

        return {'is_over': False, 'winner': None, 'reason': None}