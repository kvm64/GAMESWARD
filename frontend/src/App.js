import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import { getAvailableGames, createRoom, startGame } from './api/games';
import TicTacToe from './pages/TicTacToe';
import RussianCheckers from './pages/RussianCheckers';
import SelectOpponent from './pages/SelectOpponent';

function App() {
  const [games, setGames] = useState([]);
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [gameType, setGameType] = useState(null);
  const [gameName, setGameName] = useState(null);
  const [selectingOpponent, setSelectingOpponent] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const autoLogin = async () => {
      try {
        const response = await axios.post('/api/v1/auth/login/', {
          username: 'admin',
          password: 'admin123',
        });
        localStorage.setItem('access_token', response.data.access);
        setLoggedIn(true);
        console.log('Авторизован:', response.data.user.username);
      } catch (error) {
        console.error('Ошибка авторизации:', error.response?.data || error.message);
      }
    };
    autoLogin();
  }, []);

  useEffect(() => {
    if (loggedIn) {
      getAvailableGames()
        .then(response => setGames(response.data))
        .catch(error => console.error('Ошибка:', error));
    }
  }, [loggedIn]);

  const handleSelectGame = (type, name) => {
    setGameType(type);
    setGameName(name);
    setSelectingOpponent(true);
  };

  const handleSelectOpponent = async (opponentId) => {
    try {
      const roomResponse = await createRoom(gameType, opponentId);
      const roomId = roomResponse.data.id;
      const gameResponse = await startGame(roomId);
      setGameId(gameResponse.data.id);
      setGameState(gameResponse.data.metadata.state);
      setSelectingOpponent(false);
    } catch (error) {
      console.error('Ошибка создания игры:', error.response?.data || error.message);
    }
  };

  const handleNewGame = () => {
    setGameId(null);
    setGameState(null);
    setGameType(null);
    setGameName(null);
    setSelectingOpponent(false);
  };

  return (
    <BrowserRouter>
      <nav style={{ padding: '10px', backgroundColor: '#6C5CE7', color: 'white' }}>
        <Link to="/" style={{ color: 'white', marginRight: '15px' }} onClick={handleNewGame}>
          Главная
        </Link>
      </nav>

      <Routes>
        <Route path="/" element={
          <div style={{ padding: '20px' }}>
            <h1>GAMESWARD</h1>
            <p>Платформа для настольных игр</p>

            {!loggedIn && <p style={{ color: 'red' }}>Авторизация...</p>}

            {loggedIn && !gameId && !selectingOpponent && (
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
                onSelect={handleSelectOpponent}
                onBack={handleNewGame}
              />
            )}

            {gameId && gameType === 'tictactoe' && (
              <TicTacToe gameId={gameId} initialState={gameState} />
            )}

            {gameId && gameType === 'russian_checkers' && (
              <RussianCheckers gameId={gameId} initialState={gameState} />
            )}
          </div>
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;