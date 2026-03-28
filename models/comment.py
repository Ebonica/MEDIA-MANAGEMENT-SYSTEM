from datetime import datetime, timedelta
from config.database import db
from bson import ObjectId

class CommentModel:
    def __init__(self):
        self.collection = db.get_db().comments
    
    def create(self, comment_data: dict):
        """Create a new comment with duplicate prevention"""
        # Check for duplicate comments in the last 5 seconds
        recent_duplicate = self.collection.find_one({
            'video_id': comment_data['video_id'],
            'user_id': comment_data['user_id'],
            'text': comment_data['text'],
            'parent_id': comment_data.get('parent_id'),
            'created_at': {'$gte': datetime.now() - timedelta(seconds=5)}
        })
        
        if recent_duplicate:
            # Return existing comment ID instead of creating duplicate
            return str(recent_duplicate['_id'])
        
        # Create new comment
        comment_data['created_at'] = datetime.now()
        comment_data['likes'] = 0
        comment_data['liked_by'] = []
        comment_data['is_edited'] = False
        result = self.collection.insert_one(comment_data)
        return str(result.inserted_id)
    
    def get_by_id(self, comment_id: str):
        """Get comment by ID"""
        try:
            return self.collection.find_one({"_id": ObjectId(comment_id)})
        except:
            return None
    
    def get_by_video(self, video_id: str, parent_id=None):
        """Get comments for a video"""
        query = {"video_id": video_id}
        if parent_id:
            query["parent_id"] = parent_id
        else:
            query["parent_id"] = None
        
        return list(self.collection.find(query).sort("created_at", -1))
    
    def get_replies(self, comment_id: str):
        """Get replies to a comment"""
        return list(self.collection.find({"parent_id": comment_id}).sort("created_at", 1))
    
    def update(self, comment_id: str, text: str):
        """Update comment"""
        try:
            return self.collection.update_one(
                {"_id": ObjectId(comment_id)},
                {"$set": {"text": text, "is_edited": True}}
            )
        except:
            return None
    
    def delete(self, comment_id: str):
        """Delete comment and all replies"""
        try:
            self.collection.delete_one({"_id": ObjectId(comment_id)})
            self.collection.delete_many({"parent_id": comment_id})
            return True
        except:
            return False
    
    def like(self, comment_id: str, user_id: str):
        """Toggle like on a comment"""
        try:
            comment = self.collection.find_one({'_id': ObjectId(comment_id)})
            if not comment:
                return None
            
            liked_by = comment.get('liked_by', [])
            
            if user_id in liked_by:
                result = self.collection.update_one(
                    {'_id': ObjectId(comment_id)},
                    {
                        '$pull': {'liked_by': user_id},
                        '$inc': {'likes': -1}
                    }
                )
                return "unliked" if result.modified_count > 0 else None
            else:
                result = self.collection.update_one(
                    {'_id': ObjectId(comment_id)},
                    {
                        '$addToSet': {'liked_by': user_id},
                        '$inc': {'likes': 1}
                    }
                )
                return "liked" if result.modified_count > 0 else None
        except Exception as e:
            print(f"Error in like function: {e}")
            return None