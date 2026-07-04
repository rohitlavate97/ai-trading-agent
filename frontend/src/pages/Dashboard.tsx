import React from 'react';
import ChatWidget from '../components/ChatWidget';
import PortfolioWidget from '../components/PortfolioWidget';
import OrderHistoryWidget from '../components/OrderHistoryWidget';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard-grid">
      <div className="dashboard-left-col">
        <PortfolioWidget />
        <OrderHistoryWidget />
      </div>
      <div className="dashboard-right-col">
        <ChatWidget />
      </div>
    </div>
  );
};

export default Dashboard;
