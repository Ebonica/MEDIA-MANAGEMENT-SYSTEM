from datetime import datetime
from config.database import db
from bson import ObjectId

class ChannelModel:
    def __init__(self):
        self.collection = db.get_db().channels
    
    def create(self, channel_data: dict):
        """Create a new channel"""
        channel_data['created_at'] = datetime.now()
        channel_data['subscribers'] = 0
        channel_data['total_views'] = 0
        channel_data['subscribers_list'] = []  # Initialize empty subscribers list
        result = self.collection.insert_one(channel_data)
        return str(result.inserted_id)
    
    def get_by_id(self, channel_id: str):
        """Get channel by ID"""
        try:
            return self.collection.find_one({"_id": ObjectId(channel_id)})
        except:
            return None
    
    def get_by_creator(self, creator_id: str):
        """Get all channels by creator"""
        return list(self.collection.find({"creator_id": creator_id}))
    
    def get_all(self, limit=None):
        """Get all channels"""
        query = self.collection.find()
        if limit:
            query = query.limit(limit)
        return list(query)
    
    def update(self, channel_id: str, data: dict):
        """Update channel"""
        try:
            return self.collection.update_one(
                {"_id": ObjectId(channel_id)},
                {"$set": data}
            )
        except:
            return None
    
    def delete(self, channel_id: str):
        """Delete channel"""
        try:
            return self.collection.delete_one({"_id": ObjectId(channel_id)})
        except:
            return None
    
    def is_user_subscribed(self, channel_id: str, user_id: str):
        """
        Check if a user is subscribed to a channel
        
        Args:
            channel_id: The channel ID
            user_id: The user ID
        
        Returns:
            bool: True if subscribed, False otherwise
        """
        try:
            channel = self.collection.find_one({
                '_id': ObjectId(channel_id),
                'subscribers_list': user_id
            })
            return channel is not None
        except Exception as e:
            print(f"Error checking subscription: {e}")
            return False
    
    def subscribe(self, channel_id: str, user_id: str):
        """
        Subscribe a user to a channel (only if not already subscribed)
        
        Args:
            channel_id: The channel ID
            user_id: The user ID
        
        Returns:
            bool: True if successfully subscribed, False if already subscribed
        """
        try:
            # Check if already subscribed
            if self.is_user_subscribed(channel_id, user_id):
                return False
            
            # Add user to subscribers list and increment count
            result = self.collection.update_one(
                {'_id': ObjectId(channel_id)},
                {
                    '$addToSet': {'subscribers_list': user_id},  # Prevents duplicates
                    '$inc': {'subscribers': 1}
                }
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error subscribing: {e}")
            return False
    
    def unsubscribe(self, channel_id: str, user_id: str):
        """
        Unsubscribe a user from a channel
        
        Args:
            channel_id: The channel ID
            user_id: The user ID
        
        Returns:
            bool: True if successfully unsubscribed, False otherwise
        """
        try:
            # Check if user is subscribed before unsubscribing
            if not self.is_user_subscribed(channel_id, user_id):
                return False
            
            # Remove user from subscribers list and decrement count
            result = self.collection.update_one(
                {'_id': ObjectId(channel_id)},
                {
                    '$pull': {'subscribers_list': user_id},
                    '$inc': {'subscribers': -1}
                }
            )
            
            # Ensure subscribers count doesn't go below 0
            self.collection.update_one(
                {'_id': ObjectId(channel_id), 'subscribers': {'$lt': 0}},
                {'$set': {'subscribers': 0}}
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error unsubscribing: {e}")
            return False
    
    def get_subscribed_channels(self, user_id: str):
        """
        Get all channels a user is subscribed to
        
        Args:
            user_id: The user ID
        
        Returns:
            list: List of channel documents
        """
        try:
            return list(self.collection.find({
                'subscribers_list': user_id
            }).sort('channel_name', 1))
        except Exception as e:
            print(f"Error getting subscribed channels: {e}")
            return []
    
    def get_subscriber_count(self, channel_id: str):
        """
        Get the number of subscribers for a channel
        
        Args:
            channel_id: The channel ID
        
        Returns:
            int: Number of subscribers
        """
        try:
            channel = self.collection.find_one(
                {'_id': ObjectId(channel_id)},
                {'subscribers': 1}
            )
            return channel.get('subscribers', 0) if channel else 0
        except Exception as e:
            print(f"Error getting subscriber count: {e}")
            return 0
    
    def get_channel_analytics(self, channel_id: str):
        """Get channel analytics"""
        try:
            channel = self.get_by_id(channel_id)
            if not channel:
                return None
            
            database = db.get_db()
            
            # Get video count
            video_count = database.videos.count_documents({"channel_id": channel_id})
            
            # Get total views
            pipeline = [
                {"$match": {"channel_id": channel_id}},
                {"$group": {"_id": None, "total_views": {"$sum": "$views"}, "total_likes": {"$sum": "$likes"}}}
            ]
            result = list(database.videos.aggregate(pipeline))
            
            total_views = result[0]['total_views'] if result else 0
            total_likes = result[0]['total_likes'] if result else 0
            
            return {
                "subscribers": channel.get('subscribers', 0),
                "videos": video_count,
                "total_views": total_views,
                "total_likes": total_likes
            }
        except:
            return None