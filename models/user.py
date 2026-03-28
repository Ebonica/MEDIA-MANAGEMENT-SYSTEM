from datetime import datetime
from config.database import db
from bson import ObjectId

class UserModel:
    def __init__(self):
        self.collection = db.get_db().users
    
    def get_by_id(self, user_id: str):
        """Get user by ID"""
        try:
            return self.collection.find_one({"_id": ObjectId(user_id)})
        except:
            return None
    
    def get_by_username(self, username: str):
        """Get user by username"""
        return self.collection.find_one({"username": username})
    
    def get_all_users(self, role=None):
        """Get all users, optionally filtered by role"""
        query = {"role": role} if role else {}
        return list(self.collection.find(query))
    
    def update_profile(self, user_id: str, data: dict):
        """Update user profile"""
        try:
            return self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": data}
            )
        except:
            return None
    
    def delete_user(self, user_id: str):
        """Delete user"""
        try:
            return self.collection.delete_one({"_id": ObjectId(user_id)})
        except:
            return None
    
    def get_user_stats(self, user_id: str):
        """Get user statistics"""
        try:
            user_obj_id = ObjectId(user_id)
            database = db.get_db()
            
            channels = database.channels.count_documents({"creator_id": user_id})
            videos = database.videos.count_documents({"creator_id": user_id})
            playlists = database.playlists.count_documents({"creator_id": user_id})
            comments = database.comments.count_documents({"user_id": user_id})
            
            # Get total views across all videos
            pipeline = [
                {"$match": {"creator_id": user_id}},
                {"$group": {"_id": None, "total_views": {"$sum": "$views"}}}
            ]
            views_result = list(database.videos.aggregate(pipeline))
            total_views = views_result[0]['total_views'] if views_result else 0
            
            return {
                "channels": channels,
                "videos": videos,
                "playlists": playlists,
                "comments": comments,
                "total_views": total_views
            }
        except:
            return {
                "channels": 0,
                "videos": 0,
                "playlists": 0,
                "comments": 0,
                "total_views": 0
            }