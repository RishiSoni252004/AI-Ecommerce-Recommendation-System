import React, { createContext, useContext, useState, useEffect } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const AppContext = createContext();

export const useAppContext = () => useContext(AppContext);

export const AppProvider = ({ children }) => {
  const [items, setItems] = useState([]);
  
  // Try to load user from localStorage
  const loadUser = () => {
    const saved = localStorage.getItem('currentUser');
    return saved ? JSON.parse(saved) : null;
  };
  
  // Try to load cart from localStorage
  const loadCart = () => {
    const saved = localStorage.getItem('cart');
    return saved ? JSON.parse(saved) : [];
  };

  const [currentUser, setCurrentUser] = useState(loadUser());
  const [cart, setCart] = useState(loadCart());
  const [loading, setLoading] = useState(true);
  const [toasts, setToasts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  
  useEffect(() => {
    const initData = async () => {
      try {
        const itemsRes = await fetch(`${API_URL}/items`);
        const itemsData = await itemsRes.json();
        setItems(itemsData.items || []);
      } catch (err) {
        console.error("Failed to load initial data", err);
      } finally {
        setLoading(false);
      }
    };
    initData();
  }, []);

  // Update localStorage when currentUser or cart changes
  useEffect(() => {
    if (currentUser) {
      localStorage.setItem('currentUser', JSON.stringify(currentUser));
    } else {
      localStorage.removeItem('currentUser');
    }
  }, [currentUser]);

  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  const showToast = (msg, type = 'info') => {
    const id = Date.now();
    setToasts(prev => [...prev, { id, msg, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3000);
  };

  const login = async (email, password) => {
    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || 'Login failed');
      }
      const userData = await res.json();
      setCurrentUser(userData);
      showToast('Welcome back, ' + userData.name.split(' ')[0] + '!', 'success');
      return true;
    } catch (err) {
      showToast(err.message, 'error');
      return false;
    }
  };

  const signup = async (name, email, password) => {
    try {
      const res = await fetch(`${API_URL}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
      });
      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || 'Registration failed');
      }
      const userData = await res.json();
      setCurrentUser(userData);
      showToast('Account created successfully!', 'success');
      return true;
    } catch (err) {
      showToast(err.message, 'error');
      return false;
    }
  };

  const logout = () => {
    setCurrentUser(null);
    setCart([]);
    showToast('Logged out successfully', 'info');
  };

  const fireEvent = async (itemId, actionType) => {
    if (!currentUser) return;
    try {
      await fetch(`${API_URL}/event`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: currentUser.user_id,
          item_id: itemId,
          action_type: actionType
        })
      });
      
      // If only buying/adding, we don't spam toasts for view/click here unless wanted.
      // E-commerce usually doesn't notify on view.
    } catch (err) {
      console.error("Failed to fire event", err);
    }
  };

  const addToCart = (item) => {
    setCart(prev => {
      const existing = prev.find(i => i.item_id === item.item_id);
      if (existing) {
        return prev.map(i => i.item_id === item.item_id ? { ...i, qty: i.qty + 1 } : i);
      }
      return [...prev, { ...item, qty: 1 }];
    });
    fireEvent(item.item_id, 'click'); // Treat adding to cart as a strong click signal
    showToast('Added to cart', 'success');
  };

  const removeFromCart = (itemId) => {
    setCart(prev => prev.filter(i => i.item_id !== itemId));
  };
  
  const updateCartQty = (itemId, qty) => {
    if (qty <= 0) {
      removeFromCart(itemId);
      return;
    }
    setCart(prev => prev.map(i => i.item_id === itemId ? { ...i, qty } : i));
  };

  const checkout = async () => {
    if (cart.length === 0) return false;
    // Fire purchase event for each item
    for (const item of cart) {
      await fireEvent(item.item_id, 'purchase');
    }
    setCart([]);
    showToast('Order placed successfully! Thank you for shopping with us.', 'success');
    return true;
  };

  return (
    <AppContext.Provider value={{ 
      items, 
      currentUser, login, signup, logout,
      cart, addToCart, removeFromCart, updateCartQty, checkout,
      searchQuery, setSearchQuery,
      loading, fireEvent, API_URL, toasts 
    }}>
      {children}
    </AppContext.Provider>
  );
};
