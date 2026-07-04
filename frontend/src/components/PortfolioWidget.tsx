import React, { useState, useEffect } from 'react';
import { ApiClient } from '../api/client';

interface Position {
  symbol: string;
  quantity: number;
  average_price: number;
}

interface Portfolio {
  cash_balance: number;
  positions: Position[];
}

const PortfolioWidget: React.FC = () => {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchPortfolio = async () => {
    try {
      const data = await ApiClient.get('/portfolio');
      setPortfolio(data);
    } catch (err) {
      console.error('Failed to load portfolio', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPortfolio();
  }, []);

  if (loading) return <div className="glass-panel widget">Loading portfolio...</div>;
  if (!portfolio) return <div className="glass-panel widget">Failed to load portfolio</div>;

  return (
    <div className="glass-panel widget">
      <div className="widget-header">
        <h3>Portfolio Overview</h3>
        <button className="icon-btn" onClick={fetchPortfolio} title="Refresh">&#x21bb;</button>
      </div>
      
      <div className="portfolio-summary">
        <div className="metric-card">
          <span className="metric-label">Cash Balance</span>
          <span className="metric-value">${portfolio.cash_balance.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</span>
        </div>
      </div>

      <h4 className="section-title">Open Positions</h4>
      {portfolio.positions.length === 0 ? (
        <p className="empty-state">No open positions.</p>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th className="text-right">Shares</th>
                <th className="text-right">Avg Price</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.positions.map((pos) => (
                <tr key={pos.symbol}>
                  <td className="font-bold">{pos.symbol}</td>
                  <td className="text-right">{pos.quantity}</td>
                  <td className="text-right">${pos.average_price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default PortfolioWidget;
