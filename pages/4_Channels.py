import streamlit as st
from utils.auth import Auth
from models.channel import ChannelModel
from models.video import VideoModel
from utils.validators import Validators
from utils.helpers import Helpers
import streamlit.components.v1 as components
import hashlib
import time

st.set_page_config(page_title="Channel Management - MediaHub", page_icon="📺", layout="wide")

from utils.ui import sidebar_v2

# Render sidebar
with st.sidebar:
    sidebar_v2()

Auth.require_auth()

user = Auth.get_current_user()
channel_model = ChannelModel()
video_model = VideoModel()

# Initialize submission tracking
if 'last_channel_submission' not in st.session_state:
    st.session_state.last_channel_submission = None

# Check for success message
if 'channel_created' in st.session_state and st.session_state.channel_created:
    st.success("✅ Channel created successfully!")
    st.balloons()
    del st.session_state.channel_created

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

/* Cards */
.channel-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.channel-card:hover {
    border-color: #667eea;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
    transform: translateY(-4px);
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

/* Markdown Headers in Tabs */
.stTabs h3 {
    color: #1a202c;
    font-weight: 700;
    margin-bottom: 20px;
    font-size: 24px;
}

/* Caption Text */
.stCaption {
    color: #718096 !important;
    font-size: 13px !important;
}

/* Columns */
div[data-testid="column"] {
    padding: 0 8px;
}

/* Form Styling */
.stForm {
    background: #f8fafc;
    padding: 24px;
    border-radius: 16px;
    border: 2px solid #e2e8f0;
}

/* Select box dropdown */
.stSelectbox div[data-baseweb="select"] * {
    color: #2d3748 !important;
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

/* Channel Browse Grid */
.browse-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
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
    <h1 class="page-title">📺 Content Hub</h1>
    <p class="page-subtitle">Create, manage, and discover amazing channels</p>
</div>
""", unsafe_allow_html=True)

# ======================================================================
# TABS
# ======================================================================
tab1, tab2, tab3 = st.tabs(["📺 My Channels", "🌍 Browse Channels", "➕ Create Channel"])

# Tab 1: My Channels
with tab1:
    st.markdown("### 📺 My Channels")
    
    if user['role'] in ['Creator', 'Admin']:
        my_channels = channel_model.get_by_creator(str(user['_id']))
        
        if my_channels:
            for channel in my_channels:
                with st.expander(f"📺 {channel['channel_name']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {channel.get('description', 'No description')}")
                        st.caption(f"👥 {channel.get('subscribers', 0)} subscribers")
                        st.caption(f"📅 Created: {Helpers.time_ago(channel.get('created_at'))}")
                    
                    with col2:
                        analytics = channel_model.get_channel_analytics(str(channel['_id']))
                        if analytics:
                            st.metric("Videos", analytics['videos'])
                            st.metric("Total Views", Helpers.format_number(analytics['total_views']))
                    
                    st.markdown("---")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✏️ Edit", key=f"edit_{channel['_id']}", use_container_width=True):
                            st.session_state[f'editing_{channel["_id"]}'] = not st.session_state.get(f'editing_{channel["_id"]}', False)
                    
                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_{channel['_id']}", use_container_width=True):
                            channel_model.delete(str(channel['_id']))
                            st.success("Channel deleted!")
                            time.sleep(1)
                            st.rerun()
                    
                    with col3:
                        st.caption(f"📊 Videos: {analytics['videos'] if analytics else 0}")
                    
                    if st.session_state.get(f'editing_{channel["_id"]}', False):
                        st.markdown("---")
                        with st.form(f"edit_form_{channel['_id']}"):
                            new_name = st.text_input("Channel Name", value=channel['channel_name'])
                            new_desc = st.text_area("Description", value=channel.get('description', ''))
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                    channel_model.update(str(channel['_id']), {
                                        'channel_name': new_name,
                                        'description': new_desc
                                    })
                                    st.session_state[f'editing_{channel["_id"]}'] = False
                                    st.success("Channel updated!")
                                    time.sleep(1)
                                    st.rerun()
                            
                            with col2:
                                if st.form_submit_button("❌ Cancel", use_container_width=True):
                                    st.session_state[f'editing_{channel["_id"]}'] = False
                                    st.rerun()
        else:
            st.info("📢 You haven't created any channels yet. Create one in the 'Create Channel' tab!")
    else:
        st.warning("⚠️ Only Creators and Admins can manage channels")

# Tab 2: Browse Channels - WITH SUBSCRIPTION TOGGLE
with tab2:
    st.markdown("### 🌍 Browse All Channels")
    
    all_channels = channel_model.get_all()
    
    if all_channels:
        cols = st.columns(3)
        for idx, channel in enumerate(all_channels):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="channel-card">
                    <h3 style="margin: 0 0 8px 0; color: #1a202c;">📺 {channel['channel_name']}</h3>
                    <p style="color: #718096; font-size: 14px; margin-bottom: 12px;">{channel.get('description', 'No description')[:100]}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Get subscriber count
                subscriber_count = channel.get('subscribers', 0)
                st.metric("👥 Subscribers", subscriber_count)
                
                # Check if user is already subscribed
                is_subscribed = channel_model.is_user_subscribed(
                    str(channel['_id']), 
                    str(user['_id'])
                )
                
                # Show appropriate button based on subscription status
                if is_subscribed:
                    if st.button("✓ Subscribed", key=f"unsub_{channel['_id']}", type="secondary", use_container_width=True):
                        success = channel_model.unsubscribe(str(channel['_id']), str(user['_id']))
                        if success:
                            st.success("Unsubscribed!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Error unsubscribing!")
                else:
                    if st.button("🔔 Subscribe", key=f"sub_{channel['_id']}", type="primary", use_container_width=True):
                        success = channel_model.subscribe(str(channel['_id']), str(user['_id']))
                        if success:
                            st.success("Subscribed!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Already subscribed!")
                
                st.markdown("---")
    else:
        st.info("📢 No channels available yet")

# Tab 3: Create Channel - WITH DUPLICATE PREVENTION
with tab3:
    st.markdown("### ➕ Create New Channel")
    
    if user['role'] in ['Creator', 'Admin']:
        with st.form("create_channel_form", clear_on_submit=True):
            channel_name = st.text_input("📺 Channel Name*", placeholder="Enter your channel name")
            description = st.text_area("📝 Description", placeholder="Describe what your channel is about")
            category = st.selectbox("📁 Category", ["General", "Education", "Entertainment", 
                                                 "Technology", "Gaming", "Music", "Other"])
            
            submit = st.form_submit_button("🚀 Create Channel", use_container_width=True)
            
            if submit:
                # Create unique submission ID to prevent duplicates
                submission_id = hashlib.md5(
                    f"{channel_name}{user['_id']}{time.time()}".encode()
                ).hexdigest()
                
                # Check if this is a duplicate submission
                if st.session_state.last_channel_submission == submission_id:
                    st.warning("⚠️ Channel already being created, please wait...")
                elif not channel_name:
                    st.error("❌ Channel name is required")
                else:
                    # Check if channel name already exists for this user
                    existing_channels = channel_model.get_by_creator(str(user['_id']))
                    if any(ch['channel_name'].lower() == channel_name.lower() for ch in existing_channels):
                        st.error("❌ You already have a channel with this name!")
                    else:
                        valid, message = Validators.validate_channel_name(channel_name)
                        if not valid:
                            st.error(f"❌ {message}")
                        else:
                            # Mark this submission to prevent duplicates
                            st.session_state.last_channel_submission = submission_id
                            
                            channel_data = {
                                'channel_name': channel_name,
                                'description': description,
                                'category': category,
                                'creator_id': str(user['_id']),
                                'creator_name': user['username']
                            }
                            
                            try:
                                channel_id = channel_model.create(channel_data)
                                st.session_state.channel_created = True
                                st.success(f"✅ Channel '{channel_name}' created successfully!")
                                st.info(f"**Name:** {channel_name}\n\n**Category:** {category}")
                                
                                # Clear submission ID after 2 seconds
                                time.sleep(2)
                                st.session_state.last_channel_submission = None
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Error creating channel: {e}")
                                st.session_state.last_channel_submission = None
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f6f8fb 0%, #e9ecef 100%); 
                    border-radius: 16px; padding: 20px; margin-top: 24px; 
                    border-left: 4px solid #667eea;">
            <h4 style="color: #2d3748; margin: 0 0 12px 0; font-size: 16px;">💡 Channel Tips</h4>
            <ul style="margin: 0; padding-left: 20px; color: #4a5568; font-size: 14px; line-height: 1.8;">
                <li>Choose a unique and memorable channel name</li>
                <li>Write a clear description to attract subscribers</li>
                <li>Select the most relevant category</li>
                <li>Start uploading quality content regularly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Only Creators and Admins can create channels")