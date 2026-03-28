# ============================================================================
# FILE: pages/7_Playlists.py - PROFESSIONAL UI REDESIGN
# ============================================================================
import streamlit as st
from utils.auth import Auth
from models.playlist import PlaylistModel
from models.video import VideoModel
from utils.helpers import Helpers
import hashlib
import time

st.set_page_config(page_title="Playlists - MediaHub", page_icon="📋", layout="wide")

from utils.ui import sidebar_v2

with st.sidebar:
    sidebar_v2()

Auth.require_auth()

user = Auth.get_current_user()
playlist_model = PlaylistModel()
video_model = VideoModel()

# ======================================================================
# SESSION STATE INITIALIZATION
# ======================================================================
if 'last_playlist_submission' not in st.session_state:
    st.session_state.last_playlist_submission = None
if 'last_playlist_time' not in st.session_state:
    st.session_state.last_playlist_time = 0
if 'playlist_form_submitted' not in st.session_state:
    st.session_state.playlist_form_submitted = False
if 'current_playing_video' not in st.session_state:
    st.session_state.current_playing_video = None
if 'current_playlist' not in st.session_state:
    st.session_state.current_playlist = None
if 'player_mode' not in st.session_state:
    st.session_state.player_mode = False
if 'form_can_submit' not in st.session_state:
    st.session_state.form_can_submit = True

# Get user's videos
if user['role'] in ['Creator', 'Admin']:
    available_videos = video_model.get_by_creator(str(user['_id']))
else:
    available_videos = video_model.get_all()

# ======================================================================
# MAIN STYLING
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

/* Expander Styling */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #f7fafc, #edf2f7) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    font-weight: 600 !important;
    color: #2d3748 !important;
    border: 2px solid #e2e8f0 !important;
}

