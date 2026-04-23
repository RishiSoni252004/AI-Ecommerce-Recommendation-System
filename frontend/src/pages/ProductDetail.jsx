import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Check, ShoppingCart, Heart, Share2 } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import ProductCard from '../components/ProductCard';

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { items, fireEvent, addToCart } = useAppContext();
  
  const product = items.find(i => i.item_id === id);
  
  // Basic calculations
  const price = product?.price || 0;
  const mrp = Math.floor(price * 1.35);
  const discount = Math.floor((1 - price / mrp) * 100);
  const rating = parseFloat(product?.rating || 0).toFixed(1);
  const fullStars = Math.floor(rating);
  const stars = "★".repeat(fullStars) + "☆".repeat(5 - fullStars);

  if (!product) {
    return (
      <div className="loader-container">
        <h2>Product not found</h2>
        <button className="btn-primary" onClick={() => navigate('/')}>Back Home</button>
      </div>
    );
  }

  // Similar products logic
  const sameCat = items.filter(i => i.category === product.category && i.item_id !== product.item_id);
  const similarSort = sameCat.sort((a,b) => b.rating - a.rating).slice(0, 4);

  return (
    <div className="page-product">
      <Link to="/" className="back-link">
        <ArrowLeft size={16} /> Back to Catalog
      </Link>
      
      <div className="detail-view">
        <div className="detail-img-box">
          {product.image && (product.image.startsWith('http') || product.image.startsWith('/')) ? (
            <img src={product.image} alt={product.title} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: 'var(--radius-xl)' }} onError={(e) => { e.target.onerror = null; e.target.src = 'https://placehold.co/400x400/f3f4f6/a1a1aa?text=Image'; }} />
          ) : (
            product.image || '📦'
          )}
        </div>
        
        <div className="detail-info">
          <span className="detail-cat">{product.category}</span>
          <h1 className="detail-title">{product.title}</h1>
          <div className="detail-stars">
            {stars} <span>{rating}/5.0 · Community Favorite</span>
          </div>
          
          <div className="detail-price-box">
            <div className="detail-price">
              ₹{price.toLocaleString()} <small>₹{mrp.toLocaleString()}</small>
            </div>
            <div className="detail-offer">🎉 Save ₹{(mrp - price).toLocaleString()} ({discount}% off)</div>
          </div>
          
          <p className="detail-desc">{product.description}</p>
          
          <ul className="detail-features">
            <li><Check size={16} /> Free Delivery by Tomorrow</li>
            <li><Check size={16} /> 7-Day Easy Returns</li>
            <li><Check size={16} /> Top Rated by Community</li>
            <li><Check size={16} /> Secure Payment Options</li>
          </ul>
          
          <div className="detail-actions">
            <button 
              className="btn-primary btn-lg" 
              style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px'}}
              onClick={() => addToCart(product)}
            >
              <ShoppingCart size={20} /> Add to Cart
            </button>
            <button 
              className="btn-secondary btn-lg"
              title="Add to Wishlist"
              onClick={() => fireEvent(product.item_id, 'click')}
            >
              <Heart size={20} />
            </button>
            <button 
              className="btn-secondary btn-lg"
              title="Share"
              onClick={() => fireEvent(product.item_id, 'view')}
            >
              <Share2 size={20} />
            </button>
          </div>
        </div>
      </div>
      
      {similarSort.length > 0 && (
        <section className="section">
          <div className="sec-header">
            <div className="sec-icon">🔄</div>
            <div>
              <h2 className="sec-title">Customers Also Viewed</h2>
              <p className="sec-subtitle">Similar products you might like</p>
            </div>
          </div>
          <div className="product-grid">
            {similarSort.map(item => (
              <ProductCard key={`sim-${item.item_id}`} product={item} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default ProductDetail;
