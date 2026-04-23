import React, { useEffect, useState } from 'react';
import { Package } from 'lucide-react';
import { useAppContext } from '../context/AppContext';

const OrderHistory = () => {
  const { currentUser, API_URL, items } = useAppContext();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!currentUser) return;
    const fetchHistory = async () => {
      try {
        const res = await fetch(`${API_URL}/users/${currentUser.user_id}/history`);
        const data = await res.json();
        
        // Filter only 'purchase' events
        const purchases = (data.history || []).filter(h => h.action_type === 'purchase');
        
        // Enrich with item details
        const enriched = purchases.map(p => {
          const item = items.find(i => i.item_id === p.item_id) || { title: 'Unknown Item', price: 0, image: '📦' };
          return { ...p, ...item };
        });
        
        setOrders(enriched);
      } catch (err) {
        console.error("Failed to fetch order history", err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [currentUser, API_URL, items]);

  if (loading) return <div className="loader-container"><div className="loader"></div></div>;

  return (
    <div className="page-orders">
      <h1 className="page-title">Order History</h1>
      
      {orders.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📦</div>
          <h2>No orders yet</h2>
          <p>When you purchase items, they will appear here.</p>
        </div>
      ) : (
        <div className="orders-list">
          {orders.map((order, i) => (
            <div key={`${order.item_id}-${order.timestamp}-${i}`} className="order-card">
              <div className="order-header">
                <div>
                  <span className="order-status">Confirmed</span>
                  <span className="order-date">
                    {new Date(order.timestamp * 1000).toLocaleDateString()}
                  </span>
                </div>
                <div className="order-total">
                  ₹{order.price.toLocaleString()}
                </div>
              </div>
              <div className="order-body">
                <div className="o-img">
                  {order.image && (order.image.startsWith('http') || order.image.startsWith('/')) ? (
                    <img src={order.image} alt={order.title} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px' }} onError={(e) => { e.target.onerror = null; e.target.src = 'https://placehold.co/120x120/f3f4f6/a1a1aa?text=Image'; }} />
                  ) : (
                    order.image || '📦'
                  )}
                </div>
                <div className="o-info">
                  <h3>{order.title}</h3>
                  <p>{order.category}</p>
                </div>
                <div className="o-actions">
                  <button className="btn-secondary">View Item</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default OrderHistory;
