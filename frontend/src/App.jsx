import { BrowserRouter, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import { ShoppingBag, User as UserIcon, LogOut, Package, Search } from 'lucide-react';
import { AppProvider, useAppContext } from './context/AppContext';
import Home from './pages/Home';
import ProductDetail from './pages/ProductDetail';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Cart from './pages/Cart';
import OrderHistory from './pages/OrderHistory';

// Protected Route Wrapper
const ProtectedRoute = ({ children }) => {
  const { currentUser, loading } = useAppContext();
  if (loading) return null;
  if (!currentUser) return <Navigate to="/login" />;
  return children;
};

const Navbar = () => {
  const { currentUser, cart, logout, searchQuery, setSearchQuery } = useAppContext();
  const navigate = useNavigate();
  
  const cartItemCount = cart.reduce((sum, item) => sum + item.qty, 0);
  
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-brand">
          <span className="brand-logo">S</span>
          ShopSmart
        </Link>
        
        <div className="nav-search-bar" style={{ flex: 1, maxWidth: '400px', margin: '0 2rem', display: 'flex', alignItems: 'center', background: 'var(--bg-main)', padding: '8px 16px', borderRadius: '100px', border: '1px solid var(--border)' }}>
          <Search size={18} color="var(--text-muted)" style={{ marginRight: '8px' }} />
          <input 
            type="text" 
            placeholder="Search for items..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ border: 'none', background: 'transparent', outline: 'none', width: '100%', fontSize: '0.95rem' }}
          />
        </div>

        <div className="nav-right">
          {currentUser ? (
            <>
              <Link to="/orders" className="nav-icon-link" title="Orders">
                <Package size={22} />
              </Link>
              <Link to="/cart" className="nav-icon-link cart-link" title="Cart">
                <ShoppingBag size={22} />
                {cartItemCount > 0 && <span className="cart-badge">{cartItemCount}</span>}
              </Link>
              
              <div className="user-menu">
                <div className="user-menu-btn">
                  <UserIcon size={20} />
                  <span>{currentUser.name?.split(' ')[0]}</span>
                </div>
                <div className="user-dropdown">
                  <button onClick={() => { logout(); navigate('/login'); }}>
                    <LogOut size={16} /> Logout
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="auth-links">
              <Link to="/login" className="nav-link">Log In</Link>
              <Link to="/signup" className="btn-primary btn-small">Sign Up</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

const Footer = () => (
  <footer className="site-footer">
    <div className="footer-content">
      <div className="footer-brand">ShopSmart.</div>
      <p className="footer-text">Premium Real-Time AI Commerce</p>
      <div className="tech-badges">
        <span className="tech-badge">React</span>
        <span className="tech-badge">FastAPI</span>
        <span className="tech-badge">Kafka</span>
      </div>
    </div>
  </footer>
);

const ToastContainer = () => {
  const { toasts } = useAppContext();
  return (
    <div className="toast-container">
      {toasts.map(t => (
        <div key={t.id} className={`toast ${t.type}`}>
          <span>{t.msg}</span>
        </div>
      ))}
    </div>
  );
};

function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <div className="app-container">
          <Navbar />
          <main className="main-content">
            <AppContent />
          </main>
          <Footer />
          <ToastContainer />
        </div>
      </BrowserRouter>
    </AppProvider>
  );
}

const AppContent = () => {
  const { loading } = useAppContext();
  
  if (loading) {
    return (
      <div className="loader-container">
        <div className="loader"></div>
      </div>
    );
  }
  
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
      <Route path="/product/:id" element={<ProtectedRoute><ProductDetail /></ProtectedRoute>} />
      <Route path="/cart" element={<ProtectedRoute><Cart /></ProtectedRoute>} />
      <Route path="/orders" element={<ProtectedRoute><OrderHistory /></ProtectedRoute>} />
    </Routes>
  );
};

export default App;
