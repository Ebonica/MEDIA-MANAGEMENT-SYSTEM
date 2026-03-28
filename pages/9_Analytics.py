# ============================================================================
# FILE: pages/9_Analytics.py - PROFESSIONAL UI VERSION
# ============================================================================
import streamlit as st
from utils.auth import Auth
from models.video import VideoModel
from models.channel import ChannelModel
from models.user import UserModel
from utils.helpers import Helpers
from config.database import db
from config.settings import settings
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Analytics & Reports", page_icon="📊", layout="wide")

from utils.ui import sidebar_v2

with st.sidebar:
    sidebar_v2()

Auth.require_auth()

# ======================================================================
# MAIN STYLING - MATCHING CHANNELS PAGE
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

/* Metric Cards */
.metric-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    border-left: 4px solid #667eea;
    transition: all 0.3s ease;
    margin-bottom: 16px;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
    border-left-width: 6px;
}

.metric-title {
    color: #667eea;
    font-size: 14px;
    font-weight: 600;
    margin: 0 0 8px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #1a202c;
    margin: 0;
    line-height: 1;
}

.metric-label {
    color: #718096;
    font-size: 13px;
    margin: 8px 0 0 0;
}

/* Chart Container (base, will be overridden below) */
.chart-container {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    margin: 0 0 16px 0;
    border: 2px solid #e2e8f0;
}

.chart-title {
    font-size: 18px;
    font-weight: 700;
    color: #1a202c;
    margin: 0 0 16px 0;
    padding-bottom: 12px;
    border-bottom: 2px solid #e2e8f0;
}

/* Top Item Styling */
.top-item {
    background: linear-gradient(to right, #f8f9fa, white);
    border-radius: 12px;
    padding: 16px;
    margin: 12px 0;
    border-left: 4px solid #667eea;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
}

.top-item:hover {
    background: linear-gradient(to right, #edf2f7, #f8f9fa);
    transform: translateX(8px);
    border-left-width: 6px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Rank Badges */
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: 700;
    margin-right: 12px;
    flex-shrink: 0;
}

.rank-badge.gold { 
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
    box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}

.rank-badge.silver { 
    background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%); 
    box-shadow: 0 4px 12px rgba(192, 192, 192, 0.4);
}

.rank-badge.bronze { 
    background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%); 
    box-shadow: 0 4px 12px rgba(205, 127, 50, 0.4);
}

/* Section Headers */
.section-header {
    font-size: 24px;
    font-weight: 700;
    color: #1a202c;
    margin: 24px 0 16px 0;
    padding: 16px 0;
    border-bottom: 3px solid #667eea;
}

/* Video Card in Trending */
.video-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    min-height: 180px;
    display: flex;
    align-items: center;
}

.video-card:hover {
    border-color: #667eea;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
    transform: translateY(-4px);
}

.video-card-content {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 20px;
}

