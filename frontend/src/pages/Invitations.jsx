import React, { useState, useEffect } from 'react';
import client from '../api/client';

export default function Invitations({ onGameStarted }) {
  const [incoming, setIncoming] = useState([]);
  const [outgoing, setOutgoing] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState('incoming');

  const loadInvitations = async () => {
    try {
      const [incomingRes, outgoingRes] = await Promise.all([
        client.get('/invitations/incoming/'),
        client.get('/invitations/outgoing/'),
      ]);
      setIncoming(incomingRes.data);
      setOutgoing(outgoingRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Ошибка загрузки:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInvitations();
    // Обновляем каждые 10 секунд
    const interval = setInterval(loadInvitations, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleAccept = async (invitationId) => {
    try {
      const response = await client.post(`/invitations/${invitationId}/accept/`);
      console.log('Принято:', response.data);
	  //alert('Ответ сервера: ' + JSON.stringify(response.data));   // ← успех
      if (onGameStarted) {
        onGameStarted(
          response.data.game_type,   // ← тип игры
          response.data.game_id,     // ← id игры
          response.data.room_id      // ← id комнаты
        );
      }
    } catch (error) {
      console.error('Ошибка принятия:', error);
	  //alert('Ошибка: ' + error.message);   // ← временно
    }
  };

  const handleDecline = async (invitationId) => {
    try {
      await client.post(`/invitations/${invitationId}/decline/`);
      loadInvitations();
    } catch (error) {
      console.error('Ошибка отклонения:', error);
    }
  };

  if (loading) return <div>Загрузка приглашений...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Мои приглашения</h2>

      {/* Табы */}
      <div style={{ marginBottom: '20px' }}>
        <button
          onClick={() => setTab('incoming')}
          style={{
            padding: '8px 16px',
            marginRight: '10px',
            backgroundColor: tab === 'incoming' ? '#6C5CE7' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Входящие ({incoming.length})
        </button>
        <button
          onClick={() => setTab('outgoing')}
          style={{
            padding: '8px 16px',
            backgroundColor: tab === 'outgoing' ? '#6C5CE7' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Исходящие ({outgoing.length})
        </button>
      </div>

      {/* Список */}
      {tab === 'incoming' && (
        <div>
          {incoming.length === 0 ? (
            <p style={{ color: '#888' }}>Нет входящих приглашений</p>
          ) : (
            incoming.map(inv => (
              <div
                key={inv.id}
                style={{
                  padding: '15px',
                  margin: '10px 0',
                  backgroundColor: 'white',
                  border: '2px solid #6C5CE7',
                  borderRadius: '8px',
                  maxWidth: '600px',
                }}
              >
                <div style={{ marginBottom: '10px' }}>
                  <strong>{inv.from_user_username}</strong> приглашает на игру
                  <strong> {inv.game_type}</strong>
                </div>
                {inv.message && (
                  <div style={{ color: '#666', marginBottom: '10px', fontStyle: 'italic' }}>
                    "{inv.message}"
                  </div>
                )}
                <div style={{ fontSize: '12px', color: '#888', marginBottom: '10px' }}>
                  Контроль времени: {inv.time_control}
                </div>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button
                    onClick={() => handleAccept(inv.id)}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: '#00B894',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                    }}
                  >
                    Принять
                  </button>
                  <button
                    onClick={() => handleDecline(inv.id)}
                    style={{
                      padding: '8px 16px',
                      backgroundColor: '#E17055',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                    }}
                  >
                    Отклонить
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {tab === 'outgoing' && (
        <div>
          {outgoing.length === 0 ? (
            <p style={{ color: '#888' }}>Нет исходящих приглашений</p>
          ) : (
            outgoing.map(inv => (
              <div
                key={inv.id}
                style={{
                  padding: '15px',
                  margin: '10px 0',
                  backgroundColor: 'white',
                  border: '2px solid #ccc',
                  borderRadius: '8px',
                  maxWidth: '600px',
                }}
              >
                <div>
                  Кому: <strong>{inv.to_user_username}</strong> ({inv.game_type})
                </div>
                <div style={{ fontSize: '12px', color: '#888', marginTop: '5px' }}>
                  Статус: <strong>{inv.status}</strong>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}