import React, { useState, useEffect } from 'react';
import { ApiClient } from '../api/client';

interface Order {
  id: number;
  symbol: string;
  side: string;
  quantity: number;
  price: number;
  status: string;
  created_at: string;
}

const OrderHistoryWidget: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = async () => {
    try {
      const data = await ApiClient.get('/orders');
      setOrders(data);
    } catch (err) {
      console.error('Failed to load orders', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  if (loading) return <div className="glass-panel widget">Loading orders...</div>;

  return (
    <div className="glass-panel widget">
      <div className="widget-header">
        <h3>Order History</h3>
        <button className="icon-btn" onClick={fetchOrders} title="Refresh">&#x21bb;</button>
      </div>
      
      {orders.length === 0 ? (
        <p className="empty-state">No past orders found.</p>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Side</th>
                <th className="text-right">Qty</th>
                <th className="text-right">Price</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td className="font-bold">{order.symbol}</td>
                  <td className={order.side === 'BUY' ? 'text-success' : 'text-danger'}>
                    {order.side}
                  </td>
                  <td className="text-right">{order.quantity}</td>
                  <td className="text-right">${order.price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                  <td><span className={`status-badge status-${order.status.toLowerCase()}`}>{order.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default OrderHistoryWidget;
