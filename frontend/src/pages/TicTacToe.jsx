import React, { useState, useEffect } from 'react';
import { makeMove } from '../api/games';

export default function TicTacToe({ gameId, initialState, mySymbol, onNewGame }) {
  const [state, setState] = useState(initialState);
  const [myTurn, setMyTurn] = useState(initialState?.turn === mySymbol);

  // Синхронизация с initialState
  useEffect(() => {
    if (initialState) {
      setState(initialState);
      setMyTurn(initialState.turn === mySymbol);
    }
  }, [initialState, mySymbol]);

  // Polling: каждые 2 секунды
  useEffect(() => {
    if (!gameId) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`/api/v1/games/${gameId}/state/`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        if (res.ok) {
          const data = await res.json();
          setState(data.state);
          setMyTurn(data.state.turn === mySymbol);
        }
      } catch (error) {
        // Игнорируем
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [gameId, mySymbol]);

  const handleCellClick = async (cell) => {
    if (state.winner !== null || state.is_draw || !state.board.includes('')) {
      return;
    }
    if (!myTurn) return;

    try {
      const response = await makeMove(gameId, { cell });
      setState(response.data.metadata.state);
      setMyTurn(response.data.metadata.state.turn === mySymbol);
    } catch (error) {
      console.error('Ошибка хода:', error.response?.data || error.message);
    }
  };

  if (!state) return <div>Загрузка...</div>;

  const isDraw = state.is_draw || (!state.winner && !state.board.includes(''));
  const isGameOver = state.winner !== null || isDraw;

  const handleReset = () => {
    localStorage.removeItem('currentGame');
    if (onNewGame) {
      onNewGame();
    } else {
      window.location.reload();
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Крестики-нолики</h2>

      <p style={{ fontSize: '14px', color: '#666' }}>
        Вы играете за: <strong>{mySymbol || '—'}</strong>
      </p>

      {!isGameOver && (
        <p style={{
          fontSize: '20px',
          fontWeight: 'bold',
          color: myTurn ? '#00B894' : '#E17055',
          padding: '10px',
          backgroundColor: myTurn ? '#E8F8F5' : '#FFF5F0',
          borderRadius: '4px',
          display: 'inline-block',
        }}>
          {myTurn ? '🟢 Ваш ход!' : '🔴 Ход соперника...'}
        </p>
      )}

      {state.winner && (
        <p style={{ fontSize: '24px', color: '#6C5CE7', fontWeight: 'bold' }}>
          🏆 Победитель: {state.winner} {state.winner === mySymbol ? '(Вы!)' : '(Соперник)'}
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
            disabled={cell !== '' || isGameOver || !myTurn}
            style={{
              width: '100px',
              height: '100px',
              fontSize: '36px',
              fontWeight: 'bold',
              cursor: cell === '' && !isGameOver && myTurn ? 'pointer' : 'not-allowed',
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