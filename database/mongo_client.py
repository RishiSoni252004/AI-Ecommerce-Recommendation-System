import os
from pymongo import MongoClient

class MongoDBClient:
    def __init__(self):
        # Fallback to localhost if not in docker
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client["recsys_db"]
        self.users_collection = self.db["users"]
        self.items_collection = self.db["items"]
        self.interactions_collection = self.db["interactions"]

    def insert_users(self, users):
        if users:
            self.users_collection.insert_many(users)

    def insert_items(self, items):
        if items:
            self.items_collection.insert_many(items)

    def insert_interactions(self, interactions):
        if interactions:
            self.interactions_collection.insert_many(interactions)

    def get_user(self, user_id):
        return self.users_collection.find_one({"user_id": user_id})

    def get_user_by_email(self, email):
        return self.users_collection.find_one({"email": email}, {"_id": 0})

    def create_user(self, user_data: dict):
        self.users_collection.insert_one(user_data)

    def update_user_recommendations(self, user_id: str, recommendations: list):
        self.users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"recommendations": recommendations}}
        )

    def get_all_users(self):
        return list(self.users_collection.find({}, {"_id": 0}))

    def get_item(self, item_id):
        return self.items_collection.find_one({"item_id": item_id})

    def get_all_items(self):
        return list(self.items_collection.find({}, {"_id": 0}))

    def get_all_interactions(self):
        return list(self.interactions_collection.find({}, {"_id": 0}))

    def get_popular_items(self, limit=10):
        """
        Calculates the most popular items based on interaction counts (views, clicks, purchases).
        Returns a list of item details.
        """
        pipeline = [
            {"$group": {"_id": "$item_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        popular_ids = [res["_id"] for res in self.interactions_collection.aggregate(pipeline)]
        
        # Fetch full details for these items
        if not popular_ids:
            return []
            
        items = list(self.items_collection.find({"item_id": {"$in": popular_ids}}, {"_id": 0}))
        # Sort items in the same order as popular_ids
        items_map = {item["item_id"]: item for item in items}
        return [items_map[iid] for iid in popular_ids if iid in items_map]

    def clear_db(self):
        self.users_collection.delete_many({})
        self.items_collection.delete_many({})
        self.interactions_collection.delete_many({})

db_client = MongoDBClient()
