import bcrypt
import streamlit as st
from datetime import datetime
from config.database import db

class Auth:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def login(username: str, password: str) -> dict:
        """Authenticate user and return user data"""
        database = db.get_db()
        user = database.users.find_one({"username": username})
        
        if user and Auth.verify_password(password, user['password']):
            # Update last login
            database.users.update_one(
                {"_id": user['_id']},
                {"$set": {"last_login": datetime.now()}}
            )
            
            # Remove password from returned data
            user.pop('password', None)
            return user
        return None
    
    @staticmethod
    def register(username: str, email: str, password: str, role: str) -> tuple:
        """Register a new user"""
        database = db.get_db()
        
        # Check if username or email already exists
        if database.users.find_one({"username": username}):
            return False, "Username already exists"
        
        if database.users.find_one({"email": email}):
            return False, "Email already exists"
        
        # Create user document
        user_doc = {
            "username": username,
            "email": email,
            "password": Auth.hash_password(password),
            "role": role,
            "created_at": datetime.now(),
            "last_login": None,
            "profile_image": None,
            "bio": "",
            "is_active": True
        }
        
        result = database.users.insert_one(user_doc)
        return True, str(result.inserted_id)
    
    @staticmethod
    def logout():
        """Clear session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return 'user' in st.session_state and st.session_state.user is not None
    
    @staticmethod
    def get_current_user():
        """Get current logged-in user"""
        return st.session_state.get('user', None)
    
    @staticmethod
    def require_auth(roles=None):
        """Decorator to require authentication"""
        if not Auth.is_authenticated():
            st.warning("Please login to access this page")
            st.stop()
        
        if roles:
            user = Auth.get_current_user()
            if user['role'] not in roles:
                st.error("You don't have permission to access this page")
                st.stop()