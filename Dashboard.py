# app.py - Professional MediaHub Dashboard with Clean UI (Optimized)
import streamlit as st
from config.database import db
from config.settings import settings
from utils.auth import Auth
from models.user import UserModel
import plotly.graph_objects as go
from datetime import datetime

# Professional Page Configuration
st.set_page_config(
    page_title=f"Media Management System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Optimized with Proper Whitespace
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main App Background - Match Channel Page */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Improved Container Padding */
    .block-container {
        padding: 1.5rem 2rem !important;
        max-width: 1400px !important;
    }
    
    /* Better Element Spacing */
    .element-container {
        margin-bottom: 0.75rem !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 1rem !important;
    }
    
    div[data-testid="column"] {
        padding: 0 0.5rem !important;
    }
    
    /* Page Header - Better Spacing */
    .page-header {
        background: rgba(255, 255, 255, 0.98);
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        text-align: center;
    }
    
    .page-title {
        font-size: 32px;
        font-weight: 700;
        color: #1a202c;
        margin: 0;
        line-height: 1.2;
    }
    
    .page-subtitle {
        font-size: 16px;
        color: #718096;
        margin: 8px 0 0 0;
        line-height: 1.4;
    }
    
    /* Improved Metric Cards with Better Spacing */
    .metric-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        padding: 20px 18px;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transition: all 0.3s ease;
        border: 2px solid #e2e8f0;
        margin: 0.5rem 0;
        height: 100%;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        border-color: #667eea;
        box-shadow: 0 10px 32px rgba(102, 126, 234, 0.25);
        transform: translateY(-4px);
    }
    
    /* Streamlit Metrics Override - CRITICAL FIX */
    [data-testid="stMetric"] {
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        color: #4a5568 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px !important;
        display: block !important;
        justify-content: center !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.3 !important;
        margin: 0 !important;
        display: block !important;
        text-align: center !important;
    }
    
    [data-testid="stMetricDelta"] {
        display: none !important;
    }
    
    /* Section Headers with Better Spacing */
    .section-header {
        background: rgba(255, 255, 255, 0.98);
        padding: 16px 24px;
        border-radius: 12px;
        margin: 1.5rem 0 1rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        border-left: 5px solid #667eea;
    }
    
    .section-header h2 {
        color: #1a202c !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        line-height: 1.3 !important;
    }
    
    /* Feature Cards - Better Spacing */
    .feature-card {
        background: rgba(255, 255, 255, 0.98);
        padding: 24px 20px;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid #e2e8f0;
        height: 100%;
        min-height: 180px;
        margin: 0.5rem 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .feature-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 28px rgba(102, 126, 234, 0.25);
        transform: translateY(-4px);
    }
    
    .feature-icon {
        font-size: 2.8rem;
        margin-bottom: 12px;
        line-height: 1;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1a202c;
        margin: 10px 0;
        line-height: 1.3;
    }
    
    .feature-desc {
        color: #4a5568;
        font-size: 0.9rem;
        line-height: 1.5;
        font-weight: 500;
        margin: 0;
        padding: 0 10px;
    }
    
    /* Video Cards - Better Spacing */
    .video-card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(0,0,0,0.12);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
        border: 2px solid #e2e8f0;
        height: 100%;
    }
    
    .video-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 28px rgba(102, 126, 234, 0.2);
        transform: translateY(-4px);
    }
    
    .video-card img {
        margin: 0 !important;
        padding: 0 !important;
        width: 100%;
        height: auto;
    }
    
    .video-title {
        font-weight: 700;
        color: #1a202c;
        font-size: 1rem;
        padding: 12px 16px 0 16px;
        margin: 0;
        line-height: 1.4;
        min-height: 50px;
    }
    
    .video-stats {
        color: #4a5568;
        font-size: 0.85rem;
        padding: 8px 16px 12px 16px;
        font-weight: 600;
        margin: 0;
    }
    
    /* Action Cards - Better Spacing */
    .action-card {
        background: rgba(255, 255, 255, 0.98);
        padding: 28px 24px;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid #e2e8f0;
        margin: 0.5rem 0;
        height: 100%;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .action-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 28px rgba(102, 126, 234, 0.25);
        transform: translateY(-4px);
    }
    
    /* Buttons */
    .action-card button {
        margin-top: 12px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .action-card button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }
    
    /* Activity Items - Better Spacing */
    .activity-item {
        background: rgba(255, 255, 255, 0.98);
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .activity-item:hover {
        box-shadow: 0 5px 18px rgba(102, 126, 234, 0.2);
        transform: translateX(6px);
    }
    
    .activity-item:last-child {
        margin-bottom: 0;
    }
    
    /* Info Boxes - Better Spacing */
    .info-box {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 16px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
        text-align: center;
        font-size: 1rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .info-box code {
        background: rgba(255,255,255,0.25);
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.95rem;
    }
    
    /* Empty State - Better Spacing */
    .empty-state {
        background: rgba(255, 255, 255, 0.98);
        padding: 40px 24px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        margin: 1rem 0;
    }
    
    .empty-icon {
        font-size: 3rem;
        margin-bottom: 16px;
        line-height: 1;
    }
    
    .empty-text {
        color: #1a202c;
        font-size: 1.1rem;
        font-weight: 600;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Plotly Charts Container */
    .js-plotly-plot {
        margin: 0.5rem 0 !important;
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 12px !important;
        padding: 10px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important;
    }
    
    /* Alert Boxes */
    .stAlert {
        padding: 12px 16px !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        margin: 1rem 0 !important;
    }
    
    /* Image Optimization */
    img {
        border-radius: 10px;
        display: block;
    }
    
    /* Add spacing between columns */
    div[data-testid="column"] > div {
        padding: 0.5rem;
    }
    
    /* Ensure proper spacing for all stMarkdown elements */
    .stMarkdown {
        margin-bottom: 0.5rem !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
        }
        
        .page-header {
            padding: 18px 20px;
        }
        
        .page-title {
            font-size: 24px;
        }
        
        .page-subtitle {
            font-size: 14px;
        }
        
        .metric-card, .feature-card, .action-card {
            padding: 16px;
            min-height: auto;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        .section-header {
            padding: 12px 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ======================================================================
# INITIALIZE SESSION & DB
# ======================================================================
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    try:
        st.session_state.db_connected = db.connect()
    except Exception:
        st.session_state.db_connected = False
    st.session_state.user = None

# Initialize default admin if DB available
if st.session_state.get("db_connected", False):
    try:
        database = db.get_db()
        if not database.users.find_one({"username": "admin"}):
            Auth.register("admin", "admin@system.com", "admin123", "Admin")
    except Exception:
        pass

# ======================================================================
# SIDEBAR
# ======================================================================
from utils.ui import sidebar_v2

with st.sidebar:
    sidebar_v2()

# ======================================================================
# HELPER FUNCTIONS
# ======================================================================
def display_recent_videos():
    """Display recent videos in compact card layout"""
    from models.video import VideoModel
    from utils.helpers import Helpers

    video_model = VideoModel()
    videos = video_model.get_all(limit=6)

    if videos:
        cols = st.columns(3)
        for idx, video in enumerate(videos):
            with cols[idx % 3]:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.image(video.get('thumbnail', 'https://via.placeholder.com/300x200'))
                st.markdown(f'<div class="video-title">{video["title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="video-stats">👁️ {Helpers.format_number(video.get("views", 0))} views • 📅 {Helpers.time_ago(video.get("created_at"))}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🔭</div>
            <div class="empty-text">No videos available yet. Be the first to upload!</div>
        </div>
        """, unsafe_allow_html=True)

def display_public_home():
    """Display clean public home page"""
    # Compact Hero Section
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🎬 Welcome to MediaHub</h1>
        <p class="page-subtitle">The Professional Platform for Content Creators and Viewers</p>
    </div>
    """, unsafe_allow_html=True)

    # Call to Action
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="action-card">
            <div class="feature-icon">🔐</div>
            <div class="feature-title">Existing User?</div>
            <div class="feature-desc">Access your account and continue creating</div>
            <a href="/Login" target="_self">
                <button style="background:#48bb78;color:white;">Go to Login</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="action-card">
            <div class="feature-icon">🆕</div>
            <div class="feature-title">New User?</div>
            <div class="feature-desc">Join thousands of creators today</div>
            <a href="/Register" target="_self">
                <button style="background:#4299e1;color:white;">Go to Register</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    # Features Section
    st.markdown('<div class="section-header"><h2>✨ Platform Features</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📺</div>
            <div class="feature-title">Channels</div>
            <div class="feature-desc">Create and manage your own branded channels</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎥</div>
            <div class="feature-title">Videos</div>
            <div class="feature-desc">Upload and share high-quality content</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">Engagement</div>
            <div class="feature-desc">Build community through interactions</div>
        </div>
        """, unsafe_allow_html=True)

    # Recent Videos
    st.markdown('<div class="section-header"><h2>🔥 Trending Content</h2></div>', unsafe_allow_html=True)
    display_recent_videos()

    # Demo Account Info
    st.markdown("""
    <div class="info-box">
        💡 <strong>Demo Account:</strong> Username: <code>admin</code> | Password: <code>admin123</code>
    </div>
    """, unsafe_allow_html=True)

def display_admin_dashboard():
    """Clean admin dashboard"""
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">👑 Admin Dashboard</h1>
        <p class="page-subtitle">Complete overview and control of your platform</p>
    </div>
    """, unsafe_allow_html=True)

    database = db.get_db()

    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_users = database.users.count_documents({})
        st.metric("👥 Total Users", f"{total_users:,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_channels = database.channels.count_documents({})
        st.metric("📺 Total Channels", f"{total_channels:,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_videos = database.videos.count_documents({})
        st.metric("🎥 Total Videos", f"{total_videos:,}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_comments = database.comments.count_documents({})
        st.metric("💬 Total Comments", f"{total_comments:,}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Analytics Section
    st.markdown('<div class="section-header"><h2>📊 Analytics Overview</h2></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        role_counts = {}
        for role in [settings.ROLE_ADMIN, settings.ROLE_CREATOR, settings.ROLE_VIEWER]:
            count = database.users.count_documents({"role": role})
            role_counts[role] = count

        fig = go.Figure(data=[go.Pie(
            labels=list(role_counts.keys()), 
            values=list(role_counts.values()),
            hole=0.4,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb'])
        )])
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=40, b=10),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(text="Users by Role", font=dict(size=16, weight='bold'))
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        content_data = {
            'Channels': database.channels.count_documents({}),
            'Videos': database.videos.count_documents({}),
            'Comments': database.comments.count_documents({})
        }
        
        fig = go.Figure(data=[go.Bar(
            x=list(content_data.keys()),
            y=list(content_data.values()),
            marker=dict(color=['#667eea', '#764ba2', '#f093fb'])
        )])
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=40, b=10),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(text="Content Distribution", font=dict(size=16, weight='bold')),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)

    # Recent Activity
    st.markdown('<div class="section-header"><h2>📋 Recent Activity</h2></div>', unsafe_allow_html=True)

    recent_users = list(database.users.find().sort("created_at", -1).limit(5))
    if recent_users:
        for user in recent_users:
            created_at = user.get('created_at')
            time_str = created_at.strftime('%b %d, %Y at %H:%M') if created_at else "N/A"
            st.markdown(f"""
            <div class="activity-item">
                <strong>👤 {user['username']}</strong> 
                <span style="color: #667eea;">({user['role']})</span> 
                joined on {time_str}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state"><div class="empty-icon">🔭</div><div class="empty-text">No recent activity</div></div>', unsafe_allow_html=True)

def display_creator_dashboard():
    """Clean creator dashboard"""
    user = Auth.get_current_user()
    user_model = UserModel()
    stats = user_model.get_user_stats(str(user['_id']))

    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">🎨 Creator Studio</h1>
        <p class="page-subtitle">Welcome back, {user['username']}! Ready to create?</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics - Custom HTML for better control
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 13px; color: #4a5568; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                    📺 My Channels
                </div>
                <div style="font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    {stats.get('channels', 0)}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 13px; color: #4a5568; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                    🎥 My Videos
                </div>
                <div style="font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    {stats.get('videos', 0)}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 13px; color: #4a5568; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                    👁️ Total Views
                </div>
                <div style="font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    {stats.get('total_views', 0):,}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 13px; color: #4a5568; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                    📋 My Playlists
                </div>
                <div style="font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    {stats.get('playlists', 0)}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Quick Actions
    st.markdown('<div class="section-header"><h2>⚡ Quick Actions</h2></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📺</div>
            <div class="feature-title">Manage Channels</div>
            <div class="feature-desc">Create and customize channels</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎬</div>
            <div class="feature-title">Upload Videos</div>
            <div class="feature-desc">Share your latest content</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">View Analytics</div>
            <div class="feature-desc">Track your performance</div>
        </div>
        """, unsafe_allow_html=True)

    # Recent Videos
    st.markdown('<div class="section-header"><h2>🎥 My Recent Videos</h2></div>', unsafe_allow_html=True)
    
    from models.video import VideoModel
    from utils.helpers import Helpers
    video_model = VideoModel()
    my_videos = video_model.get_by_creator(str(user['_id']))

    if my_videos:
        cols = st.columns(3)
        for idx, video in enumerate(my_videos[:6]):
            with cols[idx % 3]:
                st.markdown('<div class="video-card">', unsafe_allow_html=True)
                st.image(video.get('thumbnail', 'https://via.placeholder.com/300x200'))
                st.markdown(f'<div class="video-title">{video["title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="video-stats">👁️ {Helpers.format_number(video.get("views", 0))} • 👍 {Helpers.format_number(video.get("likes", 0))} • 📅 {Helpers.time_ago(video.get("created_at"))}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state"><div class="empty-icon">🔭</div><div class="empty-text">No videos yet. Upload your first masterpiece!</div></div>', unsafe_allow_html=True)

def display_viewer_dashboard():
    """Clean viewer dashboard"""
    user = Auth.get_current_user()
    
    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">👀 Viewer Dashboard</h1>
        <p class="page-subtitle">Welcome back, {user['username']}! Discover amazing content</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><h2>🔥 Trending Videos</h2></div>', unsafe_allow_html=True)
    display_recent_videos()

# ======================================================================
# MAIN APPLICATION
# ======================================================================
def main():
    """Main application entry"""
    
    if not st.session_state.get("db_connected", False):
        st.error("⚠️ Database Connection Failed")
        st.info("💡 Please ensure MongoDB is running and configured correctly.")
        st.stop()

    # Display appropriate dashboard
    if Auth.is_authenticated():
        user = Auth.get_current_user()
        
        if user['role'] == settings.ROLE_ADMIN:
            display_admin_dashboard()
        elif user['role'] == settings.ROLE_CREATOR:
            display_creator_dashboard()
        else:
            display_viewer_dashboard()
    else:
        display_public_home()

if __name__ == "__main__":
    main()