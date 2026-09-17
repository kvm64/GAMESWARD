import client from './client';

export const getAvailableGames = () => client.get('/games/available/');
export const getUsers = () => client.get('/users/');

export const createRoom = (gameType, opponentId) => 
  client.post('/games/rooms/create/', { 
    game_type: gameType, 
    opponent_id: opponentId 
  });

export const startGame = (roomId) => 
  client.post(`/games/rooms/${roomId}/start/`);

export const makeMove = (gameId, move) => 
  client.post(`/games/${gameId}/move/`, { move });

export const getGameState = (gameId) => 
  client.get(`/games/${gameId}/state/`);