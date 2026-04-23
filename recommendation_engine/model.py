import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from database.mongo_client import db_client
from database.redis_client import redis_client

class HybridRecommender:
    def __init__(self):
        self.items_df = pd.DataFrame()
        self.interactions_df = pd.DataFrame()
        self.user_item_matrix = pd.DataFrame()
        self.item_similarity_cf = np.array([])
        self.item_similarity_cb = np.array([])
        self.hybrid_similarity = np.array([])
        self.refresh_model()

    def refresh_model(self):
        print("Fetching data from MongoDB for model refresh...")
        items = db_client.get_all_items()
        interactions = db_client.get_all_interactions()
        
        if not items:
            print("No items found. Skipping model refresh.")
            return
            
        self.items_df = pd.DataFrame(items).set_index("item_id")
        
        # 1. Content-Based Filtering (Item Category/Title)
        # Create text feature by combining title and category
        self.items_df["content_features"] = self.items_df["title"] + " " + self.items_df["category"]
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.items_df["content_features"])
        self.item_similarity_cb = cosine_similarity(tfidf_matrix, tfidf_matrix)

        if interactions:
            self.interactions_df = pd.DataFrame(interactions)
            
            # Map actions to weights
            action_weights = {"view": 1, "click": 2, "purchase": 5}
            self.interactions_df["weight"] = self.interactions_df["action_type"].map(action_weights)
            
            # 2. Collaborative Filtering (User-Item Matrix)
            self.user_item_matrix = self.interactions_df.pivot_table(
                index="user_id", columns="item_id", values="weight", aggfunc="sum"
            ).fillna(0)
            
            # Ensure all items match the item_df columns
            missing_cols = set(self.items_df.index) - set(self.user_item_matrix.columns)
            for c in missing_cols:
                self.user_item_matrix[c] = 0
                
            self.user_item_matrix = self.user_item_matrix[self.items_df.index]
            
            # Item-Item CF similarity
            self.item_similarity_cf = cosine_similarity(self.user_item_matrix.T)
        else:
            self.item_similarity_cf = np.zeros_like(self.item_similarity_cb)
            
        # 3. Hybrid Similarity
        # Combine CB and CF similarities (e.g., 50/50 blend)
        self.hybrid_similarity = 0.5 * self.item_similarity_cb + 0.5 * self.item_similarity_cf
        
        # 4. Global Popularity Fallback (for Cold Start)
        popular_items = db_client.get_popular_items(limit=10)
        if popular_items:
            redis_client.set_recommendations("global_trending", popular_items)
            print("Successfully cached global_trending fallback.")
        
        # Pre-compute and save for all active users
        if interactions:
            unique_users = self.interactions_df["user_id"].unique()
            for u in unique_users:
                self.update_user_recommendations(u)

    def process_new_event(self, event):
        # Optimistic fast update: just append to df and re-calc for that user
        # In a real heavy system we'd use incremental SVD, but for our scale pandas is fine
        event_df = pd.DataFrame([event])
        action_weights = {"view": 1, "click": 2, "purchase": 5}
        event_df["weight"] = event_df["action_type"].map(action_weights)
        
        self.interactions_df = pd.concat([self.interactions_df, event_df], ignore_index=True)
        
        # Update user-item matrix just for this user
        u_id = event["user_id"]
        i_id = event["item_id"]
        w = action_weights.get(event["action_type"], 1)
        
        if u_id not in self.user_item_matrix.index:
            new_row = pd.Series(0, index=self.user_item_matrix.columns, name=u_id)
            self.user_item_matrix = pd.concat([self.user_item_matrix, new_row.to_frame().T])
            
        if i_id in self.user_item_matrix.columns:
            self.user_item_matrix.at[u_id, i_id] += w
            
        self.update_user_recommendations(u_id)

    def update_user_recommendations(self, user_id):
        if user_id not in self.user_item_matrix.index or self.items_df.empty:
            return
            
        # User's items profile
        user_profile = self.user_item_matrix.loc[user_id].values
        
        # Multiply user profile by item similarity matrix to get scores
        scores = user_profile.dot(self.hybrid_similarity)
        
        # Normalize and exclude already interacted items if we wanted to
        # but let's just sort and take top 5
        item_indices = np.argsort(scores)[::-1]
        
        top_items = []
        count = 0
        for idx in item_indices:
            if count >= 5:
                break
            item_id = self.items_df.index[idx]
            
            # Optional: do not recommend already purchased items. For now we just recommend top 5 blindly
            item_data = self.items_df.iloc[idx].to_dict()
            item_data["item_id"] = item_id
            top_items.append(item_data)
            count += 1
            
        # Store in Redis
        redis_client.set_recommendations(user_id, top_items)
        print(f"Updated recommendations for {user_id}")
