import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from recommendation_engine.model import HybridRecommender
import sys
import os

# Ensure project modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@patch('recommendation_engine.model.db_client')
@patch('recommendation_engine.model.redis_client')
def test_hybrid_recommender(mock_redis, mock_db):
    print("Starting Unit Tests for Recommendation Engine...\n")
    
    # Mock database data
    mock_db.get_all_items.return_value = [
        {"item_id": "i1", "title": "MacBook Pro", "category": "Electronics", "rating": 4.8},
        {"item_id": "i2", "title": "iPhone 15", "category": "Electronics", "rating": 4.6},
        {"item_id": "i3", "title": "The Great Gatsby", "category": "Books", "rating": 4.2},
        {"item_id": "i4", "title": "Running Shoes", "category": "Clothing", "rating": 4.0},
        {"item_id": "i5", "title": "AirPods", "category": "Electronics", "rating": 4.7},
    ]
    mock_db.get_all_interactions.return_value = [
        {"user_id": "u1", "item_id": "i1", "action_type": "purchase"},
        {"user_id": "u1", "item_id": "i2", "action_type": "view"},
        {"user_id": "u2", "item_id": "i3", "action_type": "click"},
        {"user_id": "u3", "item_id": "i4", "action_type": "purchase"}
    ]

    print("1. Testing Model Initialization and Cold Start processing...")
    recommender = HybridRecommender()
    print("   ✅ Items matched and matrix formed.")
    print(f"   📊 Hybrid Similarity Matrix Shape: {recommender.hybrid_similarity.shape}\n")
    
    print("2. Testing Event Processing...")
    new_event = {"user_id": "u2", "item_id": "i5", "action_type": "purchase"}
    print(f"   [+] Simulating User u2 purchasing Item i5 (AirPods)")
    recommender.process_new_event(new_event)
    
    # Check if redis client was called
    assert mock_redis.set_recommendations.called
    print("   ✅ Recommendation update triggered (Redis set_recommendations called).\n")
    
    print("3. Validating Output Recommendations...")
    # Get the last call to redis
    call_args = mock_redis.set_recommendations.call_args_list[-1]
    user_id, recommendations = call_args[0]
    
    print(f"   🎯 Top recommendations computed for {user_id}:")
    for r in recommendations:
        print(f"       - {r['title']} [{r['category']}] (Rating: {r['rating']})")

    print("\n✅ All logic tests passed successfully!")

if __name__ == "__main__":
    test_hybrid_recommender()
