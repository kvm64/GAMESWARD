import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { getAvailableGames } from './api/games';
import TicTacToe from './pages/TicTacToe';
import RussianCheckers from './pages/RussianCheckers';
import Chess from './pages/Chess';
import SelectOpponent from './pages/SelectOpponent';
import Invitations from './pages/Invitations';
import Login from './pages/Login';

const CURRENT_GAME_KEY = 'currentGame';

function App() {
  const [games, setGames] = useState([]);
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [gameType, setGameType] = useState(null);
  const [gameName, setGameName] = useState(null);
  const [mySymbol, setMySymbol] = useState(null);
  const [selectingOpponent, setSelectingOpponent] = useState(false);
  const [view, setView] = useState('main');
  const [user, setUser] = useState(null);

  const openedInvitationsRef = useRef(new Set());

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  useEffect(() => {
    if (user) {
      getAvailableGames()
        .then(response => setGames(response.data))
        .catch(error => console.error('Ошибка:', error));
    }
  }, [user]);

  // Восстановление игры из localStorage
  useEffect(() => {
    const savedGame = localStorage.getItem(CURRENT_GAME_KEY);
    if (savedGame && user) {
      try {
        const { gameId: savedId, gameType: savedType } = JSON.parse(savedGame);
        if (savedId && savedType) {
          fetch(`/api/v1/games/${savedId}/state/`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
          })
            .then(res => {
              if (!res.ok) throw new Error('Игра не найдена');
              return res.json();
            })
            .then(data => {
              setGameId(savedId);
              setGameType(savedType);
              setGameState(data.state);
              setMySymbol(data.my_symbol);
              setView('main');
            })
            .catch(error => {
              console.error('Не удалось восстановить игру:', error);
              localStorage.removeItem(CURRENT_GAME_KEY);
            });
        }
      } catch (error) {
        console.error('Ошибка парсинга currentGame:', error);
        localStorage.removeItem(CURRENT_GAME_KEY);
      }
    }
  }, [user]);

  // Polling исходящих приглашений
  useEffect(() => {
    if (!user || gameId) return;

    const checkOutgoing = async () => {
      try {
        const res = await fetch('/api/v1/invitations/outgoing/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        if (!res.ok) return;

        const data = await res.json();
        const accepted = data.find(
          inv => inv.status === 'accepted'
            && inv.game_id
            && !openedInvitationsRef.current.has(inv.id)
        );

        if (accepted && !gameId) {
          openedInvitationsRef.current.add(accepted.id);
          console.log('Соперник принял приглашение, открываем игру:', accepted);
          handleGameStarted(accepted.game_type, accepted.game_id, accepted.room_id);
        }
      } catch (error) {
        // Игнорируем
      }
    };

    const interval = setInterval(checkOutgoing, 3000);
    checkOutgoing();

    return () => clearInterval(interval);
  }, [user, gameId]);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    localStorage.removeItem(CURRENT_GAME_KEY);
    setUser(null);
    setGameId(null);
    setGameState(null);
    setGameType(null);
    setGameName(null);
    setMySymbol(null);
    setSelectingOpponent(false);
    setView('main');
    openedInvitationsRef.current.clear();
  };

  const handleSelectGame = (type, name) => {
    setGameType(type);
    setGameName(name);
    setSelectingOpponent(true);
  };

  const handleInvitationSent = () => {
    setSelectingOpponent(false);
    setView('invitations');
    alert('Приглашение отправлено!');
  };

  const handleGameStarted = (newGameType, newGameId, roomId) => {
    setGameType(newGameType);
    setGameId(newGameId);
    setView('main');

    localStorage.setItem(CURRENT_GAME_KEY, JSON.stringify({
      gameId: newGameId,
      gameType: newGameType,
      roomId: roomId,
    }));

    fetch(`/api/v1/games/${newGameId}/state/`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    })
      .then(res => res.json())
      .then(data => {
        setGameState(data.state);
        setMySymbol(data.my_symbol);
      })
      .catch(error => console.error('Ошибка загрузки игры:', error));
  };

  const handleNewGame = () => {
    setGameId(null);
    setGameState(null);
    setGameType(null);
    setGameName(null);
    setMySymbol(null);
    setSelectingOpponent(false);
    setView('main');
    localStorage.removeItem(CURRENT_GAME_KEY);
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <BrowserRouter>
      <nav style={{
        padding: '10px',
        backgroundColor: '#6C5CE7',
        color: 'white',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <div>
          <Link to="/" style={{ color: 'white', marginRight: '15px' }} onClick={handleNewGame}>
            Главная
          </Link>
          <button
            onClick={() => setView('invitations')}
            style={{
              color: 'white',
              backgroundColor: 'transparent',
              border: '1px solid white',
              borderRadius: '4px',
              padding: '5px 10px',
              cursor: 'pointer',
              marginRight: '10px',
            }}
          >
            📨 Мои приглашения
          </button>
          {gameId && (
            <button
              onClick={handleNewGame}
              style={{
                color: 'white',
                backgroundColor: 'transparent',
                border: '1px solid white',
                borderRadius: '4px',
                padding: '5px 10px',
                cursor: 'pointer',
              }}
            >
              🚪 Выйти из игры
            </button>
          )}
        </div>
        <div>
          <span style={{ marginRight: '15px' }}>
            👤 {user.username}
          </span>
          <button
            onClick={handleLogout}
            style={{
              color: 'white',
              backgroundColor: 'transparent',
              border: '1px solid white',
              borderRadius: '4px',
              padding: '5px 10px',
              cursor: 'pointer',
            }}
          >
            Выйти
          </button>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={
          <div style={{ padding: '20px' }}>
            <h1>GAMESWARD</h1>
            <p>Платформа для настольных игр</p>

            {view === 'invitations' && (
              <Invitations onGameStarted={handleGameStarted} />
            )}

            {view === 'main' && !gameId && !selectingOpponent && (
              <>
                <h2>Доступные игры</h2>
                {games.map(game => (
                  <div key={game.type} style={{ margin: '10px 0' }}>
                    <button
                      onClick={() => handleSelectGame(game.type, game.name)}
                      style={{
                        padding: '10px 20px',
                        backgroundColor: '#6C5CE7',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                      }}
                    >
                      Начать игру: {game.name}
                    </button>
                  </div>
                ))}
              </>
            )}

            {selectingOpponent && (
              <SelectOpponent
                gameType={gameType}
                gameName={gameName}
                onBack={handleNewGame}
                onInvitationSent={handleInvitationSent}
              />
            )}

            {gameId && gameType === 'tictactoe' && gameState && (
              <TicTacToe
                gameId={gameId}
                initialState={gameState}
                mySymbol={mySymbol}
                onNewGame={handleNewGame}
              />
            )}

            {gameId && gameType === 'russian_checkers' && gameState && (
              <RussianCheckers
                gameId={gameId}
                initialState={gameState}
                mySymbol={mySymbol}
                onNewGame={handleNewGame}
              />
            )}

            {gameId && gameType === 'chess' && gameState && (
              <Chess
                gameId={gameId}
                initialState={gameState}
                mySymbol={mySymbol}
                onNewGame={handleNewGame}
              />
            )}
          </div>
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;