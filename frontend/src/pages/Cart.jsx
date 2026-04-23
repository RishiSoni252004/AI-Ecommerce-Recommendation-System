import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ShoppingCart, Trash2, ArrowRight } from 'lucide-react';
import { useAppContext } from '../context/AppContext';

const Cart = () => {
  const { cart, removeFromCart, updateCartQty, checkout } = useAppContext();
  const navigate = useNavigate();

  const total = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);

  const handleCheckout = async () => {
    const success = await checkout();
    if (success) {
      navigate('/orders');
    }
  };

  if (cart.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">🛒</div>
        <h2>Your cart is empty</h2>
        <p>Looks like you haven't added anything to your cart yet.</p>
        <Link to="/" className="btn-primary" style={{ display: 'inline-block', marginTop: '1rem' }}>
          Start Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="page-cart">
      <h1 className="page-title">Shopping Cart</h1>
      
      <div className="cart-layout">
        <div className="cart-items">
          {cart.map(item => (
            <div key={item.item_id} className="cart-item">
              <div className="c-item-img">
                {item.image && (item.image.startsWith('http') || item.image.startsWith('/')) ? (
                  <img src={item.image} alt={item.title} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px' }} onError={(e) => { e.target.onerror = null; e.target.src = 'https://placehold.co/120x120/f3f4f6/a1a1aa?text=Image'; }} />
                ) : (
                  item.image || '📦'
                )}
              </div>
              <div className="c-item-info">
                <h3>{item.title}</h3>
                <p className="c-item-cat">{item.category}</p>
                <div className="c-item-qty">
                  <button onClick={() => updateCartQty(item.item_id, item.qty - 1)}>-</button>
                  <span>{item.qty}</span>
                  <button onClick={() => updateCartQty(item.item_id, item.qty + 1)}>+</button>
                </div>
              </div>
              <div className="c-item-price-col">
                <div className="c-item-price">₹{(item.price * item.qty).toLocaleString()}</div>
                <button className="c-item-remove" onClick={() => removeFromCart(item.item_id)}>
                  <Trash2 size={18} />
                </button>
              </div>
            </div>
          ))}
        </div>
        
        <div className="cart-summary">
          <h2>Order Summary</h2>
          <div className="summary-row">
            <span>Subtotal</span>
            <span>₹{total.toLocaleString()}</span>
          </div>
          <div className="summary-row">
            <span>Shipping</span>
            <span>Free</span>
          </div>
          <div className="summary-row total">
            <span>Total</span>
            <span>₹{total.toLocaleString()}</span>
          </div>
          
          <button className="btn-primary w-100 btn-lg" onClick={handleCheckout}>
            Proceed to Checkout <ArrowRight size={18} style={{marginLeft: 8}} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Cart;
