import streamlit as st
from utils.auth import Auth
from models.comment import CommentModel
from models.video import VideoModel
from utils.helpers import Helpers
import hashlib
import time

st.set_page_config(page_title="Comment System", page_icon="💬", layout="wide")

from utils.ui import sidebar_v2

with st.sidebar:
    sidebar_v2()

Auth.require_auth()

# ======================================================================
# STYLING - AGGRESSIVE WHITE PLACEHOLDER REMOVAL
# ======================================================================
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

.main-content {
    background: rgba(255, 255, 255, 0.98);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    margin-bottom: 20px;
}

.stVerticalBlock {
    gap: 0rem !important;
}

.stVerticalBlockBorderWrapper {
    padding: 0 !important;
    margin: 0 !important;
}

.element-container {
    margin: 0 !important;
    padding: 0 !important;
}

.element-container:empty {
    display: none !important;
    height: 0 !important;
}

.stMarkdown:empty,
.stMarkdown > div:empty,
.stMarkdown > div > div:empty {
    display: none !important;
    height: 0 !important;
}

div[data-testid="stVerticalBlock"] > div:empty {
    display: none !important;
}

.stMarkdown {
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stVerticalBlock"] > div[style*="background"] {
    background: transparent !important;
    padding: 0 !important;
}

.row-widget {
    margin: 0 !important;
    padding: 0 !important;
}

h3, .main-content h3 {
    color: #1a202c !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    margin-top: 0 !important;
    font-size: 24px !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    background: white !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

.stTextInput > label,
.stTextArea > label,
.stSelectbox > label {
    font-weight: 600 !important;
    color: #2d3748 !important;
    font-size: 14px !important;
    margin-bottom: 8px !important;
}

.stSelectbox [data-baseweb="select"] {
    background: white !important;
}

.stSelectbox [data-baseweb="select"] > div {
    background: white !important;
    border-radius: 12px !important;
}

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

.stForm .stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.video-display-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0 16px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 2px solid #e2e8f0;
}

.video-title-main {
    font-size: 28px;
    font-weight: 700;
    color: #1a202c;
    margin-bottom: 8px;
}

.video-creator {
    color: #667eea;
    font-weight: 600;
    font-size: 14px;
}

.video-stats {
    color: #718096;
    font-size: 14px;
    margin-top: 8px;
}

