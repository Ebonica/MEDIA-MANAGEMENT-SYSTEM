from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from config.settings import settings
import streamlit as st

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish MongoDB connection"""
        if self._client is None:
            try:
                self._client = MongoClient(settings.MONGODB_URI)
                self._db = self._client[settings.DATABASE_NAME]
                # Test connection
                self._client.admin.command('ping')
                self._create_indexes()
                return True
            except ConnectionFailure as e:
                st.error(f"Failed to connect to MongoDB: {e}")
                return False
        return True
    
    def _create_indexes(self):
        """Create database indexes for optimization"""
        try:
            # Users collection indexes
            self._db.users.create_index([("username", ASCENDING)], unique=True)
            self._db.users.create_index([("email", ASCENDING)], unique=True)
            
            # Channels collection indexes
            self._db.channels.create_index([("channel_name", ASCENDING)])
            self._db.channels.create_index([("creator_id", ASCENDING)])
            
            # Videos collection indexes
            self._db.videos.create_index([("title", ASCENDING)])
            self._db.videos.create_index([("channel_id", ASCENDING)])
            self._db.videos.create_index([("creator_id", ASCENDING)])
            self._db.videos.create_index([("views", DESCENDING)])
            self._db.videos.create_index([("likes", DESCENDING)])
            self._db.videos.create_index([("created_at", DESCENDING)])
            
            # Playlists collection indexes
            self._db.playlists.create_index([("creator_id", ASCENDING)])
            
            # Comments collection indexes
            self._db.comments.create_index([("video_id", ASCENDING)])
            self._db.comments.create_index([("parent_id", ASCENDING)])
            
        except Exception as e:
            print(f"Error creating indexes: {e}")
    
    def get_db(self):
        """Get database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

# Global database instance
db = Database()