.video-thumbnail {
    flex-shrink: 0;
    width: 200px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.video-info {
    flex: 1;
    min-width: 0;
}

.video-title {
    font-size: 18px;
    font-weight: 600;
    color: #1a202c;
    margin: 12px 0 8px 0;
}

.video-meta {
    color: #718096;
    font-size: 14px;
    line-height: 1.6;
}

/* Info Box */
.info-box {
    background: linear-gradient(135deg, #f6f8fb 0%, #e9ecef 100%);
    border-radius: 16px;
    padding: 20px;
    margin-top: 24px;
    border-left: 4px solid #667eea;
}

.info-box h4 {
    color: #2d3748;
    margin: 0 0 12px 0;
    font-size: 16px;
    font-weight: 600;
}

/* Dataframe Styling */
.dataframe {
    border-radius: 12px !important;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
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
    
    .metric-value {
        font-size: 24px;
    }
    
    .video-card-content {
        flex-direction: column;
    }
    
    .video-thumbnail {
        width: 100%;
    }
}

/* --- Compact charts: remove big white card under section titles --- */
.chart-container {
    background: transparent !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: none !important;
}

.section-header {
    margin-bottom: 8px !important;
}

.block-container {
    padding-bottom: 0rem !important;
}

[data-testid="stPlotlyChart"] {
    margin-bottom: 0px !important;
}
</style>
""", unsafe_allow_html=True)

# ======================================================================
# PAGE HEADER
# ======================================================================
st.markdown("""
<div class="page-header">
    <h1 class="page-title">📊 Analytics Dashboard</h1>
    <p class="page-subtitle">Insights, metrics, and performance analytics</p>
</div>
""", unsafe_allow_html=True)

user = Auth.get_current_user()
video_model = VideoModel()
channel_model = ChannelModel()
user_model = UserModel()

# ============================================================================
# ENHANCED FUNCTIONS
# ============================================================================

def display_admin_analytics():
    """Enhanced Admin analytics dashboard"""
    
    database = db.get_db()
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = database.users.count_documents({})
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">👥 Total Users</p>
            <h1 class="metric-value">{total_users}</h1>
            <p class="metric-label">Registered accounts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_channels = database.channels.count_documents({})
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">📺 Total Channels</p>
            <h1 class="metric-value">{total_channels}</h1>
            <p class="metric-label">Active channels</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_videos = database.videos.count_documents({})
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">🎥 Total Videos</p>
            <h1 class="metric-value">{total_videos}</h1>
            <p class="metric-label">Published content</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        pipeline = [{"$group": {"_id": None, "total": {"$sum": "$views"}}}]
        result = list(database.videos.aggregate(pipeline))
        total_views = result[0]['total'] if result else 0
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">👁️ Total Views</p>
            <h1 class="metric-value">{Helpers.format_number(total_views)}</h1>
            <p class="metric-label">Platform engagement</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Section
    st.markdown('<h3 class="section-header">📊 Distribution Analytics</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="chart-title">👥 Users by Role</p>', unsafe_allow_html=True)
        
        roles = ['Admin', 'Creator', 'Viewer']
        role_counts = [database.users.count_documents({"role": role}) for role in roles]
        
        colors = ['#667eea', '#764ba2', '#f093fb']
        fig = go.Figure(data=[go.Pie(
            labels=roles, 
            values=role_counts, 
            hole=0.4,
            marker=dict(colors=colors),
            textfont=dict(size=14, color='white', family='Poppins'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        fig.update_layout(
            height=350,
            showlegend=True,
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=-0.2, 
                xanchor="center", 
                x=0.5,
                font=dict(family='Poppins', size=12)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<p class="chart-title">📈 Videos by Category</p>', unsafe_allow_html=True)
        
        categories = settings.VIDEO_CATEGORIES
        category_counts = [database.videos.count_documents({"category": cat}) for cat in categories]
        
        fig = go.Figure(data=[go.Bar(
            x=categories, 
            y=category_counts,
            marker=dict(
                color=category_counts,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Videos")
            ),
            hovertemplate='<b>%{x}</b><br>Videos: %{y}<extra></extra>'
        )])
        fig.update_layout(
            height=350, 
            xaxis_tickangle=-45,
            showlegend=False,
            xaxis=dict(title="Category", titlefont=dict(family='Poppins')),
            yaxis=dict(title="Video Count", titlefont=dict(family='Poppins')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Content
    st.markdown('<h3 class="section-header">🏆 Top Performing Content</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="chart-title">🔥 Top 10 Videos by Views</p>', unsafe_allow_html=True)
        
        top_videos = video_model.get_top_videos('views', 10)
        
        if top_videos:
            for idx, video in enumerate(top_videos):
                rank_class = "gold" if idx == 0 else "silver" if idx == 1 else "bronze" if idx == 2 else ""
                st.markdown(f"""
                <div class="top-item">
                    <span class="rank-badge {rank_class}">{idx + 1}</span>
                    <div>
                        <strong style="color: #1a202c; font-size: 15px;">{video['title']}</strong><br>
                        <small style="color: #718096;">👁️ {Helpers.format_number(video.get('views', 0))} views • by {video.get('creator_name', 'Unknown')}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🔭 No videos yet")
    
    with col2:
        st.markdown('<p class="chart-title">❤️ Top 10 Videos by Likes</p>', unsafe_allow_html=True)
        
        top_liked = video_model.get_top_videos('likes', 10)
        
        if top_liked:
            for idx, video in enumerate(top_liked):
                rank_class = "gold" if idx == 0 else "silver" if idx == 1 else "bronze" if idx == 2 else ""
                st.markdown(f"""
                <div class="top-item">
                    <span class="rank-badge {rank_class}">{idx + 1}</span>
                    <div>
                        <strong style="color: #1a202c; font-size: 15px;">{video['title']}</strong><br>
                        <small style="color: #718096;">👍 {Helpers.format_number(video.get('likes', 0))} likes • by {video.get('creator_name', 'Unknown')}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🔭 No videos yet")
    
    # Top Channels
    st.markdown('<h3 class="section-header">📺 Top Channels</h3>', unsafe_allow_html=True)
    
    all_channels = channel_model.get_all()
    sorted_channels = sorted(all_channels, key=lambda x: x.get('subscribers', 0), reverse=True)[:10]
    
    if sorted_channels:
        for idx, channel in enumerate(sorted_channels):
            rank_class = "gold" if idx == 0 else "silver" if idx == 1 else "bronze" if idx == 2 else ""
            st.markdown(f"""
            <div class="top-item">
                <span class="rank-badge {rank_class}">{idx + 1}</span>
                <div>
                    <strong style="color: #1a202c; font-size: 15px;">{channel['channel_name']}</strong><br>
                    <small style="color: #718096;">👤 by {channel['creator_name']} • 👥 {Helpers.format_number(channel.get('subscribers', 0))} subscribers</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔭 No channels yet")

def display_creator_analytics():
    """Enhanced Creator analytics dashboard"""
    
    stats = user_model.get_user_stats(str(user['_id']))
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">📺 My Channels</p>
            <h1 class="metric-value">{stats['channels']}</h1>
            <p class="metric-label">Created channels</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">🎥 My Videos</p>
            <h1 class="metric-value">{stats['videos']}</h1>
            <p class="metric-label">Published content</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">👁️ Total Views</p>
            <h1 class="metric-value">{Helpers.format_number(stats['total_views'])}</h1>
            <p class="metric-label">Content reach</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">💬 Engagement</p>
            <h1 class="metric-value">{stats['comments']}</h1>
            <p class="metric-label">Total comments</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Channel Performance
    my_channels = channel_model.get_by_creator(str(user['_id']))
    
    if my_channels:
        st.markdown('<h3 class="section-header">📺 Channel Performance</h3>', unsafe_allow_html=True)
        
        channel_data = []
        for channel in my_channels:
            analytics = channel_model.get_channel_analytics(str(channel['_id']))
            if analytics:
                channel_data.append({
                    'Channel': channel['channel_name'],
                    'Subscribers': analytics['subscribers'],
                    'Videos': analytics['videos'],
                    'Views': analytics['total_views'],
                    'Likes': analytics['total_likes']
                })
        
        if channel_data:
            df = pd.DataFrame(channel_data)
            
            st.dataframe(
                df.style.background_gradient(cmap='Purples', subset=['Subscribers', 'Views', 'Likes']),
                use_container_width=True,
                height=200
            )
            
            # Comparison chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Subscribers', 
                x=df['Channel'], 
                y=df['Subscribers'],
                marker_color='#667eea'
            ))
            fig.add_trace(go.Bar(
                name='Videos', 
                x=df['Channel'], 
                y=df['Videos'],
                marker_color='#764ba2'
            ))
            fig.update_layout(
                barmode='group', 
                height=350,
                hovermode='x unified',
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.02, 
                    xanchor="right", 
                    x=1,
                    font=dict(family='Poppins')
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins'),
                margin=dict(t=40, b=0, l=0, r=0)
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("🔭 No channels yet. Create your first channel!")
    
    # Video Performance
    my_videos = video_model.get_by_creator(str(user['_id']))
    
    if my_videos:
        st.markdown('<h3 class="section-header">🎥 Top 10 Video Performance</h3>', unsafe_allow_html=True)
        
        sorted_videos = sorted(my_videos, key=lambda x: x.get('views', 0), reverse=True)[:10]
        
        video_titles = [v['title'][:30] + '...' if len(v['title']) > 30 else v['title'] for v in sorted_videos]
        video_views = [v.get('views', 0) for v in sorted_videos]
        video_likes = [v.get('likes', 0) for v in sorted_videos]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Views', 
            x=video_titles, 
            y=video_views,
            marker_color='#667eea',
            hovertemplate='<b>%{x}</b><br>Views: %{y}<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            name='Likes', 
            x=video_titles, 
            y=video_likes,
            marker_color='#f093fb',
            hovertemplate='<b>%{x}</b><br>Likes: %{y}<extra></extra>'
        ))
        fig.update_layout(
            barmode='group', 
            height=350, 
            xaxis_tickangle=-45,
            hovermode='x unified',
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1,
                font=dict(family='Poppins')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins'),
            margin=dict(t=40, b=40, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("🔭 No videos yet. Upload your first video!")

def display_viewer_analytics():
    """Enhanced Viewer analytics dashboard"""
    
    stats = user_model.get_user_stats(str(user['_id']))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">💬 My Comments</p>
            <h1 class="metric-value">{stats['comments']}</h1>
            <p class="metric-label">Your engagement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">📋 Playlists</p>
            <h1 class="metric-value">{stats['playlists']}</h1>
            <p class="metric-label">Collections created</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-title">🎯 Total Activity</p>
            <h1 class="metric-value">{stats['comments'] + stats['playlists']}</h1>
            <p class="metric-label">All interactions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Trending Videos
    st.markdown('<h3 class="section-header">🔥 Trending Videos</h3>', unsafe_allow_html=True)

    top_videos = video_model.get_top_videos('views', 10)

    if top_videos:
        for idx, video in enumerate(top_videos):
            rank_class = "gold" if idx == 0 else "silver" if idx == 1 else "bronze" if idx == 2 else ""
            
            st.markdown(f"""
            <div class="video-card">
                <div class="video-card-content">
                    <div class="video-thumbnail">
                        <img src="{video.get('thumbnail', 'https://via.placeholder.com/300x200?text=Video')}" 
                             style="width: 100%; height: auto; display: block; border-radius: 12px;" 
                             alt="{video['title']}">
                    </div>
                    <div class="video-info">
                        <span class="rank-badge {rank_class}">#{idx + 1}</span>
                        <h3 class="video-title">{video['title']}</h3>
                        <p class="video-meta">
                            👤 <strong>{video['creator_name']}</strong><br>
                            👁️ {Helpers.format_number(video.get('views', 0))} views • 
                            👍 {Helpers.format_number(video.get('likes', 0))} likes • 
                            📁 {video.get('category', 'Unknown')}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔭 No videos available yet")

# ============================================================================
# RENDER BASED ON ROLE
# ============================================================================
if user['role'] == 'Admin':
    display_admin_analytics()
elif user['role'] == 'Creator':
    display_creator_analytics()
else:
    display_viewer_analytics()