import client from './client';

export const getAvailableGames = () => client.get('/games/available/');
export const getUsers = () => client.get('/users/');

export const createInvitation = (toUserId, gameType, message = '', timeControl = 'unlimited', colorPreference = 'random') => 
  client.post('/invitations/create/', { 
    to_user: toUserId, 
    game_type: gameType,
    message: message,
    time_control: timeControl,
    color_preference: colorPreference,
  });

export const getIncomingInvitations = () => client.get('/invitations/incoming/');
export const getOutgoingInvitations = () => client.get('/invitations/outgoing/');
export const acceptInvitation = (id) => client.post(`/invitations/${id}/accept/`);
export const declineInvitation = (id) => client.post(`/invitations/${id}/decline/`);

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