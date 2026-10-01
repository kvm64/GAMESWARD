import React, { useState, useEffect } from 'react';
import { makeMove } from '../api/games';

export default function TicTacToe({ gameId, initialState }) {
  const [state, setState] = useState(initialState);

  // Синхронизация: если initialState обновился (например, после fetch в App.js),
  // обновляем локальный state
  useEffect(() => {
    if (initialState) {
      setState(initialState);
    }
  }, [initialState]);

  const handleCellClick = async (cell) => {
    // Не даём ходить, если игра окончена
    if (state.winner !== null || !state.board.includes('')) {
      return;
    }

    try {
      const response = await makeMove(gameId, { cell });
      setState(response.data.metadata.state);
    } catch (error) {
      console.error('Ошибка хода:', error.response?.data || error.message);
    }
  };

  if (!state) return <div>Загрузка...</div>;

  // Проверяем, закончилась ли игра
  const isDraw = !state.winner && !state.board.includes('');
  const isGameOver = state.winner !== null || isDraw;

  const handleReset = () => {
    window.location.reload();
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Крестики-нолики</h2>

      {!isGameOver && (
        <p>Ход: <strong>{state.turn}</strong></p>
      )}

      {state.winner && (
        <p style={{ fontSize: '24px', color: '#6C5CE7', fontWeight: 'bold' }}>
          🏆 Победитель: {state.winner}
        </p>
      )}

      {isDraw && (
        <p style={{ fontSize: '24px', color: '#888', fontWeight: 'bold' }}>
          🤝 Ничья!
        </p>
      )}

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 100px)',
        gap: '5px',
        marginTop: '20px',
      }}>
        {state.board.map((cell, index) => (
          <button
            key={index}
            onClick={() => handleCellClick(index)}
            disabled={cell !== '' || isGameOver}
            style={{
              width: '100px',
              height: '100px',
              fontSize: '36px',
              fontWeight: 'bold',
              cursor: cell === '' && !isGameOver ? 'pointer' : 'not-allowed',
              backgroundColor: cell === 'X' ? '#E3F2FD' : cell === 'O' ? '#FCE4EC' : '#f0f0f0',
              border: '2px solid #6C5CE7',
              borderRadius: '4px',
            }}
          >
            {cell}
          </button>
        ))}
      </div>

      {isGameOver && (
        <button
          onClick={handleReset}
          style={{
            marginTop: '20px',
            padding: '10px 20px',
            backgroundColor: '#6C5CE7',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '16px',
          }}
        >
          Новая игра
        </button>
      )}
    </div>
  );
}