import React from 'react';
import { Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './DashboardLayout.css';

const DashboardLayout: React.FC = () => {
  const { logout } = useAuth();

  return (
    <div className="dashboard-layout animate-fade-in">
      <aside className="dashboard-sidebar glass-panel">
        <div className="sidebar-brand">
          <h3>AI Trader</h3>
        </div>
        <nav className="sidebar-nav">
          <button className="nav-item active">Dashboard</button>
          <button className="nav-item">Portfolio</button>
          <button className="nav-item">Settings</button>
          <div className="nav-spacer"></div>
          <button className="nav-item logout" onClick={logout}>Logout</button>
        </nav>
      </aside>
      <main className="dashboard-main">
        <Outlet />
      </main>
    </div>
  );
};

export default DashboardLayout;
