from datetime import datetime
from config.database import db
from bson import ObjectId

class VideoModel:
    def __init__(self):
        self.collection = db.get_db().videos
    
    def create(self, video_data: dict):
        """Create a new video"""
        video_data['created_at'] = datetime.now()
        video_data['views'] = 0
        video_data['likes'] = 0
        video_data['dislikes'] = 0
        video_data['liked_by'] = []  # Track users who liked
        video_data['disliked_by'] = []  # Track users who disliked
        result = self.collection.insert_one(video_data)
        return str(result.inserted_id)
    
    def get_by_id(self, video_id: str):
        """Get video by ID"""
        try:
            return self.collection.find_one({"_id": ObjectId(video_id)})
        except:
            return None
    
    def get_by_channel(self, channel_id: str):
        """Get all videos by channel"""
        return list(self.collection.find({"channel_id": channel_id}).sort("created_at", -1))
    
    def get_by_creator(self, creator_id: str):
        """Get all videos by creator"""
        return list(self.collection.find({"creator_id": creator_id}).sort("created_at", -1))
    
    def get_all(self, limit=None):
        """Get all videos"""
        query = self.collection.find().sort("created_at", -1)
        if limit:
            query = query.limit(limit)
        return list(query)
    
    def update(self, video_id: str, data: dict):
        """Update video"""
        try:
            return self.collection.update_one(
                {"_id": ObjectId(video_id)},
                {"$set": data}
            )
        except:
            return None
    
    def delete(self, video_id: str):
        """Delete video"""
        try:
            return self.collection.delete_one({"_id": ObjectId(video_id)})
        except:
            return None
    
    def increment_views(self, video_id: str):
        """Increment view count"""
        try:
            return self.collection.update_one(
                {"_id": ObjectId(video_id)},
                {"$inc": {"views": 1}}
            )
        except:
            return None
    
    def like(self, video_id: str, user_id: str):
        """Toggle like for a video"""
        try:
            video = self.collection.find_one({"_id": ObjectId(video_id)})
            if not video:
                return None
            
            liked_by = video.get('liked_by', [])
            disliked_by = video.get('disliked_by', [])
            
            # If user already liked, unlike it
            if user_id in liked_by:
                self.collection.update_one(
                    {"_id": ObjectId(video_id)},
                    {
                        "$pull": {"liked_by": user_id},
                        "$inc": {"likes": -1}
                    }
                )
                return "unliked"
            else:
                # Remove from dislike if present
                if user_id in disliked_by:
                    self.collection.update_one(
                        {"_id": ObjectId(video_id)},
                        {
                            "$pull": {"disliked_by": user_id},
                            "$inc": {"dislikes": -1}
                        }
                    )
                
                # Add to likes
                self.collection.update_one(
                    {"_id": ObjectId(video_id)},
                    {
                        "$addToSet": {"liked_by": user_id},
                        "$inc": {"likes": 1}
                    }
                )
                return "liked"
        except Exception as e:
            print(f"Error in like: {e}")
            return None
    
    def dislike(self, video_id: str, user_id: str):
        """Toggle dislike for a video"""
        try:
            video = self.collection.find_one({"_id": ObjectId(video_id)})
            if not video:
                return None
            
            liked_by = video.get('liked_by', [])
            disliked_by = video.get('disliked_by', [])
            
            # If user already disliked, remove dislike
            if user_id in disliked_by:
                self.collection.update_one(
                    {"_id": ObjectId(video_id)},
                    {
                        "$pull": {"disliked_by": user_id},
                        "$inc": {"dislikes": -1}
                    }
                )
                return "undisliked"
            else:
                # Remove from like if present
                if user_id in liked_by:
                    self.collection.update_one(
                        {"_id": ObjectId(video_id)},
                        {
                            "$pull": {"liked_by": user_id},
                            "$inc": {"likes": -1}
                        }
                    )
                
                # Add to dislikes
                self.collection.update_one(
                    {"_id": ObjectId(video_id)},
                    {
                        "$addToSet": {"disliked_by": user_id},
                        "$inc": {"dislikes": 1}
                    }
                )
                return "disliked"
        except Exception as e:
            print(f"Error in dislike: {e}")
            return None
    
    def has_liked(self, video_id: str, user_id: str):
        """Check if user has liked the video"""
        try:
            video = self.collection.find_one({"_id": ObjectId(video_id)})
            if not video:
                return False
            return user_id in video.get('liked_by', [])
        except:
            return False
    
    def has_disliked(self, video_id: str, user_id: str):
        """Check if user has disliked the video"""
        try:
            video = self.collection.find_one({"_id": ObjectId(video_id)})
            if not video:
                return False
            return user_id in video.get('disliked_by', [])
        except:
            return False
    
    def search(self, query: str, filters: dict = None):
        """Search videos"""
        search_query = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"tags": {"$regex": query, "$options": "i"}}
            ]
        }
        
        if filters:
            search_query.update(filters)
        
        return list(self.collection.find(search_query).sort("created_at", -1))
    
    def get_top_videos(self, sort_by="views", limit=10):
        """Get top videos"""
        return list(self.collection.find().sort(sort_by, -1).limit(limit))
    
    def get_all(self, limit=None):
        """Get all public videos with optional limit"""
        query = {'visibility': 'Public'}
        videos = self.collection.find(query).sort('created_at', -1)
        
        if limit:
            videos = videos.limit(limit)
        
        return list(videos)