.streamlit-expanderHeader:hover {
    border-color: #667eea !important;
    background: linear-gradient(135deg, #edf2f7, #e2e8f0) !important;
}

.streamlit-expanderContent {
    background: white !important;
    border: 2px solid #e2e8f0 !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 20px !important;
}

/* Text Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stMultiSelect > div > div > div {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    background: #f8fafc !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    background: white !important;
}

.stTextInput > label,
.stTextArea > label,
.stSelectbox > label,
.stMultiSelect > label,
.stCheckbox > label {
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

/* Cards */
.playlist-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.playlist-card:hover {
    border-color: #667eea;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
    transform: translateY(-4px);
}

/* Video Item Cards */
.video-item-card {
    background: #f8fafc;
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
}

.video-item-card:hover {
    background: white;
    border-color: #667eea;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
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

/* Info/Warning/Success/Error boxes */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 12px !important;
    padding: 16px 20px !important;
    margin: 12px 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* Video Player Section */
.video-player-section {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    margin: 20px 0;
}

.video-stats-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(102, 126, 234, 0.3);
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

/* Image styling */
img {
    border-radius: 8px;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(135deg, #667eea, #764ba2);
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

# ======================================================================
# PAGE HEADER
# ======================================================================
st.markdown("""
<div class="page-header">
    <h1 class="page-title">📋 Playlist Hub</h1>
    <p class="page-subtitle">Create, organize, and enjoy your video collections</p>
</div>
""", unsafe_allow_html=True)

# ======================================================================
# HELPER FUNCTION: VIDEO PLAYER
# ======================================================================
def display_video_player(video, playlist_id=None, context="default"):
    """Display video player with full statistics"""
    st.markdown('<div class="video-player-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### 🎬 {video['title']}")
        
        # Video display
        if video.get('video_url'):
            st.video(video['video_url'])
        elif video.get('video_file'):
            st.video(video['video_file'])
        else:
            st.info("Video source not available")
        
        # Video description
        with st.expander("📝 Description", expanded=True):
            st.write(video.get('description', 'No description available'))
        
        # Tags
        if video.get('tags'):
            st.markdown("**🏷️ Tags:**")
            tags_html = " ".join([
                f'<span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 4px 12px; border-radius: 16px; font-size: 12px; margin-right: 8px; display: inline-block;">{tag}</span>'
                for tag in video['tags']
            ])
            st.markdown(tags_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Statistics")
        
        # Views
        st.markdown('<div class="video-stats-card">', unsafe_allow_html=True)
        st.metric("👁️ Views", Helpers.format_number(video.get('views', 0)))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Likes
        st.markdown('<div class="video-stats-card">', unsafe_allow_html=True)
        st.metric("👍 Likes", Helpers.format_number(video.get('likes', 0)))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Comments
        st.markdown('<div class="video-stats-card">', unsafe_allow_html=True)
        st.metric("💬 Comments", video.get('comment_count', 0))
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### ℹ️ Details")
        st.caption(f"**Category:** {video.get('category', 'N/A')}")
        st.caption(f"**Creator:** {video.get('creator_name', 'Unknown')}")
        st.caption(f"**Status:** {video.get('status', 'N/A')}")
        
        if video.get('created_at'):
            st.caption(f"**Uploaded:** {video['created_at'].strftime('%b %d, %Y')}")
        
        # Like ratio
        total_interactions = video.get('likes', 0) + video.get('dislikes', 0)
        if total_interactions > 0:
            like_ratio = (video.get('likes', 0) / total_interactions) * 100
            st.progress(like_ratio / 100)
            st.caption(f"Like Ratio: {like_ratio:.1f}%")
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("⬅️ Back to Playlist", key=f"back_player_{context}_{video['_id']}", use_container_width=True):
            st.session_state.current_playing_video = None
            st.session_state.current_playlist = None
            st.session_state.player_mode = False
            st.rerun()
    
    with col2:
        if playlist_id:
            playlist = playlist_model.get_by_id(playlist_id)
            if playlist:
                video_ids = playlist.get('video_ids', [])
                current_idx = video_ids.index(str(video['_id'])) if str(video['_id']) in video_ids else -1
                
                if current_idx < len(video_ids) - 1:
                    if st.button("▶️ Next Video", key=f"next_player_{context}_{video['_id']}", use_container_width=True):
                        st.session_state.current_playing_video = video_ids[current_idx + 1]
                        st.session_state.player_mode = True
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================================
# TABS
# ======================================================================
tab1, tab2, tab3 = st.tabs(["📋 My Playlists", "🌐 Browse Playlists", "➕ Create Playlist"])

# ======================================================================
# TAB 1: MY PLAYLISTS
# ======================================================================
with tab1:
    st.markdown("### 📋 My Playlists")
    
    my_playlists = playlist_model.get_by_creator(str(user['_id']))
    
    # Check if playing video
    if st.session_state.player_mode and st.session_state.current_playing_video:
        video = video_model.get_by_id(st.session_state.current_playing_video)
        if video:
            display_video_player(video, st.session_state.current_playlist, context="my_playlists")
        else:
            st.error("Video not found")
            st.session_state.player_mode = False
            st.session_state.current_playing_video = None
    elif my_playlists:
        for playlist in my_playlists:
            with st.expander(f"📋 {playlist['name']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Description:** {playlist.get('description', 'No description')}")
                    visibility = "🌐 Public" if playlist.get('is_public', True) else "🔒 Private"
                    st.caption(visibility)
                    st.caption(f"📅 Created: {Helpers.time_ago(playlist.get('created_at'))}")
                
                with col2:
                    video_count = len(playlist.get('video_ids', []))
                    st.metric("Videos", video_count)
                
                st.markdown("---")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if playlist.get('video_ids'):
                        if st.button("▶️ Play All", key=f"play_all_{playlist['_id']}", use_container_width=True, type="primary"):
                            st.session_state.current_playing_video = playlist['video_ids'][0]
                            st.session_state.current_playlist = str(playlist['_id'])
                            st.session_state.player_mode = True
                            st.rerun()
                
                with col2:
                    if st.button("➕ Add Videos", key=f"add_{playlist['_id']}", use_container_width=True):
                        st.session_state[f'adding_to_{playlist["_id"]}'] = not st.session_state.get(f'adding_to_{playlist["_id"]}', False)
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_{playlist['_id']}", use_container_width=True):
                        st.session_state[f'editing_{playlist["_id"]}'] = not st.session_state.get(f'editing_{playlist["_id"]}', False)
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_{playlist['_id']}", use_container_width=True, type="secondary"):
                        playlist_model.delete(str(playlist['_id']))
                        st.success("Playlist deleted!")
                        time.sleep(1)
                        st.rerun()
                
                # Edit form
                if st.session_state.get(f'editing_{playlist["_id"]}', False):
                    st.markdown("---")
                    with st.form(f"edit_form_{playlist['_id']}"):
                        new_name = st.text_input("Playlist Name", value=playlist['name'])
                        new_desc = st.text_area("Description", value=playlist.get('description', ''))
                        new_public = st.checkbox("🌐 Public playlist", value=playlist.get('is_public', True))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                playlist_model.update(str(playlist['_id']), {
                                    'name': new_name,
                                    'description': new_desc,
                                    'is_public': new_public
                                })
                                st.session_state[f'editing_{playlist["_id"]}'] = False
                                st.success("Playlist updated!")
                                time.sleep(1)
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel", use_container_width=True):
                                st.session_state[f'editing_{playlist["_id"]}'] = False
                                st.rerun()
                
                # Display videos
                video_ids = playlist.get('video_ids', [])
                
                if video_ids:
                    st.markdown("#### 🎬 Videos in Playlist")
                    
                    for idx, video_id in enumerate(video_ids):
                        video = video_model.get_by_id(video_id)
                        if video:
                            st.markdown('<div class="video-item-card">', unsafe_allow_html=True)
                            
                            col1, col2, col3, col4, col5, col6 = st.columns([0.5, 1.5, 3, 1, 1, 1])
                            
                            with col1:
                                st.markdown(f"**#{idx + 1}**")
                            
                            with col2:
                                if video.get('thumbnail'):
                                    st.image(video['thumbnail'], use_column_width=True)
                                else:
                                    st.image('https://via.placeholder.com/150x100?text=Video', use_column_width=True)
                            
                            with col3:
                                st.markdown(f"**{video['title']}**")
                                st.caption(f"👁️ {Helpers.format_number(video.get('views', 0))} views • 👍 {Helpers.format_number(video.get('likes', 0))} likes")
                            
                            with col4:
                                if st.button("▶️", key=f"play_{playlist['_id']}_{idx}", use_container_width=True):
                                    st.session_state.current_playing_video = video_id
                                    st.session_state.current_playlist = str(playlist['_id'])
                                    st.session_state.player_mode = True
                                    st.rerun()
                            
                            with col5:
                                if idx > 0:
                                    if st.button("⬆️", key=f"up_{playlist['_id']}_{idx}", use_container_width=True):
                                        new_order = video_ids.copy()
                                        new_order[idx], new_order[idx-1] = new_order[idx-1], new_order[idx]
                                        playlist_model.reorder_videos(str(playlist['_id']), new_order)
                                        st.rerun()
                                if idx < len(video_ids) - 1:
                                    if st.button("⬇️", key=f"down_{playlist['_id']}_{idx}", use_container_width=True):
                                        new_order = video_ids.copy()
                                        new_order[idx], new_order[idx+1] = new_order[idx+1], new_order[idx]
                                        playlist_model.reorder_videos(str(playlist['_id']), new_order)
                                        st.rerun()
                            
                            with col6:
                                if st.button("❌", key=f"remove_{playlist['_id']}_{video_id}", use_container_width=True):
                                    playlist_model.remove_video(str(playlist['_id']), video_id)
                                    st.success("Removed!")
                                    st.rerun()
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("📢 No videos in this playlist. Click '➕ Add Videos' to add some!")
                
                # Add videos section
                if st.session_state.get(f'adding_to_{playlist["_id"]}', False):
                    st.markdown("---")
                    st.markdown("#### ➕ Add Videos to Playlist")
                    
                    available_for_add = [v for v in available_videos if str(v['_id']) not in video_ids]
                    
                    if available_for_add:
                        search_query = st.text_input("🔍 Search videos", key=f"search_{playlist['_id']}")
                        
                        if search_query:
                            available_for_add = [
                                v for v in available_for_add 
                                if search_query.lower() in v['title'].lower()
                            ]
                        
                        st.caption(f"Showing {min(len(available_for_add), 10)} of {len(available_for_add)} videos")
                        
                        for video in available_for_add[:10]:
                            col1, col2, col3 = st.columns([1, 4, 1])
                            
                            with col1:
                                st.image(video.get('thumbnail', 'https://via.placeholder.com/100'), use_column_width=True)
                            
                            with col2:
                                st.markdown(f"**{video['title']}**")
                                st.caption(f"👁️ {Helpers.format_number(video.get('views', 0))} views • {video.get('category', 'N/A')}")
                            
                            with col3:
                                if st.button("Add", key=f"add_vid_{playlist['_id']}_{video['_id']}", use_container_width=True):
                                    playlist_model.add_video(str(playlist['_id']), str(video['_id']))
                                    st.success("Added!")
                                    st.rerun()
                        
                        if len(available_for_add) > 10:
                            st.info(f"Showing 10 of {len(available_for_add)} videos. Use search to find more.")
                    else:
                        st.info("All available videos are already in this playlist!")
                    
                    if st.button("✅ Done", key=f"done_{playlist['_id']}", use_container_width=True):
                        st.session_state[f'adding_to_{playlist["_id"]}'] = False
                        st.rerun()
    else:
        st.info("📢 You haven't created any playlists yet. Create one in the 'Create Playlist' tab!")

# ======================================================================
# TAB 2: BROWSE PLAYLISTS
# ======================================================================
with tab2:
    st.markdown("### 🌐 Browse Public Playlists")
    
    if st.session_state.player_mode and st.session_state.current_playing_video:
        video = video_model.get_by_id(st.session_state.current_playing_video)
        if video:
            display_video_player(video, st.session_state.current_playlist, context="browse")
        else:
            st.error("Video not found")
            st.session_state.player_mode = False
    else:
        all_playlists = playlist_model.get_all()
        public_playlists = [p for p in all_playlists if p.get('is_public', True)]
        
        if public_playlists:
            cols = st.columns(3)
            for idx, playlist in enumerate(public_playlists):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="playlist-card">
                        <h3 style="margin: 0 0 8px 0; color: #1a202c;">📋 {playlist['name']}</h3>
                        <p style="color: #718096; font-size: 14px; margin-bottom: 12px;">{playlist.get('description', 'No description')[:100]}</p>
                        <p style="color: #4a5568; font-size: 12px;">by {playlist.get('creator_name', 'Unknown')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    video_count = len(playlist.get('video_ids', []))
                    st.metric("🎬 Videos", video_count)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if playlist.get('video_ids'):
                            if st.button("▶️ Play", key=f"play_pub_{playlist['_id']}", use_container_width=True, type="primary"):
                                st.session_state.current_playing_video = playlist['video_ids'][0]
                                st.session_state.current_playlist = str(playlist['_id'])
                                st.session_state.player_mode = True
                                st.rerun()
                    
                    with col2:
                        if st.button("👁️ View", key=f"view_{playlist['_id']}", use_container_width=True):
                            st.session_state[f'viewing_{playlist["_id"]}'] = not st.session_state.get(f'viewing_{playlist["_id"]}', False)
                            st.rerun()
                    
                    st.markdown("---")
            
            # Show expanded playlist details
            for playlist in public_playlists:
                if st.session_state.get(f'viewing_{playlist["_id"]}', False):
                    st.markdown("---")
                    st.markdown(f"### 📋 {playlist['name']}")
                    st.caption(f"by {playlist.get('creator_name', 'Unknown')}")
                    
                    video_ids = playlist.get('video_ids', [])
                    
                    if video_ids:
                        st.markdown(f"#### 🎬 {len(video_ids)} Videos")
                        
                        for idx, video_id in enumerate(video_ids):
                            video = video_model.get_by_id(video_id)
                            if video:
                                st.markdown('<div class="video-item-card">', unsafe_allow_html=True)
                                
                                col1, col2, col3, col4 = st.columns([0.5, 1.5, 4, 1])
                                
                                with col1:
                                    st.markdown(f"**#{idx + 1}**")
                                
                                with col2:
                                    st.image(video.get('thumbnail', 'https://via.placeholder.com/150x100'), use_column_width=True)
                                
                                with col3:
                                    st.markdown(f"**{video['title']}**")
                                    st.caption(f"👁️ {Helpers.format_number(video.get('views', 0))} views • 👍 {Helpers.format_number(video.get('likes', 0))} likes")
                                
                                with col4:
                                    if st.button("▶️ Play", key=f"play_pub_vid_{playlist['_id']}_{idx}", use_container_width=True):
                                        st.session_state.current_playing_video = video_id
                                        st.session_state.current_playlist = str(playlist['_id'])
                                        st.session_state.player_mode = True
                                        st.rerun()
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("This playlist is empty")
                    
                    if st.button("⬅️ Back to Browse", key=f"back_{playlist['_id']}", use_container_width=True):
                        st.session_state[f'viewing_{playlist["_id"]}'] = False
                        st.rerun()
        else:
            st.info("📢 No public playlists available yet")

# ======================================================================
# TAB 3: CREATE PLAYLIST
# ======================================================================
with tab3:
    st.markdown("### ➕ Create New Playlist")
    
    with st.form("create_playlist_form", clear_on_submit=True):
        st.markdown("#### 📋 Playlist Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("📋 Playlist Name*", placeholder="e.g., My Favorite Videos")
        
        with col2:
            is_public = st.checkbox("🌍 Make playlist public", value=True)
        
        description = st.text_area(
            "📝 Description", 
            placeholder="What's this playlist about?",
            height=100
        )
        
        st.markdown("---")
        
        st.markdown("#### 🎬 Add Videos (Optional)")
        st.caption("💡 You can also add videos later from the 'My Playlists' tab")
        
        selected_videos = []
        if available_videos:
            selected_videos = st.multiselect(
                "Select videos to add",
                options=[str(v['_id']) for v in available_videos],
                format_func=lambda x: next((v['title'] for v in available_videos if str(v['_id']) == x), x),
                help="Hold Ctrl/Cmd to select multiple videos"
            )
            
            if selected_videos:
                st.success(f"✅ {len(selected_videos)} video(s) selected")
        else:
            st.warning("⚠️ No videos available. Upload some videos first!")
        
        st.markdown("---")
        
        submit = st.form_submit_button(
            "🚀 Create Playlist", 
            use_container_width=True, 
            type="primary",
            disabled=not st.session_state.form_can_submit
        )
    
    # PROCESS SUBMISSION OUTSIDE THE FORM
    if submit and st.session_state.form_can_submit:
        if not name:
            st.error("❌ Playlist name is required")
        else:
            normalized_name = name.strip()
            if not normalized_name:
                st.error("❌ Playlist name cannot be only spaces")
            else:
                # DISABLE FORM IMMEDIATELY to prevent double-clicks
                st.session_state.form_can_submit = False
                
                # UNIQUE HASH FOR THIS SUBMISSION (based on name + user only)
                submission_hash = hashlib.md5(
                    f"{normalized_name.lower()}_{user['_id']}".encode()
                ).hexdigest()
                
                current_time = time.time()
                last_hash = st.session_state.last_playlist_submission
                last_time = st.session_state.last_playlist_time
                time_diff = current_time - last_time
                
                # Only submit if it's a DIFFERENT playlist OR more than 2 seconds have passed
                if last_hash != submission_hash or time_diff > 2.0:
                    try:
                        st.session_state.last_playlist_submission = submission_hash
                        st.session_state.last_playlist_time = current_time
                        
                        video_ids_to_add = [str(vid) for vid in selected_videos] if selected_videos else []
                        
                        playlist_data = {
                            'name': normalized_name,
                            'description': description,
                            'creator_id': str(user['_id']),
                            'creator_name': user['username'],
                            'is_public': is_public,
                            'video_ids': video_ids_to_add
                        }
                        
                        playlist_id = playlist_model.create(playlist_data)
                        
                        st.success(f"✅ Playlist '{normalized_name}' created successfully!")
                        if video_ids_to_add:
                            st.success(f"✅ Added {len(video_ids_to_add)} video(s) to playlist")
                        st.balloons()
                        
                        st.session_state.form_can_submit = True
                        
                        time.sleep(1.5)
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Error creating playlist: {e}")
                        st.session_state.form_can_submit = True
                        st.session_state.last_playlist_submission = None
                else:
                    st.warning("⏳ Playlist already created! Redirecting...")
                    st.session_state.form_can_submit = True
                    time.sleep(1)
                    st.rerun()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f6f8fb 0%, #e9ecef 100%); 
                border-radius: 16px; padding: 20px; margin-top: 24px; 
                border-left: 4px solid #667eea;">
        <h4 style="color: #2d3748; margin: 0 0 12px 0; font-size: 16px;">💡 Playlist Tips</h4>
        <ul style="margin: 0; padding-left: 20px; color: #4a5568; font-size: 14px; line-height: 1.8;">
            <li>Give your playlist a descriptive and catchy name</li>
            <li>Add a clear description to help others understand the theme</li>
            <li>Organize videos in a logical order for the best viewing experience</li>
            <li>Make it public to share with the community or keep it private</li>
            <li>You can reorder videos anytime by using the ⬆️ and ⬇️ buttons</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ======================================================================
# SIDEBAR STATISTICS
# ======================================================================
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Your Playlist Stats")
    
    my_playlists = playlist_model.get_by_creator(str(user['_id']))
    my_playlists_count = len(my_playlists)
    total_videos_in_playlists = sum(len(p.get('video_ids', [])) for p in my_playlists)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📋 Playlists", my_playlists_count)
    
    with col2:
        st.metric("🎬 Videos", total_videos_in_playlists)
    
    if my_playlists_count > 0:
        avg_videos = total_videos_in_playlists / my_playlists_count
        st.metric("📈 Avg Videos/Playlist", f"{avg_videos:.1f}")
    
    public_count = sum(1 for p in my_playlists if p.get('is_public', True))
    private_count = my_playlists_count - public_count
    
    st.markdown("---")
    st.markdown("#### 🔒 Privacy")
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"🌐 Public: {public_count}")
    with col2:
        st.caption(f"🔒 Private: {private_count}")
