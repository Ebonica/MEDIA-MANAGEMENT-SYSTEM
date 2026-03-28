import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "youtube_media_db")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Application settings
    APP_NAME = "YouTube Media System"
    APP_VERSION = "1.0.0"
    
    # User roles
    ROLE_ADMIN = "Admin"
    ROLE_CREATOR = "Creator"
    ROLE_VIEWER = "Viewer"
    
    # Video categories
    VIDEO_CATEGORIES = [
        "Education", "Entertainment", "Music", "Gaming", 
        "News", "Sports", "Technology", "Science", 
        "Travel", "Food", "Fashion", "Health", "Other"
    ]
    
    # Pagination
    ITEMS_PER_PAGE = 10

settings = Settings()