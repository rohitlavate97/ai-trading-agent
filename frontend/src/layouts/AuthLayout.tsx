import React from 'react';
import { Outlet } from 'react-router-dom';
import './AuthLayout.css';

const AuthLayout: React.FC = () => {
  return (
    <div className="auth-layout animate-fade-in">
      <div className="auth-background-decoration"></div>
      <div className="auth-container glass-panel">
        <div className="auth-logo">
          <h2>AI Trading Assistant</h2>
          <p>Your intelligent market companion</p>
        </div>
        <Outlet />
      </div>
    </div>
  );
};

export default AuthLayout;
