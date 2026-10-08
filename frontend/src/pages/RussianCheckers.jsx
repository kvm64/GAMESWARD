import React, { useState, useEffect } from 'react';
import { makeMove, getGameState } from '../api/games';

export default function RussianCheckers({ gameId, initialState, mySymbol, onNewGame }) {
  const [state, setState] = useState(initialState);
  const [selected, setSelected] = useState(null);
  const [myTurn, setMyTurn] = useState(initialState?.turn === mySymbol);
  const [errorMessage, setErrorMessage] = useState(null);   // ← НОВОЕ

  const isDevMode = process.env.REACT_APP_DEV_MODE === 'true';

  // Автоочистка сообщения через 4 секунды
  useEffect(() => {
    if (errorMessage) {
      const timer = setTimeout(() => setErrorMessage(null), 4000);
      return () => clearTimeout(timer);
    }
  }, [errorMessage]);

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
        const response = await getGameState(gameId);
        const data = response.data.state;
        setState(data);
        setMyTurn(data.turn === mySymbol);
      } catch (error) {
        // Игнорируем
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [gameId, mySymbol]);

  const handleCellClick = async (row, col) => {
    if (state.winner !== null || state.is_draw) return;
    if (!myTurn) return;

    const cell = state.board[row][col];

    // Если уже выбрана шашка — пробуем сделать ход
    if (selected) {
      const move = {
        from: [selected.row, selected.col],
        to: [row, col],
      };

      try {
        const response = await makeMove(gameId, move);
        const newState = response.data.metadata.state;
        setState(newState);
        setMyTurn(newState.turn === mySymbol);
        setErrorMessage(null);   // ← сбрасываем при успехе

        if (newState.must_continue && newState.continue_from) {
          setSelected({
            row: newState.continue_from[0],
            col: newState.continue_from[1],
          });
        } else {
          setSelected(null);
        }
      } catch (error) {
        console.error('Ошибка хода:', error.response?.data || error.message);
        // Показываем сообщение об ошибке
        const serverError = error.response?.data?.error;
        setErrorMessage(serverError || 'Недопустимый ход');   // ← НОВОЕ
        setSelected(null);
      }
      return;
    }

    // Если клик по своей шашке — выбираем
    if (cell && cell.color === state.turn) {
      setSelected({ row, col });
    }
  };

  const handleRefresh = async () => {
    try {
      const response = await getGameState(gameId);
      setState(response.data.state);
      setMyTurn(response.data.state.turn === mySymbol);
      setSelected(null);
      setErrorMessage(null);
    } catch (error) {
      console.error('Ошибка обновления:', error.response?.data || error.message);
    }
  };

  const handleNewGame = () => {
    localStorage.removeItem('currentGame');
    if (onNewGame) {
      onNewGame();
    } else {
      window.location.reload();
    }
  };

  if (!state) return <div>Загрузка...</div>;

  const isDraw = state.is_draw;
  const isGameOver = state.winner !== null || isDraw;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Русские шашки</h2>

      <p style={{ fontSize: '14px', color: '#666' }}>
        Вы играете за: <strong>{mySymbol === 'white' ? 'Белые' : mySymbol === 'black' ? 'Чёрные' : '—'}</strong>
      </p>

      {isDevMode && (
        <button
          onClick={handleRefresh}
          style={{
            padding: '8px 16px',
            backgroundColor: '#0984E3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginBottom: '15px',
            fontSize: '14px',
          }}
        >
          🔄 Обновить состояние (dev)
        </button>
      )}

      {/* Сообщение об ошибке хода */}
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
          maxWidth: '400px',
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

      {selected && (
        <p style={{ color: '#6C5CE7', fontWeight: 'bold', minHeight: '24px' }}>
          {`Выбрана шашка: ${String.fromCharCode(97 + selected.col)}${8 - selected.row} (${selected.row}, ${selected.col})`}
        </p>
      )}

      {!selected && (
        <p style={{ minHeight: '24px' }}>{'\u00A0'}</p>
      )}

      {state.must_continue && (
        <p style={{ color: '#E17055', fontWeight: 'bold' }}>
          ⚔️ Продолжите взятие!
        </p>
      )}

      {state.winner && (
        <p style={{ fontSize: '24px', color: '#6C5CE7', fontWeight: 'bold' }}>
          🏆 Победитель: {state.winner === 'white' ? 'Белые' : 'Чёрные'}
          {state.winner === mySymbol ? ' (Вы!)' : ' (Соперник)'}
        </p>
      )}

      {isDraw && (
        <p style={{ fontSize: '24px', color: '#888', fontWeight: 'bold' }}>
          🤝 Ничья!
        </p>
      )}

      <div style={{ position: 'relative', marginTop: '20px' }}>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(8, 60px)',
          marginLeft: '30px',
          marginBottom: '4px',
        }}>
          {['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].map(letter => (
            <div key={letter} style={{ textAlign: 'center', fontSize: '14px', fontWeight: 'bold', color: '#6C5CE7' }}>
              {letter}
            </div>
          ))}
        </div>

        <div style={{ display: 'flex' }}>

          <div style={{
            display: 'grid',
            gridTemplateRows: 'repeat(8, 60px)',
            marginRight: '4px',
          }}>
            {[8, 7, 6, 5, 4, 3, 2, 1].map(num => (
              <div key={num} style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#6C5CE7',
                width: '26px',
              }}>
                {num}
              </div>
            ))}
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(8, 60px)',
            gridTemplateRows: 'repeat(8, 60px)',
            border: '4px solid #6C5CE7',
          }}>
            {state.board.map((row, rowIndex) =>
              row.map((cell, colIndex) => {
                const isDark = (rowIndex + colIndex) % 2 === 1;
                const isSelected = selected && selected.row === rowIndex && selected.col === colIndex;

                const isMustContinue =
                  state.must_continue &&
                  state.continue_from &&
                  state.continue_from[0] === rowIndex &&
                  state.continue_from[1] === colIndex;

                return (
                  <div
                    key={`${rowIndex}-${colIndex}`}
                    onClick={() => handleCellClick(rowIndex, colIndex)}
                    style={{
                      width: '60px',
                      height: '60px',
                      backgroundColor: isDark ? '#6C5CE7' : '#E6E6FA',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      cursor: (cell || selected) && !isGameOver && myTurn ? 'pointer' : 'default',
                      position: 'relative',
                    }}
                  >
                    {cell && (
                      <div style={{
                        width: '44px',
                        height: '44px',
                        borderRadius: '50%',
                        backgroundColor: cell.color === 'white' ? '#FFFFFF' : '#000000',
                        border: '2px solid ' + (cell.color === 'white' ? '#888' : '#FFF'),
                        boxShadow: isSelected ? '0 0 0 4px #F48FB1' : '0 2px 4px rgba(0,0,0,0.3)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '20px',
                        animation: isMustContinue ? 'pulse 1s ease-in-out infinite' : 'none',
                      }}>
                        {cell.is_king && '👑'}
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>

          <div style={{
            display: 'grid',
            gridTemplateRows: 'repeat(8, 60px)',
            marginLeft: '4px',
          }}>
            {[8, 7, 6, 5, 4, 3, 2, 1].map(num => (
              <div key={num} style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '14px',
                fontWeight: 'bold',
                color: '#6C5CE7',
                width: '26px',
              }}>
                {num}
              </div>
            ))}
          </div>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(8, 60px)',
          marginLeft: '30px',
          marginTop: '4px',
        }}>
          {['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].map(letter => (
            <div key={letter} style={{ textAlign: 'center', fontSize: '14px', fontWeight: 'bold', color: '#6C5CE7' }}>
              {letter}
            </div>
          ))}
        </div>

      </div>

      {isGameOver && (
        <button
          onClick={handleNewGame}
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

      <style>
        {`
          @keyframes pulse {
            0% { box-shadow: 0 0 0 4px #F48FB1; }
            50% { box-shadow: 0 0 0 8px #F48FB1, 0 0 15px 4px #F48FB1; }
            100% { box-shadow: 0 0 0 4px #F48FB1; }
          }
        `}
      </style>
    </div>
  );
}