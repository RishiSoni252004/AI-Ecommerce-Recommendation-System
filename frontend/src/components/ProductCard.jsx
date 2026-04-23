import React from 'react';
import { Link } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';

const ProductCard = ({ product }) => {
  const { fireEvent, addToCart } = useAppContext();
  
  const price = product.price || 0;
  const mrp = Math.floor(price * (1.15 + Math.random() * 0.3));
  const discount = Math.floor((1 - price / mrp) * 100);
  const rating = parseFloat(product.rating || 0).toFixed(1);
  const fullStars = Math.floor(rating);
  const stars = "★".repeat(fullStars) + "☆".repeat(5 - fullStars);

  const isUrl = product.image && (product.image.startsWith('http') || product.image.startsWith('/'));

  return (
    <div className="p-card">
      <div className="p-card-img-wrap">
        <span className="p-card-badge">{discount}% OFF</span>
        {isUrl ? (
          <img 
            src={product.image} 
            alt={product.title} 
            className="p-card-img"
            loading="lazy"
            onError={(e) => { e.target.onerror = null; e.target.src = 'https://placehold.co/400x400/f3f4f6/a1a1aa?text=Image'; }}
          />
        ) : (
          <div className="p-card-img-emoji">{product.image || '📦'}</div>
        )}
      </div>
      
      <div className="p-card-body">
        <p className="p-card-cat">{product.category}</p>
        <p className="p-card-name">{product.title}</p>
        <p className="p-card-stars">
          <span style={{color: 'var(--gold)'}}>{stars}</span> 
          <span style={{color: 'var(--text-muted)', fontSize: '0.75rem', marginLeft: '6px'}}>{rating}</span>
        </p>
        
        <div className="p-card-price-row">
          <p className="p-card-price">₹{price.toLocaleString()}</p>
          <p className="p-card-mrp">₹{mrp.toLocaleString()}</p>
        </div>
        
        <div className="p-card-actions">
          <Link 
            to={`/product/${product.item_id}`} 
            className="btn-primary"
            onClick={() => fireEvent(product.item_id, 'view')}
          >
            View Details
          </Link>
          <button 
            className="btn-secondary"
            onClick={() => addToCart(product)}
            title="Add to Cart"
          >
            🛒
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
