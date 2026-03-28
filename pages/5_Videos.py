# ============================================================================
# FILE: pages/Video_Management.py - FIXED DUPLICATE COMMENTS ISSUE
# ============================================================================
import streamlit as st
from utils.auth import Auth
from models.video import VideoModel
from models.channel import ChannelModel
from models.comment import CommentModel
from utils.validators import Validators
from utils.helpers import Helpers
from config.settings import settings
from config.database import db
from models.user import UserModel
import os
import hashlib
import time

st.set_page_config(page_title="Video Management", page_icon="🎬", layout="wide")

from utils.ui import sidebar_v2

with st.sidebar:
    sidebar_v2()

Auth.require_auth()


# Modern CSS Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Page Header */
.page-header {
    background: rgba(255, 255, 255, 0.98);
    padding: 30px 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    text-align: center;
}

.page-title {
    font-size: 36px;
    font-weight: 700;
    color: #1a202c;
    margin: 0;
}

.page-subtitle {
    font-size: 16px;
    color: #718096;
    margin-top: 8px;
}

/* Tabs Styling */
.stTabs {
    background: rgba(255, 255, 255, 0.98);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #f7fafc;
    padding: 8px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    color: #4a5568;
    background: transparent;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
}

/* Video Card - Modern Design */
.video-card-modern {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    border: 2px solid #e2e8f0;
}

.video-card-modern:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
    border-color: #667eea;
}

/* Thumbnail Container */
.thumbnail-container {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Thumbnail Placeholder */
.thumbnail-placeholder {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 60px 20px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.thumbnail-placeholder:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.15);
}

.placeholder-emoji {
    font-size: 4rem;
    margin-bottom: 10px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.placeholder-title {
    color: white;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 5px;
}

.placeholder-subtitle {
    color: rgba(255,255,255,0.8);
    font-size: 0.9rem;
}

/* Upload Placeholder */
.upload-placeholder {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 12px;
    padding: 40px 20px;
    text-align: center;
    border: 2px dashed rgba(255,255,255,0.3);
    transition: all 0.3s ease;
}

.upload-placeholder:hover {
    border-color: rgba(255,255,255,0.6);
    transform: scale(1.02);
}

/* Text Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    background: #f8fafc !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    background: white !important;
}

.stTextInput > label,
.stTextArea > label,
.stSelectbox > label {
    font-weight: 600 !important;
    color: #2d3748 !important;
    font-size: 14px !important;
    margin-bottom: 5px !important;
}

/* Buttons - Primary */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4) !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

/* Buttons - Secondary */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(72, 187, 120, 0.3) !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="baseButton-secondary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(72, 187, 120, 0.5) !important;
}

/* Regular Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(66, 153, 225, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(66, 153, 225, 0.5) !important;
}

/* Form Submit Buttons */
.stForm .stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 24px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4) !important;
}

.stForm .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

