import React from 'react';
import ChatWidget from '../components/ChatWidget';

const Dashboard: React.FC = () => {
  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h2>Welcome to your Dashboard</h2>
        <p>Market is currently open. Your AI assistant is ready to help.</p>
      </div>
      <div style={{ flex: 1, minHeight: 0 }}>
        <ChatWidget />
      </div>
    </div>
  );
};

export default Dashboard;
