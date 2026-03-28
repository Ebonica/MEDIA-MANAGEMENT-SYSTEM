import streamlit as st
from utils.auth import Auth
from models.video import VideoModel
from models.channel import ChannelModel
from utils.helpers import Helpers
from config.database import db

st.set_page_config(
    page_title="Media Management System",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.ui import sidebar_v2

with st.sidebar:
    sidebar_v2()

# Enhanced Professional CSS
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Smooth Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    /* Hero Section - Modern Gradient */
    .hero-section {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 5rem 3rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: float 20s infinite linear;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 20px rgba(0,0,0,0.3);
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        opacity: 0.95;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        margin-top: 1.5rem;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Modern Feature Cards */
    .feature-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        height: 100%;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.25);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        transition: transform 0.4s ease;
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.1) rotate(5deg);
    }
    
    .feature-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #1a202c;
        letter-spacing: -0.5px;
    }
    
    .feature-desc {
        color: #718096;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    
    /* Stats Card - Glassmorphism */
    .stats-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.18);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stats-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        opacity: 0.9;
        z-index: -1;
    }
    
    .stats-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
    }
    
    .stats-number {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: white;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }
    
    .stats-label {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.95);
        font-weight: 500;
    }
    
    /* Video Card - Premium Design */
    .video-card-custom {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    .video-card-custom:hover {
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        transform: translateY(-8px);
    }
    
    .video-thumbnail {
        position: relative;
        overflow: hidden;
        background: #000;
        aspect-ratio: 16/9;
    }
    
    .video-thumbnail img {
        transition: transform 0.4s ease;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .video-thumbnail video {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.4s ease;
    }
    
    .video-card-custom:hover .video-thumbnail img,
    .video-card-custom:hover .video-thumbnail video {
        transform: scale(1.1);
    }
    
    .video-play-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 60px;
        height: 60px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 10;
    }
    
    .video-play-overlay:hover {
        background: rgba(255, 255, 255, 1);
        transform: translate(-50%, -50%) scale(1.1);
    }
    
    /* Channel Card */
    .channel-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    .channel-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 2rem;
        color: #1a202c;
        position: relative;
        display: inline-block;
        letter-spacing: -1px;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 0;
        width: 60px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    /* Welcome Card */
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
    }
    
    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 3rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin: 3rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .cta-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 50px 50px;
    }
    
    /* Divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,0,0,0.1), transparent);
        margin: 4rem 0;
    }
    
    /* Buttons Enhancement */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }
    
    /* Info Boxes */
    .info-box {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    /* Metric Enhancement */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Smooth Page Load */
    .main > div {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Loading Shimmer */
    .shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HERO SECTION
# ============================================================================
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🎥 Media Management System</div>
    <div class="hero-subtitle">Create, Share, and Discover Amazing Content</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# WELCOME MESSAGE
# ============================================================================
if Auth.is_authenticated():
    user = Auth.get_current_user()
    st.markdown(f"""
    <div class="welcome-card">
        <h2 style="margin-bottom: 0.5rem;">👋 Welcome back, {user['username']}!</h2>
        <p style="opacity: 0.9; font-size: 1.1rem;">Ready to create something amazing today?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if user['role'] in ['Creator', 'Admin']:
            st.button("📺 My Channels", use_container_width=True, type="primary")
    
    with col2:
        if user['role'] in ['Creator', 'Admin']:
            st.button("🎬 Upload Video", use_container_width=True, type="primary")
    
    with col3:
        st.button("🔍 Search Videos", use_container_width=True)
    
    with col4:
        st.button("📊 View Analytics", use_container_width=True)
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 800; color: #1a202c; margin-bottom: 1rem;">
                🚀 Join Our Community Today!
            </h1>
            <p style="font-size: 1.2rem; color: #718096; margin-bottom: 3rem; line-height: 1.6;">
                Start creating and sharing your content with millions of viewers worldwide
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div class="info-box">
                <h3 style="color: #667eea; margin-bottom: 0.5rem;">🔑 Already a Member?</h3>
                <p style="color: #718096;">Navigate to <strong>Login</strong> using the sidebar</p>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="info-box" style="border-left-color: #23d5ab;">
                <h3 style="color: #23d5ab; margin-bottom: 0.5rem;">✨ New Here?</h3>
                <p style="color: #718096;">Navigate to <strong>Register</strong> using the sidebar</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# PLATFORM STATISTICS
# ============================================================================
st.markdown('<h2 class="section-header">📊 Platform Statistics</h2>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

try:
    database = db.get_db()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = database.users.count_documents({})
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{total_users:,}</div>
            <div class="stats-label">👥 Total Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_channels = database.channels.count_documents({})
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{total_channels:,}</div>
            <div class="stats-label">📺 Active Channels</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_videos = database.videos.count_documents({})
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{total_videos:,}</div>
            <div class="stats-label">🎥 Total Videos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        pipeline = [{"$group": {"_id": None, "total": {"$sum": "$views"}}}]
        result = list(database.videos.aggregate(pipeline))
        total_views = result[0]['total'] if result else 0
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{Helpers.format_number(total_views)}</div>
            <div class="stats-label">👁️ Total Views</div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.warning("📊 Statistics will be available shortly")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# PLATFORM FEATURES
# ============================================================================
st.markdown('<h2 class="section-header">✨ Platform Features</h2>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📺</div>
        <div class="feature-title">Channel Management</div>
        <div class="feature-desc">
            Create and customize your own channels. Build your brand and grow your audience with powerful analytics and engagement tools.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎬</div>
        <div class="feature-title">Video Hosting</div>
        <div class="feature-desc">
            Upload and manage unlimited videos. Advanced support for custom thumbnails, tags, categories, and comprehensive performance metrics.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Engagement Tools</div>
        <div class="feature-desc">
            Connect deeply with your audience through interactive comments, real-time likes, subscriptions, and community building features.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Advanced Analytics</div>
        <div class="feature-desc">
            Track your performance with detailed insights. Monitor views, engagement rates, subscriber growth, and revenue analytics in real-time.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <div class="feature-title">Playlist Creation</div>
        <div class="feature-desc">
            Organize your content intelligently into curated playlists. Enhance discoverability and keep viewers engaged with your content longer.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Smart Search</div>
        <div class="feature-desc">
            Find exactly what you're looking for instantly. Advanced filtering by title, tags, categories, creators, and popularity metrics.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# TRENDING VIDEOS
# ============================================================================
st.markdown('<h2 class="section-header">🔥 Trending Videos</h2>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

try:
    video_model = VideoModel()
    trending_videos = video_model.get_top_videos('views', 6)
    
    if trending_videos:
        cols = st.columns(3)
        
        for idx, video in enumerate(trending_videos):
            with cols[idx % 3]:
                st.markdown('<div class="video-card-custom">', unsafe_allow_html=True)
                
                st.markdown('<div class="video-thumbnail">', unsafe_allow_html=True)
                
                # Check if custom thumbnail exists
                if video.get('thumbnail') and video['thumbnail'] != 'https://via.placeholder.com/400x225/667eea/ffffff?text=Video+Thumbnail':
                    # Display custom thumbnail
                    st.image(
                        video['thumbnail'],
                        use_column_width=True
                    )
                elif video.get('video_url'):
                    # Display video preview with controls disabled and muted
                    st.video(video['video_url'], start_time=0)
                else:
                    # Fallback placeholder
                    st.image(
                        'https://via.placeholder.com/400x225/667eea/ffffff?text=Video+Preview',
                        use_column_width=True
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div style="padding: 1rem;">', unsafe_allow_html=True)
                st.markdown(f"<h4 style='margin: 0 0 0.5rem 0; color: #1a202c;'>{video['title'][:60]}{'...' if len(video['title']) > 60 else ''}</h4>", unsafe_allow_html=True)
                
                st.caption(f"📺 {video.get('creator_name', 'Unknown Creator')}")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.caption(f"👁️ {Helpers.format_number(video.get('views', 0))}")
                with col_b:
                    st.caption(f"👍 {Helpers.format_number(video.get('likes', 0))}")
                
                st.caption(f"🕐 {Helpers.time_ago(video.get('created_at'))}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🎬 No videos available yet. Be the first to upload content!")

except Exception as e:
    st.warning("🎥 Trending videos will appear here")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# POPULAR CHANNELS
# ============================================================================
st.markdown('<h2 class="section-header">🌟 Popular Channels</h2>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

try:
    channel_model = ChannelModel()
    popular_channels = channel_model.get_all(limit=6)
    popular_channels = sorted(popular_channels, key=lambda x: x.get('subscribers', 0), reverse=True)
    
    if popular_channels:
        cols = st.columns(3)
        
        for idx, channel in enumerate(popular_channels[:6]):
            with cols[idx % 3]:
                st.markdown('<div class="channel-card">', unsafe_allow_html=True)
                
                st.markdown(f"<h3 style='color: #1a202c; margin-bottom: 0.5rem;'>📺 {channel['channel_name']}</h3>", unsafe_allow_html=True)
                st.caption(f"By {channel.get('creator_name', 'Unknown')}")
                st.markdown(f"<p style='color: #718096; margin: 1rem 0;'>{channel.get('description', 'No description')[:100]}{'...' if len(channel.get('description', '')) > 100 else ''}</p>", unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Subscribers", Helpers.format_number(channel.get('subscribers', 0)))
                with col_b:
                    analytics = channel_model.get_channel_analytics(str(channel['_id']))
                    if analytics:
                        st.metric("Videos", analytics['videos'])
                
                st.button("View Channel", key=f"ch_{channel['_id']}", use_container_width=True, type="primary")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📺 Popular channels will appear here")

except Exception as e:
    st.warning("📺 Channels will be displayed shortly")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# CALL TO ACTION
# ============================================================================
if not Auth.is_authenticated():
    st.markdown("""
    <div class="cta-section">
        <h2 style="font-size: 2.5rem; margin-bottom: 1rem; font-weight: 800;">🚀 Ready to Get Started?</h2>
        <p style="font-size: 1.3rem; margin-bottom: 2rem; opacity: 0.95;">
            Join thousands of creators and viewers already using our platform!
        </p>
        <p style="font-size: 1.1rem; opacity: 0.9;">
            👈 Use the sidebar to navigate to <strong>Register</strong> or <strong>Login</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="cta-section">
        <h3 style="font-size: 2rem; margin-bottom: 1rem;">✨ Explore More Features</h3>
        <p style="font-size: 1.1rem; opacity: 0.9;">
            Use the sidebar navigation to access all platform features and tools
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER INFO
# ============================================================================
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #667eea; margin-bottom: 1rem;">📚 Resources</h4>
        <p style="color: #718096; line-height: 2;">
            • User Guide<br>
            • Video Tutorials<br>
            • Best Practices<br>
            • Creator Academy
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #667eea; margin-bottom: 1rem;">💡 Support</h4>
        <p style="color: #718096; line-height: 2;">
            • Help Center<br>
            • Community Forum<br>
            • Contact Support<br>
            • Report Issues
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🔗 Connect</h4>
        <p style="color: #718096; line-height: 2;">
            • System Status<br>
            • Platform Updates<br>
            • Feature Requests<br>
            • Feedback
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #718096;">
    <p style="font-size: 0.95rem;">© 2024 Media Management System | Built with ❤️ using Streamlit & MongoDB</p>
</div>
""", unsafe_allow_html=True)