/* Metrics */
.stMetric {
    background: linear-gradient(135deg, #f7fafc, #edf2f7);
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
}

.stMetric label {
    color: #4a5568 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}

.stMetric [data-testid="stMetricValue"] {
    color: #1a202c !important;
    font-weight: 700 !important;
}

/* Comment Section */
.comment-section {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
    border-left: 4px solid #667eea;
}

.comment-item {
    background: white;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
}

.comment-author {
    font-weight: 600;
    color: #667eea;
}

.comment-time {
    color: #999;
    font-size: 0.85rem;
}

/* Reply Box */
.reply-box {
    background: #f0f4ff;
    border-left: 3px solid #667eea;
    padding: 0.8rem;
    margin-left: 2rem;
    margin-top: 0.3rem;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
}

/* Video Player Container */
.video-player-container {
    background: #000;
    border-radius: 12px;
    overflow: hidden;
    margin: 1rem 0;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

/* Video Title */
.video-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 0.5rem;
    line-height: 1.3;
}

/* Category Badge */
.category-badge {
    display: inline-block;
    background: linear-gradient(135deg, #FF6B6B, #ee5a52);
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-right: 10px;
    box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
}

/* Tags */
.tag {
    display: inline-block;
    background: #E8F5E9;
    color: #2E7D32;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.8rem;
    margin: 3px;
    border: 1px solid #C8E6C9;
}

/* Upload Section */
.upload-section {
    background: white;
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
    border: 2px dashed #667eea;
}

/* Empty State */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: white;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

/* Info/Warning/Success/Error boxes */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 12px !important;
    padding: 16px 20px !important;
    margin: 12px 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* Caption Text */
.stCaption {
    color: #718096 !important;
    font-size: 13px !important;
}

/* Form Styling */
.stForm {
    background: #f8fafc;
    padding: 24px;
    border-radius: 16px;
    border: 2px solid #e2e8f0;
}

/* Divider */
hr {
    margin: 24px 0;
    border: none;
    border-top: 2px solid #e2e8f0;
}

/* Container */
.block-container {
    padding: 2rem 1rem !important;
    max-width: 1400px !important;
}

/* Responsive */
@media (max-width: 768px) {
    .page-header {
        padding: 20px;
    }
    
    .page-title {
        font-size: 28px;
    }
    
    .stTabs {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align: center; color: #667eea;">🎬 Video Management</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Manage your video content with ease</p>', unsafe_allow_html=True)

user = Auth.get_current_user()
video_model = VideoModel()
channel_model = ChannelModel()
comment_model = CommentModel()

# Initialize tracking - FIXED
if 'last_video_submission' not in st.session_state:
    st.session_state.last_video_submission = None
if 'uploading' not in st.session_state:
    st.session_state.uploading = False
if 'comment_submissions' not in st.session_state:
    st.session_state.comment_submissions = {}
if 'reply_submissions' not in st.session_state:
    st.session_state.reply_submissions = {}
if 'action_performed' not in st.session_state:
    st.session_state.action_performed = False

# Helper functions
def save_uploaded_file(uploaded_file, video_id):
    try:
        upload_dir = "uploads/videos"
        os.makedirs(upload_dir, exist_ok=True)
        file_extension = uploaded_file.name.split('.')[-1]
        filename = f"{video_id}.{file_extension}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def save_uploaded_thumbnail(uploaded_file, video_id):
    try:
        upload_dir = "uploads/thumbnails"
        os.makedirs(upload_dir, exist_ok=True)
        file_extension = uploaded_file.name.split('.')[-1]
        filename = f"{video_id}_thumb.{file_extension}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error saving thumbnail: {e}")
        return None

def display_video(video_path):
    try:
        with open(video_path, "rb") as f:
            video_bytes = f.read()
        st.video(video_bytes)
    except Exception as e:
        st.error(f"Could not load video: {e}")

def get_category_emoji(category):
    """Get emoji based on video category"""
    category_emojis = {
        'Education': '📚',
        'Entertainment': '🎭',
        'Gaming': '🎮',
        'Music': '🎵',
        'Sports': '⚽',
        'Technology': '💻',
        'News': '📰',
        'Cooking': '👨‍🍳',
        'Travel': '✈️',
        'Fashion': '👗',
        'Health': '💪',
        'Science': '🔬',
        'Art': '🎨',
        'Comedy': '😂',
        'Vlog': '📹',
        'Tutorial': '🎓',
        'Review': '⭐',
        'Documentary': '🎬',
        'Animation': '🎞️',
        'Podcast': '🎙️',
        'DIY': '🔨',
        'Finance': '💰',
        'Business': '💼',
        'Lifestyle': '🌟',
        'Pets': '🐾',
        'Other': '🎬'
    }
    return category_emojis.get(category, '🎬')

def get_random_thumbnail_message():
    """Get a random encouraging message for thumbnail upload"""
    import random
    messages = [
        "Make your video stand out!",
        "First impressions matter!",
        "Add a catchy thumbnail!",
        "Eye-catching = More clicks!",
        "Show them what it's about!",
        "Make it pop!",
        "Grab their attention!",
        "Picture perfect moment!"
    ]
    return random.choice(messages)

def display_comment_with_replies(comment, video_id, level=0):
    """Display a comment with all its replies - FIXED"""
    comment_id_str = str(comment['_id'])
    
    # Use reply-box class for nested comments
    box_class = "reply-box" if level > 0 else "comment-item"
    
    st.markdown(f'<div class="{box_class}">', unsafe_allow_html=True)
    
    col_a, col_b = st.columns([4, 1])
    
    with col_a:
        st.markdown(f'<span class="comment-author">👤 {comment["username"]}</span>', unsafe_allow_html=True)
        st.markdown(f'<span class="comment-time">{Helpers.time_ago(comment["created_at"])}</span>', unsafe_allow_html=True)
        st.markdown(comment['text'])
        if comment.get('is_edited'):
            st.caption("✏️ (edited)")
    
    with col_b:
        # Check if user has liked this comment
        comment_liked_by = comment.get('liked_by', [])
        user_has_liked_comment = str(user['_id']) in comment_liked_by
        
        st.caption(f"👍 {comment.get('likes', 0)}")
        like_icon = "💙" if user_has_liked_comment else "👍"
        if st.button(like_icon, key=f"like_c_{comment_id_str}_{level}"):
            comment_model.like(comment_id_str, str(user['_id']))
            time.sleep(0.3)
            st.rerun()
    
    # Action buttons for owner/admin
    if str(comment['user_id']) == str(user['_id']) or user['role'] == 'Admin':
        col1, col2, col3 = st.columns([1, 1, 8])
        
        with col1:
            if st.button("✏️ Edit", key=f"edit_c_{comment_id_str}_{level}"):
                st.session_state[f'editing_comment_{comment_id_str}'] = not st.session_state.get(f'editing_comment_{comment_id_str}', False)
        
        with col2:
            if st.button("🗑️ Delete", key=f"delete_c_{comment_id_str}_{level}"):
                comment_model.delete(comment_id_str)
                st.success("Comment deleted!")
                time.sleep(0.3)
                st.rerun()
    
    # Reply button for all users (limited nesting)
    if level < 2:  # Allow replies up to 2 levels deep
        if st.button("💬 Reply", key=f"reply_btn_{comment_id_str}_{level}"):
            st.session_state[f'replying_to_{comment_id_str}'] = not st.session_state.get(f'replying_to_{comment_id_str}', False)
    
    # Edit form
    if st.session_state.get(f'editing_comment_{comment_id_str}', False):
        with st.form(f"edit_comment_form_{comment_id_str}"):
            new_text = st.text_area("Edit comment", value=comment['text'], key=f"edit_text_{comment_id_str}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save"):
                    if new_text and new_text.strip():
                        comment_model.update(comment_id_str, new_text.strip())
                        st.session_state[f'editing_comment_{comment_id_str}'] = False
                        st.success("Comment updated!")
                        time.sleep(0.3)
                        st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state[f'editing_comment_{comment_id_str}'] = False
    
    # Reply form - FIXED
    if st.session_state.get(f'replying_to_{comment_id_str}', False):
        # Initialize reply tracking
        if 'reply_submissions' not in st.session_state:
            st.session_state.reply_submissions = {}
        
        with st.form(f"reply_form_{comment_id_str}", clear_on_submit=True):
            reply_text = st.text_area("Write a reply", key=f"reply_text_{comment_id_str}")
            
            col1, col2 = st.columns(2)
            with col1:
                submit_reply = st.form_submit_button("📤 Post Reply")
                
                if submit_reply:
                    if not reply_text or not reply_text.strip():
                        st.error("❌ Reply cannot be empty")
                    else:
                        # Create unique submission ID
                        submission_id = hashlib.md5(
                            f"{reply_text.strip()}{user['_id']}{comment_id_str}".encode()
                        ).hexdigest()
                        
                        reply_key = f'reply_{comment_id_str}'
                        
                        # Check for duplicate
                        if reply_key in st.session_state.reply_submissions:
                            if submission_id == st.session_state.reply_submissions[reply_key]:
                                st.warning("⚠️ This reply has already been posted!")
                            else:
                                # New reply - proceed
                                reply_data = {
                                    'video_id': video_id,
                                    'user_id': str(user['_id']),
                                    'username': user['username'],
                                    'text': reply_text.strip(),
                                    'parent_id': comment_id_str
                                }
                                comment_model.create(reply_data)
                                st.session_state.reply_submissions[reply_key] = submission_id
                                st.session_state[f'replying_to_{comment_id_str}'] = False
                                st.success("✅ Reply posted!")
                                time.sleep(0.3)
                                st.rerun()
                        else:
                            # First reply - proceed
                            reply_data = {
                                'video_id': video_id,
                                'user_id': str(user['_id']),
                                'username': user['username'],
                                'text': reply_text.strip(),
                                'parent_id': comment_id_str
                            }
                            comment_model.create(reply_data)
                            st.session_state.reply_submissions[reply_key] = submission_id
                            st.session_state[f'replying_to_{comment_id_str}'] = False
                            st.success("✅ Reply posted!")
                            time.sleep(0.3)
                            st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state[f'replying_to_{comment_id_str}'] = False
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display replies recursively
    if level < 3:  # Limit nesting depth
        replies = comment_model.get_replies(comment_id_str)
        if replies:
            for reply in replies:
                display_comment_with_replies(reply, video_id, level + 1)

# Success message
if 'video_uploaded' in st.session_state and st.session_state.video_uploaded:
    st.success("✅ Video uploaded successfully!")
    st.balloons()
    del st.session_state.video_uploaded

# Tabs
tab1, tab2 = st.tabs(["📺 My Videos", "⬆️ Upload Video"])

# ============================================================================
# TAB 1: MY VIDEOS - FIXED
# ============================================================================
with tab1:
    # Different behavior for Viewers vs Creators/Admins
    if user['role'] in ['Creator', 'Admin']:
        # Creators/Admins see their own videos
        my_videos = video_model.get_by_creator(str(user['_id']))
        st.markdown("### 🎬 My Videos")
    else:
        # Viewers see all public videos
        my_videos = video_model.get_all()  # You need to add this method to VideoModel
        st.markdown("### 🎬 All Videos")
        st.caption("👀 Viewing mode - You can watch and interact with videos")
    

    
    if my_videos:
        st.caption(f"📊 Total Videos: {len(my_videos)}")
    
    if not my_videos:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🎬</div>
            <h2>No Videos Yet</h2>
            <p style="color: #666;">Upload your first video to get started!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display videos
        for idx, video in enumerate(my_videos):
            with st.container():
                col1, col2 = st.columns([1, 2])
            
            with col1:
                if video.get('thumbnail_path') and os.path.exists(video['thumbnail_path']):
                    st.image(video['thumbnail_path'], use_column_width=True)
                else:
                    # Custom placeholder for missing thumbnail with category-specific emoji
                    category_emoji = get_category_emoji(video.get('category', 'Other'))
                    st.markdown(f"""
                    <div class="thumbnail-placeholder">
                        <div class="placeholder-emoji">{category_emoji}</div>
                        <div class="placeholder-title">No Thumbnail</div>
                        <div class="placeholder-subtitle">{video.get('category', 'Video')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="video-title">{video["title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<span class="category-badge">{video.get("category", "General")}</span>', unsafe_allow_html=True)
                st.caption(f"📅 {Helpers.time_ago(video.get('created_at'))}")
                
                if video.get('description'):
                    st.markdown(f"{video['description'][:150]}...")
                
                if video.get('tags'):
                    tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in video.get('tags', [])[:6]])
                    st.markdown(tags_html, unsafe_allow_html=True)
            
            # Stats row - FRESH DATA from database
            video_comments = comment_model.get_by_video(str(video['_id']))
            comment_count = len(video_comments)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👁️ Views", Helpers.format_number(video.get('views', 0)))
            
            with col2:
                st.metric("👍 Likes", Helpers.format_number(video.get('likes', 0)))
            
            with col3:
                st.metric("💬 Comments", comment_count)
            
            with col4:
                like_ratio = 0
                if video.get('views', 0) > 0:
                    like_ratio = (video.get('likes', 0) / video.get('views', 0)) * 100
                st.metric("📊 Engagement", f"{like_ratio:.1f}%")
            
            # Action buttons
# Action buttons - Different for Viewers vs Creators
            st.markdown("---")
            
            if user['role'] in ['Creator', 'Admin'] and str(video.get('creator_id')) == str(user['_id']):
                # Full controls for video owner
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    if st.button("▶️ Play", key=f"play_{video['_id']}", use_container_width=True):
                        st.session_state[f'playing_{video["_id"]}'] = not st.session_state.get(f'playing_{video["_id"]}', False)
                        if st.session_state[f'playing_{video["_id"]}']:
                            video_model.increment_views(str(video['_id']))
                
                with col2:
                    user_has_liked = video_model.has_liked(str(video['_id']), str(user['_id']))
                    like_button_text = "💙 Liked" if user_has_liked else "👍 Like"
                    
                    if st.button(like_button_text, key=f"like_{video['_id']}", use_container_width=True):
                        result = video_model.like(str(video['_id']), str(user['_id']))
                        if result == "liked":
                            st.success("👍 Liked!")
                        elif result == "unliked":
                            st.info("Unlike successful")
                        time.sleep(0.3)
                        st.rerun()
                
                with col3:
                    if st.button("💬 Comments", key=f"comments_{video['_id']}", use_container_width=True):
                        st.session_state[f'show_comments_{video["_id"]}'] = not st.session_state.get(f'show_comments_{video["_id"]}', False)
                
                with col4:
                    if st.button("✏️ Edit", key=f"edit_{video['_id']}", use_container_width=True):
                        st.session_state[f'editing_{video["_id"]}'] = not st.session_state.get(f'editing_{video["_id"]}', False)
                
                with col5:
                    if st.button("🗑️ Delete", key=f"delete_{video['_id']}", use_container_width=True, type="secondary"):
                        if video.get('video_path') and os.path.exists(video['video_path']):
                            os.remove(video['video_path'])
                        if video.get('thumbnail_path') and os.path.exists(video['thumbnail_path']):
                            os.remove(video['thumbnail_path'])
                        video_model.delete(str(video['_id']))
                        st.success("Video deleted!")
                        time.sleep(0.3)
                        st.rerun()
            else:
                # Limited controls for Viewers
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("▶️ Play", key=f"play_{video['_id']}", use_container_width=True):
                        st.session_state[f'playing_{video["_id"]}'] = not st.session_state.get(f'playing_{video["_id"]}', False)
                        if st.session_state[f'playing_{video["_id"]}']:
                            video_model.increment_views(str(video['_id']))
                
                with col2:
                    user_has_liked = video_model.has_liked(str(video['_id']), str(user['_id']))
                    like_button_text = "💙 Liked" if user_has_liked else "👍 Like"
                    
                    if st.button(like_button_text, key=f"like_{video['_id']}", use_container_width=True):
                        result = video_model.like(str(video['_id']), str(user['_id']))
                        if result == "liked":
                            st.success("👍 Liked!")
                        elif result == "unliked":
                            st.info("Unlike successful")
                        time.sleep(0.3)
                        st.rerun()
                
                with col3:
                    if st.button("💬 Comments", key=f"comments_{video['_id']}", use_container_width=True):
                        st.session_state[f'show_comments_{video["_id"]}'] = not st.session_state.get(f'show_comments_{video["_id"]}', False)
            
            # Video player
            if st.session_state.get(f'playing_{video["_id"]}', False):
                st.markdown('<div class="video-player-container">', unsafe_allow_html=True)
                if video.get('video_path') and os.path.exists(video['video_path']):
                    display_video(video['video_path'])
                st.markdown('</div>', unsafe_allow_html=True)
                
                if st.button("⏸️ Close Player", key=f"close_{video['_id']}"):
                    st.session_state[f'playing_{video["_id"]}'] = False
            
            # Comments section - FIXED DUPLICATE ISSUE
            if st.session_state.get(f'show_comments_{video["_id"]}', False):
                st.markdown('<div class="comment-section">', unsafe_allow_html=True)
                st.markdown("### 💬 Comments")
                
                # Initialize submission tracking for this video if not exists
                video_key = f'video_{video["_id"]}'
                if 'comment_submissions' not in st.session_state:
                    st.session_state.comment_submissions = {}
                
                # Add comment form
                with st.form(f"add_comment_{video['_id']}", clear_on_submit=True):
                    new_comment = st.text_area("Add a comment", key=f"comment_text_{video['_id']}", placeholder="Share your thoughts...")
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        submit_button = st.form_submit_button("📤 Post", use_container_width=True)
                        
                    if submit_button:
                        # Validate comment
                        if not new_comment or not new_comment.strip():
                            st.error("❌ Comment cannot be empty")
                        else:
                            # Create unique submission ID based on content + user + video
                            submission_id = hashlib.md5(
                                f"{new_comment.strip()}{user['_id']}{video['_id']}".encode()
                            ).hexdigest()
                            
                            # Check if this exact comment was already submitted
                            if video_key in st.session_state.comment_submissions:
                                if submission_id == st.session_state.comment_submissions[video_key]:
                                    st.warning("⚠️ This comment has already been posted!")
                                else:
                                    # Different comment - proceed with submission
                                    comment_data = {
                                        'video_id': str(video['_id']),
                                        'user_id': str(user['_id']),
                                        'username': user['username'],
                                        'text': new_comment.strip(),
                                        'parent_id': None
                                    }
                                    
                                    comment_model.create(comment_data)
                                    st.session_state.comment_submissions[video_key] = submission_id
                                    st.success("✅ Comment posted!")
                                    time.sleep(0.5)
                                    st.rerun()
                            else:
                                # First comment for this video - proceed
                                comment_data = {
                                    'video_id': str(video['_id']),
                                    'user_id': str(user['_id']),
                                    'username': user['username'],
                                    'text': new_comment.strip(),
                                    'parent_id': None
                                }
                                
                                comment_model.create(comment_data)
                                st.session_state.comment_submissions[video_key] = submission_id
                                st.success("✅ Comment posted!")
                                time.sleep(0.3)
                                st.rerun()
                
                # Display comments - FRESH from database
                video_comments = comment_model.get_by_video(str(video['_id']))
                
                if video_comments:
                    st.caption(f"📊 {len(video_comments)} comment(s)")
                    
                    # Separate top-level comments and replies
                    top_level_comments = [c for c in video_comments if not c.get('parent_id')]
                    
                    for comment in top_level_comments:
                        display_comment_with_replies(comment, str(video['_id']), level=0)
                else:
                    st.info("💭 No comments yet. Be the first to comment!")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Edit form
            if st.session_state.get(f'editing_{video["_id"]}', False):
                with st.form(f"edit_form_{video['_id']}"):
                    st.markdown("### ✏️ Edit Video")
                    
                    new_title = st.text_input("Title", value=video['title'])
                    new_desc = st.text_area("Description", value=video.get('description', ''))
                    new_tags = st.text_input("Tags", value=', '.join(video.get('tags', [])))
                    new_category = st.selectbox("Category", settings.VIDEO_CATEGORIES,
                                               index=settings.VIDEO_CATEGORIES.index(video.get('category', 'Other')))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("💾 Save", use_container_width=True):
                            tags_list = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
                            video_model.update(str(video['_id']), {
                                'title': new_title,
                                'description': new_desc,
                                'tags': tags_list,
                                'category': new_category
                            })
                            st.session_state[f'editing_{video["_id"]}'] = False
                            st.success("Updated!")
                            time.sleep(0.3)
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                            st.session_state[f'editing_{video["_id"]}'] = False
            
            # Divider between videos
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================================
# TAB 2: UPLOAD VIDEO
# ============================================================================
with tab2:
    if user['role'] not in ['Creator', 'Admin']:
        st.warning("⚠️ Only Creators can upload videos")
        st.stop()
    
    my_channels = channel_model.get_by_creator(str(user['_id']))
    
    if not my_channels:
        st.warning("⚠️ Create a channel first!")
        st.info("👉 Navigate to **Channel Management**")
    else:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### ⬆️ Upload New Video")
        st.caption("Share your content with the world")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.uploading:
            st.warning("⏳ Upload in progress...")
        
        with st.form("upload_video_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Video Title*", placeholder="Enter an engaging title")
                category = st.selectbox("Category*", settings.VIDEO_CATEGORIES)
                channel_options = {ch['channel_name']: str(ch['_id']) for ch in my_channels}
                selected_channel = st.selectbox("Channel*", list(channel_options.keys()))
            
            with col2:
                tags = st.text_input("Tags", placeholder="tutorial, education, tech")
                visibility = st.selectbox("Visibility", ["Public", "Unlisted", "Private"])
            
            description = st.text_area("Description", placeholder="Describe your video...")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                video_file = st.file_uploader("Upload Video*", type=['mp4', 'mov', 'avi', 'mkv', 'webm'])
                if video_file:
                    st.success(f"✅ {video_file.name}")
                    st.caption(f"Size: {video_file.size / (1024*1024):.2f} MB")
            
            with col2:
                thumbnail_file = st.file_uploader("Thumbnail", type=['jpg', 'jpeg', 'png', 'webp'])
                if thumbnail_file:
                    st.image(thumbnail_file, use_column_width=True)
                else:
                    # Preview placeholder when no thumbnail uploaded
                    st.markdown("""
                    <div class="upload-placeholder">
                        <div class="placeholder-emoji">📸</div>
                        <div class="placeholder-title">Optional Thumbnail</div>
                        <div class="placeholder-subtitle">Make your video stand out!</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                submit = st.form_submit_button("🚀 Upload", use_container_width=True, 
                                              type="primary", disabled=st.session_state.uploading)
            
            if submit:
                if st.session_state.uploading:
                    st.warning("⏳ Upload already in progress! Please wait...")
                    st.stop()
                
                if not title or not video_file:
                    st.error("❌ Title and video file are required!")
                    st.stop()
                
                valid, msg = Validators.validate_video_title(title)
                if not valid:
                    st.error(msg)
                    st.stop()
                
                database = db.get_db()
                existing_video = database.videos.find_one({
                    'title': title,
                    'creator_id': str(user['_id'])
                })
                
                if existing_video:
                    st.error(f"❌ You already have a video with the title: '{title}'")
                    st.warning("💡 Please use a different title or delete the existing video first.")
                    st.stop()
                
                video_file.seek(0)
                file_hash = hashlib.md5(video_file.read()).hexdigest()
                video_file.seek(0)
                
                existing_file = database.videos.find_one({
                    'creator_id': str(user['_id']),
                    'file_hash': file_hash
                })
                
                if existing_file:
                    st.error(f"❌ This video file was already uploaded!")
                    st.info(f"🎹 Existing video: '{existing_file.get('title', 'Untitled')}'")
                    st.warning("💡 You cannot upload the same video file twice.")
                    st.stop()
                
                st.session_state.uploading = True
                submission_id = hashlib.md5(f"{title}{user['_id']}{time.time()}".encode()).hexdigest()
                st.session_state.last_video_submission = submission_id
                
                with st.spinner("Uploading..."):
                    try:
                        import uuid
                        temp_id = str(uuid.uuid4())
                        
                        video_path = save_uploaded_file(video_file, temp_id)
                        thumbnail_path = None
                        if thumbnail_file:
                            thumbnail_path = save_uploaded_thumbnail(thumbnail_file, temp_id)
                        
                        tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
                        
                        video_data = {
                            'title': title,
                            'description': description,
                            'video_path': video_path,
                            'video_url': video_path,
                            'thumbnail_path': thumbnail_path,
                            'thumbnail': thumbnail_path or 'https://via.placeholder.com/640x360',
                            'category': category,
                            'tags': tags_list,
                            'visibility': visibility,
                            'channel_id': channel_options[selected_channel],
                            'creator_id': str(user['_id']),
                            'creator_name': user['username'],
                            'file_size': video_file.size,
                            'file_name': video_file.name,
                            'file_hash': file_hash
                        }
                        
                        video_model.create(video_data)
                        st.session_state.video_uploaded = True
                        st.success("✅ Uploaded!")
                        
                        # Reset state and rerun ONLY after successful upload
                        st.session_state.uploading = False
                        st.session_state.last_video_submission = None
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.session_state.uploading = False
                        st.session_state.last_video_submission = None