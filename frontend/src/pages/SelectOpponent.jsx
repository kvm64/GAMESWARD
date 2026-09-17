import React, { useState, useEffect } from 'react';
import { getUsers } from '../api/games';

export default function SelectOpponent({ gameType, gameName, onSelect, onBack }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getUsers()
      .then(response => {
        setUsers(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ошибка загрузки пользователей:', error);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Загрузка пользователей...</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Выбор противника</h2>
      <p>Игра: <strong>{gameName}</strong></p>

      <button
        onClick={onBack}
        style={{
          padding: '8px 16px',
          backgroundColor: '#888',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          marginBottom: '15px',
        }}
      >
        ← Назад
      </button>

      {users.length === 0 ? (
        <p style={{ color: '#888' }}>Нет других пользователей</p>
      ) : (
        <div>
          {users.map(user => (
            <div
              key={user.id}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '10px 15px',
                margin: '8px 0',
                backgroundColor: 'white',
                border: '2px solid #6C5CE7',
                borderRadius: '6px',
                maxWidth: '500px',
              }}
            >
              <div>
                <strong>{user.username}</strong>
                {(user.first_name || user.last_name) && (
                  <span style={{ color: '#888', marginLeft: '10px' }}>
                    ({user.first_name} {user.last_name})
                  </span>
                )}
                <div style={{ color: '#888', fontSize: '12px', marginTop: '4px' }}>
                  {user.status === 'на сайте' ? (
                    <span style={{ color: '#00B894' }}>● на сайте</span>
                  ) : (
                    <span>{user.status}</span>
                  )}
                </div>
              </div>
              <button
                onClick={() => onSelect(user.id)}
                style={{
                  padding: '6px 12px',
                  backgroundColor: '#6C5CE7',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                }}
              >
                Пригласить
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}