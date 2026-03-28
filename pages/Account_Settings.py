import streamlit as st
from utils.auth import Auth
from models.user import UserModel
from utils.validators import Validators

st.set_page_config(page_title="Settings - MediaHub", page_icon="⚙️", layout="wide")

from utils.ui import sidebar_v2

# Render sidebar
with st.sidebar:
    sidebar_v2()

Auth.require_auth()

user = Auth.get_current_user()
user_model = UserModel()

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
    background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(229, 62, 62, 0.3) !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="baseButton-secondary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(229, 62, 62, 0.5) !important;
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
.info-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    border: 2px solid #e2e8f0;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.info-card:hover {
    border-color: #667eea;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
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

/* Checkbox */
.stCheckbox {
    padding: 8px 0;
}

.stCheckbox > label {
    font-weight: 500 !important;
    color: #2d3748 !important;
}

/* Feature List */
.feature-list {
    background: linear-gradient(135deg, #f6f8fb 0%, #e9ecef 100%);
    border-radius: 16px;
    padding: 24px;
    border-left: 4px solid #667eea;
    margin: 20px 0;
}

.feature-list h4 {
    color: #2d3748;
    margin: 0 0 16px 0;
    font-size: 18px;
    font-weight: 600;
}

.feature-list ul {
    margin: 0;
    padding-left: 20px;
    color: #4a5568;
    font-size: 14px;
    line-height: 1.8;
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
    <h1 class="page-title">⚙️ Account Settings</h1>
    <p class="page-subtitle">Manage your profile, security, and preferences</p>
</div>
""", unsafe_allow_html=True)

# ======================================================================
# TABS
# ======================================================================
tab1, tab2, tab3 = st.tabs(["👤 Profile Settings", "🔒 Account Settings", "ℹ️ System Info"])

# Tab 1: Profile Settings
with tab1:
    st.markdown("### 👤 Profile Settings")
    
    with st.form("profile_settings_form"):
        st.markdown("#### Edit Your Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", value=user['username'], disabled=True, 
                                    help="Username cannot be changed")
            email = st.text_input("📧 Email*", value=user['email'])
        
        with col2:
            role = st.text_input("Role", value=user['role'], disabled=True)
            profile_image = st.text_input("🖼️ Profile Image URL", value=user.get('profile_image', ''),
                                         placeholder="https://example.com/image.jpg")
        
        bio = st.text_area("📝 Bio", value=user.get('bio', ''), 
                          placeholder="Tell us about yourself... (Max 500 characters)", 
                          max_chars=500,
                          height=120)
        
        st.caption(f"👤 Member since: {user['created_at'].strftime('%B %d, %Y')}")
        
        submit = st.form_submit_button("💾 Save Profile", use_container_width=True)
        
        if submit:
            if not email:
                st.error("❌ Email is required")
            elif not Validators.validate_email(email):
                st.error("❌ Invalid email format")
            else:
                update_data = {
                    'email': email,
                    'profile_image': profile_image,
                    'bio': bio
                }
                
                user_model.update_profile(str(user['_id']), update_data)
                
                # Update session
                st.session_state.user.update(update_data)
                
                # Show success message immediately without rerun
                st.success("✅ Profile updated successfully!")
                st.balloons()
    
    # Profile Tips
    st.markdown("""
    <div class="feature-list">
        <h4>💡 Profile Tips</h4>
        <ul>
            <li>Use a professional email address for better communication</li>
            <li>Add a profile image to personalize your account</li>
            <li>Write a compelling bio to let others know about you</li>
            <li>Keep your information up-to-date</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Tab 2: Account Settings
with tab2:
    st.markdown("### 🔒 Account Security")
    
    # Change Password Section
    with st.expander("🔑 Change Password", expanded=True):
        with st.form("change_password_form"):
            st.markdown("#### Update Your Password")
            
            current_password = st.text_input("Current Password", type="password", 
                                            placeholder="Enter your current password")
            
            col1, col2 = st.columns(2)
            with col1:
                new_password = st.text_input("New Password", type="password",
                                            placeholder="Enter new password")
            with col2:
                confirm_password = st.text_input("Confirm New Password", type="password",
                                                placeholder="Confirm new password")
            
            st.caption("⚠️ Password must be at least 8 characters long")
            
            submit = st.form_submit_button("🔒 Change Password", use_container_width=True)
            
            if submit:
                if not current_password or not new_password or not confirm_password:
                    st.error("❌ Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("❌ New passwords do not match")
                else:
                    valid, message = Validators.validate_password(new_password)
                    if not valid:
                        st.error(f"❌ {message}")
                    else:
                        # Verify current password
                        user_data = user_model.get_by_id(str(user['_id']))
                        
                        if user_data and Auth.verify_password(current_password, user_data['password']):
                            # Update password
                            new_hash = Auth.hash_password(new_password)
                            user_model.update_profile(str(user['_id']), {'password': new_hash})
                            
                            # Show success message immediately without rerun
                            st.success("✅ Password changed successfully!")
                            st.balloons()
                        else:
                            st.error("❌ Current password is incorrect")
    
    st.markdown("---")
    
    # Account Statistics
    st.markdown("### 📊 Account Statistics")
    
    stats = user_model.get_user_stats(str(user['_id']))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📺 Channels", stats['channels'])
    
    with col2:
        st.metric("🎬 Videos", stats['videos'])
    
    with col3:
        st.metric("📋 Playlists", stats['playlists'])
    
    with col4:
        st.metric("💬 Comments", stats['comments'])
    
    st.markdown("---")
    
    # Danger Zone
    with st.expander("⚠️ Danger Zone", expanded=False):
        st.markdown("### 🗑️ Delete Account")
        st.warning("⚠️ **Warning:** This action is irreversible! All your data will be permanently deleted.")
        
        st.markdown("""
        <div class="info-card">
            <h4 style="color: #e53e3e; margin: 0 0 12px 0;">What will be deleted:</h4>
            <ul style="margin: 0; padding-left: 20px; color: #4a5568; font-size: 14px; line-height: 1.8;">
                <li>Your user account and profile</li>
                <li>All channels you've created</li>
                <li>All videos you've uploaded</li>
                <li>All playlists you've created</li>
                <li>All comments you've posted</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        confirm_delete = st.checkbox("✅ I understand this action cannot be undone")
        
        if confirm_delete:
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("🗑️ Delete My Account", type="secondary", use_container_width=True):
                    # Delete user and all related data
                    from config.database import db
                    database = db.get_db()
                    
                    with st.spinner("Deleting account..."):
                        # Delete user's channels
                        database.channels.delete_many({"creator_id": str(user['_id'])})
                        
                        # Delete user's videos
                        database.videos.delete_many({"creator_id": str(user['_id'])})
                        
                        # Delete user's playlists
                        database.playlists.delete_many({"creator_id": str(user['_id'])})
                        
                        # Delete user's comments
                        database.comments.delete_many({"user_id": str(user['_id'])})
                        
                        # Delete user
                        user_model.delete_user(str(user['_id']))
                        
                        st.success("✅ Account deleted successfully. Logging out...")
                        st.balloons()
                        
                        # Use st.rerun() only for logout (necessary to redirect)
                        import time
                        time.sleep(2)
                        Auth.logout()

# Tab 3: System Info
with tab3:
    st.markdown("### ℹ️ System Information")
    
    from config.settings import settings
    from config.database import db
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3 style="margin: 0 0 16px 0; color: #1a202c;">📱 Application Info</h3>
            <p style="margin: 8px 0; color: #4a5568;"><strong>App Name:</strong> {}</p>
            <p style="margin: 8px 0; color: #4a5568;"><strong>Version:</strong> {}</p>
            <p style="margin: 8px 0; color: #4a5568;"><strong>Database:</strong> MongoDB</p>
            <p style="margin: 8px 0; color: #4a5568;"><strong>Framework:</strong> Streamlit</p>
        </div>
        """.format(settings.APP_NAME, settings.APP_VERSION), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3 style="margin: 0 0 16px 0; color: #1a202c;">📊 Database Statistics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        database = db.get_db()
        
        total_users = database.users.count_documents({})
        total_channels = database.channels.count_documents({})
        total_videos = database.videos.count_documents({})
        total_playlists = database.playlists.count_documents({})
        total_comments = database.comments.count_documents({})
        
        st.metric("👥 Total Users", total_users)
        st.metric("📺 Total Channels", total_channels)
        st.metric("🎬 Total Videos", total_videos)
        st.metric("📋 Total Playlists", total_playlists)
        st.metric("💬 Total Comments", total_comments)
    
    st.markdown("---")
    
    # Features Section
    st.markdown("""
    <div class="feature-list">
        <h4>🔧 Platform Features</h4>
        <ul>
            <li>✅ Role-based authentication (Admin, Creator, Viewer)</li>
            <li>✅ Channel management with subscriptions</li>
            <li>✅ Video upload and management</li>
            <li>✅ Playlist creation and organization</li>
            <li>✅ Comment system with threaded replies</li>
            <li>✅ Real-time analytics and reports</li>
            <li>✅ Advanced search and filtering</li>
            <li>✅ User profile management</li>
            <li>✅ View and like tracking</li>
            <li>✅ Content moderation tools</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Future Enhancements
    st.markdown("""
    <div class="feature-list" style="border-left-color: #48bb78;">
        <h4>🚀 Future Enhancements</h4>
        <ul>
            <li>🤖 AI-powered video recommendations</li>
            <li>📊 Comment sentiment analysis</li>
            <li>📝 Video transcription and closed captions</li>
            <li>📡 Live streaming support</li>
            <li>🛡️ Advanced content moderation AI</li>
            <li>✂️ Video editing tools</li>
            <li>📱 Mobile app integration</li>
            <li>💰 Monetization features</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)