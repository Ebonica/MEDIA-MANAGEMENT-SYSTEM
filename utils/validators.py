import re

class Validators:
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_username(username: str) -> tuple:
        """Validate username"""
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 30:
            return False, "Username must be less than 30 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> tuple:
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if len(password) > 50:
            return False, "Password must be less than 50 characters"
        return True, ""
    
    @staticmethod
    def validate_channel_name(name: str) -> tuple:
        """Validate channel name"""
        if len(name) < 3:
            return False, "Channel name must be at least 3 characters"
        if len(name) > 50:
            return False, "Channel name must be less than 50 characters"
        return True, ""
    
    @staticmethod
    def validate_video_title(title: str) -> tuple:
        """Validate video title"""
        if len(title) < 3:
            return False, "Video title must be at least 3 characters"
        if len(title) > 100:
            return False, "Video title must be less than 100 characters"
        return True, ""