/* EXTENDED COMMENT CARDS */
.comment-box {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.comment-box:hover {
    border-color: #667eea;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
    transform: translateY(-4px);
}

/* EXTENDED REPLY CARDS */
.reply-box {
    background: linear-gradient(to right, #f0f4ff, white);
    border-left: 4px solid #667eea;
    padding: 20px;
    margin: 16px 0 16px 2rem !important;
    border-radius: 16px;
    border: 2px solid #d6e4ff;
    box-shadow: 0 2px 12px rgba(102, 126, 234, 0.1);
    transition: all 0.3s ease;
    min-height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.reply-box:hover {
    border-color: #667eea;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    transform: translateX(8px);
}

.comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 2px solid #e2e8f0;
}

.comment-user-info {
    display: flex;
    align-items: center;
    gap: 8px;
}

.comment-stats {
    display: flex;
    align-items: center;
    gap: 12px;
}

.comment-section-header {
    background: linear-gradient(135deg, #f7fafc, #edf2f7);
    border-radius: 12px;
    padding: 14px 18px;
    margin: 12px 0 8px 0;
    border-left: 4px solid #667eea;
}

.comment-author {
    font-weight: 600;
    color: #667eea;
    font-size: 15px;
}

.comment-time {
    color: #a0aec0;
    font-size: 13px;
}

.comment-text {
    color: #2d3748;
    font-size: 15px;
    line-height: 1.6;
    margin: 6px 0;
}

.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin: 6px 0 !important;
    font-size: 14px !important;
}

.stForm {
    background: #f8fafc;
    padding: 16px;
    border-radius: 16px;
    border: 2px solid #e2e8f0;
    margin: 6px 0;
}

.stImage {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

hr {
    margin: 10px 0 !important;
    border: none;
    border-top: 2px solid #e2e8f0;
}

.block-container {
    padding: 2rem 1rem !important;
    max-width: 1400px !important;
}

.empty-state {
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin: 1rem 0;
    border: 2px solid #e2e8f0;
}

.empty-state-icon {
    font-size: 3rem;
    margin-bottom: 0.8rem;
}

div[data-testid="column"] {
    padding: 0 6px;
}

@media (max-width: 768px) {
    .page-header { padding: 20px; }
    .page-title { font-size: 28px; }
    .main-content { padding: 20px; }
    .reply-box { margin-left: 1rem !important; }
    .comment-box, .reply-box { min-height: 120px; }
}
</style>
""", unsafe_allow_html=True)

# ======================================================================
# INITIALIZE SESSION STATE
# ======================================================================
if 'last_comment_submission' not in st.session_state:
    st.session_state.last_comment_submission = {}

if 'action_processed' not in st.session_state:
    st.session_state.action_processed = False

if 'last_like_time' not in st.session_state:
    st.session_state.last_like_time = {}

# ======================================================================
# PAGE HEADER
# ======================================================================
st.markdown("""
<div class="page-header">
    <h1 class="page-title">💬 Comment System</h1>
    <p class="page-subtitle">Engage with videos through comments and discussions</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)

user = Auth.get_current_user()
comment_model = CommentModel()
video_model = VideoModel()

if 'comment_posted' in st.session_state and st.session_state.comment_posted:
    st.success("✅ Comment posted!")
    st.session_state.comment_posted = False

# Display comment function - DEBOUNCED LIKE SYSTEM
def display_comment(comment, level=0):
    """Display comment with replies"""
    comment_id_str = str(comment['_id'])
    box_class = "reply-box" if level > 0 else "comment-box"
    user_id = str(user['_id'])
    
    # Check if user has liked
    liked_by = comment.get('liked_by', [])
    is_liked = user_id in liked_by
    like_emoji = "❤️" if is_liked else "🤍"
    
    # Display comment with enhanced structure
    comment_html = f'<div class="{box_class}">'
    comment_html += '<div class="comment-header">'
    comment_html += '<div class="comment-user-info">'
    comment_html += f'<span class="comment-author">👤 {comment["username"]}</span>'
    comment_html += f'<span class="comment-time">• {Helpers.time_ago(comment["created_at"])}</span>'
    if comment.get('is_edited'):
        comment_html += '<span style="color: #718096; font-size: 12px;">✏️ (edited)</span>'
    comment_html += '</div>'
    comment_html += '<div class="comment-stats">'
    comment_html += f'<span style="color: #718096; font-size: 14px; font-weight: 600;">👍 {comment.get("likes", 0)}</span>'
    comment_html += '</div>'
    comment_html += '</div>'
    comment_html += f'<div class="comment-text">{comment["text"]}</div>'
    comment_html += '</div>'
    
    st.markdown(comment_html, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
    
    with col1:
        # DEBOUNCED LIKE BUTTON
        like_key = f"like_{comment_id_str}_{level}"
        current_time = time.time()
        last_time = st.session_state.last_like_time.get(like_key, 0)
        
        # Only process if 1 second has passed since last click
        if st.button(like_emoji, key=like_key):
            if current_time - last_time > 1.0:  # 1 second debounce
                st.session_state.last_like_time[like_key] = current_time
                result = comment_model.like(comment_id_str, user_id)
                if result:
                    time.sleep(0.2)  # Small delay to ensure DB update
                    st.rerun()
    
    with col2:
        if level < 2:
            if st.button("💬", key=f"reply_{comment_id_str}_{level}"):
                st.session_state[f'replying_to_{comment_id_str}'] = not st.session_state.get(f'replying_to_{comment_id_str}', False)
                st.rerun()
    
    with col3:
        if str(comment['user_id']) == user_id or user.get('role') == 'Admin':
            if st.button("✏️", key=f"edit_{comment_id_str}_{level}"):
                st.session_state[f'editing_{comment_id_str}'] = not st.session_state.get(f'editing_{comment_id_str}', False)
                st.rerun()
    
    with col4:
        if str(comment['user_id']) == user_id or user.get('role') == 'Admin':
            if st.button("🗑️", key=f"delete_{comment_id_str}_{level}"):
                comment_model.delete(comment_id_str)
                st.success("Deleted!")
                time.sleep(0.3)
                st.rerun()
    
    # Reply form
    if st.session_state.get(f'replying_to_{comment_id_str}', False):
        with st.form(f"reply_form_{comment_id_str}", clear_on_submit=True):
            reply_text = st.text_area("Reply", key=f"reply_text_{comment_id_str}", placeholder="Write your reply...")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("📤 Post Reply", use_container_width=True):
                    if reply_text and reply_text.strip():
                        reply_data = {
                            'video_id': comment['video_id'],
                            'user_id': user_id,
                            'username': user['username'],
                            'text': reply_text.strip(),
                            'parent_id': comment_id_str
                        }
                        comment_model.create(reply_data)
                        st.session_state[f'replying_to_{comment_id_str}'] = False
                        st.success("Reply posted!")
                        time.sleep(0.3)
                        st.rerun()
                    else:
                        st.error("❌ Reply cannot be empty")
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state[f'replying_to_{comment_id_str}'] = False
                    st.rerun()
    
    # Edit form
    if st.session_state.get(f'editing_{comment_id_str}', False):
        with st.form(f"edit_form_{comment_id_str}"):
            new_text = st.text_area("Edit", value=comment['text'], key=f"edit_text_{comment_id_str}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Save", use_container_width=True):
                    if new_text and new_text.strip():
                        comment_model.update(comment_id_str, new_text.strip())
                        st.session_state[f'editing_{comment_id_str}'] = False
                        st.success("Updated!")
                        time.sleep(0.3)
                        st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state[f'editing_{comment_id_str}'] = False
                    st.rerun()
    
    # Display replies
    if level < 3:
        replies = comment_model.get_replies(comment_id_str)
        if replies:
            for reply in replies:
                display_comment(reply, level + 1)

# ======================================================================
# MAIN CONTENT
# ======================================================================
videos = video_model.get_all()

if not videos:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🎬</div>
        <h2 style="color: #2d3748;">No Videos Available</h2>
        <p style="color: #718096;">Upload some videos first to start commenting!</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

st.markdown("### 🎬 Select Video")
video_options = {f"{v['title']} (by {v['creator_name']})": str(v['_id']) for v in videos}
selected_video_display = st.selectbox("Choose a video to view comments", list(video_options.keys()))
selected_video_id = video_options[selected_video_display]

video = video_model.get_by_id(selected_video_id)

if video:
    st.markdown('<div class="video-display-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(video.get('thumbnail', 'https://via.placeholder.com/300x200'), use_column_width=True)
    
    with col2:
        st.markdown(f'<div class="video-title-main">{video["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="video-creator">by {video["creator_name"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="video-stats">👁️ {Helpers.format_number(video.get("views", 0))} views • 👍 {Helpers.format_number(video.get("likes", 0))} likes</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
# Replace the "Add comment" section (around line 380) with this:

# Replace the entire "Add comment" and "Display comments" section with this:

# Add comment
st.markdown("### 💬 Add a Comment")

with st.form("add_comment_form", clear_on_submit=True):
    comment_text = st.text_area("Your Comment", placeholder="Share your thoughts...", height=100)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        submit = st.form_submit_button("📤 Post", use_container_width=True, type="primary")

# Process submission OUTSIDE the form
if submit:
    if comment_text and comment_text.strip():
        # CREATE UNIQUE HASH FOR THIS SUBMISSION
        submission_hash = hashlib.md5(
            f"{selected_video_id}_{user['_id']}_{comment_text.strip()}_{int(time.time())}".encode()
        ).hexdigest()
        
        # CHECK IF THIS EXACT COMMENT WAS JUST SUBMITTED
        last_hash = st.session_state.last_comment_submission.get('hash')
        last_time = st.session_state.last_comment_submission.get('time', 0)
        current_time = time.time()
        
        # Only submit if: different content OR more than 2 seconds have passed
        if last_hash != submission_hash or (current_time - last_time) > 2.0:
            comment_data = {
                'video_id': selected_video_id,
                'user_id': str(user['_id']),
                'username': user['username'],
                'text': comment_text.strip(),
                'parent_id': None
            }
            
            try:
                comment_model.create(comment_data)
                
                # STORE THIS SUBMISSION TO PREVENT DUPLICATES
                st.session_state.last_comment_submission = {
                    'hash': submission_hash,
                    'time': current_time
                }
                
                st.success("✅ Comment posted!")
                time.sleep(0.5)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("⏳ Please wait before submitting again")
    else:
        st.error("❌ Comment cannot be empty")

st.markdown("---")

# Display comments
st.markdown('<div class="comment-section-header">', unsafe_allow_html=True)
st.markdown("### 💬 Comments")
st.markdown('</div>', unsafe_allow_html=True)

comments = comment_model.get_by_video(selected_video_id)

if comments:
    top_level_comments = [c for c in comments if not c.get('parent_id')]
    st.caption(f"📊 {len(comments)} total comment(s) • {len(top_level_comments)} top-level")
    
    for comment in top_level_comments:
        display_comment(comment, level=0)
else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">💭</div>
        <h3 style="color: #2d3748;">No comments yet</h3>
        <p style="color: #718096;">Be the first to share your thoughts!</p>
    </div>
    """, unsafe_allow_html=True)