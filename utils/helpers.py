from datetime import datetime
import streamlit as st

class Helpers:
    @staticmethod
    def format_number(num: int) -> str:
        """Format large numbers (e.g., 1000 -> 1K)"""
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        return str(num)
    
    @staticmethod
    def time_ago(dt: datetime) -> str:
        """Convert datetime to 'time ago' format"""
        if dt is None:
            return "Never"
        
        now = datetime.now()
        diff = now - dt
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 2592000:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif seconds < 31536000:
            months = int(seconds / 2592000)
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = int(seconds / 31536000)
            return f"{years} year{'s' if years != 1 else ''} ago"
    
    @staticmethod
    def display_video_card(video: dict):
        """Display a video card"""
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if video.get('thumbnail'):
                st.image(video['thumbnail'], use_column_width=True)
            else:
                st.image("https://via.placeholder.com/300x200?text=No+Thumbnail", use_column_width=True)
        
        with col2:
            st.markdown(f"### {video['title']}")
            st.caption(f"👁️ {Helpers.format_number(video.get('views', 0))} views • "
                      f"👍 {Helpers.format_number(video.get('likes', 0))} likes")
            st.caption(f"📅 {Helpers.time_ago(video.get('created_at'))}")
            if video.get('description'):
                st.text(video['description'][:100] + "..." if len(video['description']) > 100 else video['description'])

def navigate_to(page_name):
    """Helper function for navigation"""
    st.session_state.navigate_to = page_name
    st.rerun()