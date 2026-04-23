import React, { useState, useEffect, useMemo } from 'react';
import { useAppContext } from '../context/AppContext';
import ProductCard from '../components/ProductCard';

const Home = () => {
  const { items, currentUser, API_URL, searchQuery } = useAppContext();
  const [recs, setRecs] = useState([]);
  const [displayedItems, setDisplayedItems] = useState([]);
  const [visibleCount, setVisibleCount] = useState(12);
  const [selectedCategory, setSelectedCategory] = useState('All');
  
  // Extract unique categories from items
  const categories = useMemo(() => {
    const cats = [...new Set(items.map(i => i.category))];
    return ['All', ...cats.sort()];
  }, [items]);

  // Fetch recommendations when user changes
  useEffect(() => {
    if (!currentUser) return;
    
    const fetchRecs = async () => {
      try {
        const res = await fetch(`${API_URL}/recommendations/${currentUser.user_id}`);
        const data = await res.json();
        const recommendedItems = data.recommendations || [];
        const fullRecs = recommendedItems.map(r => {
          const localItem = items.find(i => i.item_id === r.item_id);
          return localItem || r;
        });
        setRecs(fullRecs);
      } catch (err) {
        console.error("Failed to fetch recs", err);
      }
    };
    
    fetchRecs();
    const interval = setInterval(fetchRecs, 5000);
    return () => clearInterval(interval);
  }, [currentUser, items, API_URL]);

  // Filter items based on search query and category
  useEffect(() => {
    if (items.length > 0) {
      let filtered = [...items];
      
      // Apply category filter
      if (selectedCategory !== 'All') {
        filtered = filtered.filter(item => item.category === selectedCategory);
      }
      
      // Apply search filter
      if (searchQuery.trim() !== '') {
        const query = searchQuery.toLowerCase();
        filtered = filtered.filter(item => 
          item.title?.toLowerCase().includes(query) || 
          item.category?.toLowerCase().includes(query) ||
          item.description?.toLowerCase().includes(query)
        );
      } else if (selectedCategory === 'All') {
        // Only shuffle when no search and no category filter
        filtered = filtered.sort(() => 0.5 - Math.random());
      }
      
      setDisplayedItems(filtered);
      setVisibleCount(12); // Reset pagination on filter change
    }
  }, [items, searchQuery, selectedCategory]);

  const handleLoadMore = () => {
    setVisibleCount(prev => prev + 12);
  };

  const isSearching = searchQuery.trim() !== '';
  const isFiltering = selectedCategory !== 'All';

  return (
    <div className="page-home">
      {/* Only show hero when not searching */}
      {!isSearching && (
        <div className="hero">
          <div className="hero-content">
            <h1>Discover Premium Excellence</h1>
            <p>Curated products tailored just for you by our AI engine.</p>
          </div>
        </div>
      )}
      
      {/* RECOMMENDED FOR YOU ROW — hidden during search or category filter */}
      {recs.length > 0 && !isSearching && !isFiltering && (
        <section className="section">
          <div className="sec-header">
            <h2 className="sec-title">Recommended For You</h2>
            <p className="sec-subtitle">Based on your recent activity</p>
          </div>
          <div className="product-scroll">
            {recs.slice(0, 10).map(item => (
              <ProductCard key={`rec-${item.item_id}`} product={item} />
            ))}
          </div>
        </section>
      )}

      {/* CATEGORY FILTER BAR */}
      <section className="section">
        <div className="sec-header">
          <h2 className="sec-title">
            {isSearching 
              ? `Search Results for "${searchQuery}"` 
              : isFiltering 
                ? selectedCategory 
                : "Explore Products"}
          </h2>
          <p className="sec-subtitle">
            {isSearching 
              ? `Found ${displayedItems.length} items` 
              : isFiltering 
                ? `${displayedItems.length} products in this category`
                : "Handpicked selection just for you"}
          </p>
        </div>
        
        {/* Category chips */}
        {!isSearching && (
          <div className="category-bar">
            {categories.map(cat => (
              <button
                key={cat}
                className={`category-chip ${selectedCategory === cat ? 'active' : ''}`}
                onClick={() => setSelectedCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
        )}
        
        {displayedItems.length === 0 ? (
          <div className="empty-state" style={{ padding: '2rem' }}>
            <h2>No items found.</h2>
            <p>Try a different search query or category.</p>
          </div>
        ) : (
          <div className="product-grid">
            {displayedItems.slice(0, visibleCount).map(item => (
              <ProductCard key={`rand-${item.item_id}`} product={item} />
            ))}
          </div>
        )}

        {visibleCount < displayedItems.length && (
          <div style={{ textAlign: 'center', marginTop: '3rem' }}>
            <button className="btn-secondary btn-lg" onClick={handleLoadMore}>
              Load More Items
            </button>
          </div>
        )}
      </section>
    </div>
  );
};

export default Home;
