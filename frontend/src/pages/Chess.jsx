import React, { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess as ChessJS } from 'chess.js';
import { makeMove, resignGame } from '../api/games';

export default function Chess({ gameId, initialState, mySymbol, onNewGame }) {
  const [state, setState] = useState(initialState);
  const [myTurn, setMyTurn] = useState(initialState?.turn === mySymbol);
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  useEffect(() => {
    if (errorMessage) {
      const timer = setTimeout(() => setErrorMessage(null), 4000);
      return () => clearTimeout(timer);
    }
  }, [errorMessage]);

  useEffect(() => {
    if (initialState) {
      setState(initialState);
      setMyTurn(initialState.turn === mySymbol);
    }
  }, [initialState, mySymbol]);

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

  const sendMove = async (from, to) => {
    try {
      const response = await makeMove(gameId, { from, to });
      const newState = response.data.metadata.state;
      setState(newState);
      setMyTurn(newState.turn === mySymbol);
      setSelectedSquare(null);
      setErrorMessage(null);
    } catch (error) {
      console.error('Ошибка хода:', error.response?.data || error.message);
      const serverError = error.response?.data?.error;
      setErrorMessage(serverError || 'Недопустимый ход');
      setSelectedSquare(null);
    }
  };

  const onPieceDrop = ({ sourceSquare, targetSquare }) => {
    if (!myTurn) return false;
    if (state.winner || state.is_draw) return false;
    if (!targetSquare) return false;

    sendMove(sourceSquare, targetSquare);
    return true;
  };

  const onSquareClick = ({ square }) => {
    if (!myTurn) return;
    if (state.winner || state.is_draw) return;

    if (selectedSquare) {
      if (selectedSquare === square) {
        setSelectedSquare(null);
        return;
      }
      sendMove(selectedSquare, square);
      setSelectedSquare(null);
    } else {
      const chess = new ChessJS(state.fen);
      const pieceOnSquare = chess.get(square);
      if (pieceOnSquare && pieceOnSquare.color === (mySymbol === 'white' ? 'w' : 'b')) {
        setSelectedSquare(square);
      }
    }
  };

  if (!state) return <div>Загрузка...</div>;

  const isGameOver = state.winner !== null || state.is_draw;
  const chess = new ChessJS(state.fen);
  const isCheck = chess.isCheck();

  const handleNewGame = () => {
    localStorage.removeItem('currentGame');
    if (onNewGame) {
      onNewGame();
    } else {
      window.location.reload();
    }
  };

  const handleResign = async () => {
    if (!window.confirm('Сдаться? Соперник победит.')) return;
    try {
      await resignGame(gameId);
      window.location.reload();
    } catch (error) {
      console.error('Ошибка сдачи:', error.response?.data || error.message);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px' }}>
      <h2>Шахматы</h2>

      <p style={{ fontSize: '14px', color: '#666' }}>
        Вы играете за:{' '}
        <strong>{mySymbol === 'white' ? 'Белые' : mySymbol === 'black' ? 'Чёрные' : '—'}</strong>
      </p>

      {errorMessage && (
        <div style={{
          padding: '12px 16px',
          backgroundColor: '#FFE5E5',
          border: '2px solid #E17055',
          borderRadius: '4px',
          color: '#C0392B',
          fontWeight: 'bold',
          fontSize: '16px',
          marginBottom: '15px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <span>❌ {errorMessage}</span>
          <button
            onClick={() => setErrorMessage(null)}
            style={{
              background: 'none',
              border: 'none',
              color: '#C0392B',
              fontSize: '20px',
              cursor: 'pointer',
              marginLeft: '10px',
              padding: '0 5px',
            }}
          >
            ×
          </button>
        </div>
      )}

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

      {isCheck && !isGameOver && (
        <p style={{ color: '#E17055', fontWeight: 'bold', fontSize: '18px' }}>
          ⚠️ Шах!
        </p>
      )}

      {state.winner && (
        <p style={{ fontSize: '24px', color: '#6C5CE7', fontWeight: 'bold' }}>
          🏆 Победитель: {state.winner === 'white' ? 'Белые' : 'Чёрные'}
          {state.winner === mySymbol ? ' (Вы!)' : ' (Соперник)'}
        </p>
      )}

      {state.is_checkmate && state.winner && (
        <p style={{ fontSize: '18px', color: '#E17055' }}>Мат!</p>
      )}

      {state.is_stalemate && (
        <p style={{ fontSize: '24px', color: '#888', fontWeight: 'bold' }}>
          🤝 Пат!
        </p>
      )}

      {state.is_draw && !state.is_stalemate && (
        <p style={{ fontSize: '24px', color: '#888', fontWeight: 'bold' }}>
          🤝 Ничья!
        </p>
      )}

      <div style={{ marginTop: '20px', maxWidth: '500px' }}>
        <Chessboard
          options={{
            position: state.fen,
            onPieceDrop: onPieceDrop,
            onSquareClick: onSquareClick,
            boardOrientation: mySymbol === 'black' ? 'black' : 'white',
            squareStyles: selectedSquare ? {
              [selectedSquare]: { backgroundColor: '#F48FB1' },
            } : {},
            allowDragging: myTurn && !isGameOver,
          }}
        />
      </div>

      {state.history && state.history.length > 0 && (
        <div style={{
          marginTop: '20px',
          padding: '10px',
          backgroundColor: '#F5F5F5',
          borderRadius: '4px',
          maxHeight: '150px',
          overflowY: 'auto',
        }}>
          <strong>История:</strong>{' '}
          {state.history.map((move, i) => (
            <span key={i}>
              {Math.floor(i / 2) + 1}.{i % 2 === 1 ? '..' : ''} {move}{' '}
            </span>
          ))}
        </div>
      )}

      <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
        {!isGameOver && (
          <button
            onClick={handleResign}
            style={{
              padding: '10px 20px',
              backgroundColor: '#E17055',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px',
            }}
          >
            🏳️ Сдаться
          </button>
        )}

        {isGameOver && (
          <button
            onClick={handleNewGame}
            style={{
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
    </div>
  );
}