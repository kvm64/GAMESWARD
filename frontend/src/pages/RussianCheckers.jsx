import React, { useState } from 'react';
import { makeMove, getGameState } from '../api/games';

export default function RussianCheckers({ gameId, initialState }) {
  const [state, setState] = useState(initialState);
  const [selected, setSelected] = useState(null);

  const isDevMode = process.env.REACT_APP_DEV_MODE === 'true';

  const handleCellClick = async (row, col) => {
    const cell = state.board[row][col];

    if (selected) {
      const move = {
        from: [selected.row, selected.col],
        to: [row, col],
      };

      try {
        const response = await makeMove(gameId, move);
        const newState = response.data.metadata.state;
        setState(newState);

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
        setSelected(null);
      }
      return;
    }

    if (cell && cell.color === state.turn) {
      setSelected({ row, col });
    }
  };

  const handleRefresh = async () => {
    try {
      const response = await getGameState(gameId);
      setState(response.data.state);
      setSelected(null);
    } catch (error) {
      console.error('Ошибка обновления:', error.response?.data || error.message);
    }
  };

  if (!state) return <div>Загрузка...</div>;

  const isGameOver = state.winner !== null;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Русские шашки</h2>

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

      {!isGameOver && (
        <p>Ход: <strong>{state.turn === 'white' ? 'Белые' : 'Чёрные'}</strong></p>
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
                      cursor: cell || selected ? 'pointer' : 'default',
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