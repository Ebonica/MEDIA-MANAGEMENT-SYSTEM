import streamlit as st
from utils.auth import Auth
from utils.validators import Validators
from config.settings import settings
import streamlit.components.v1 as components

st.set_page_config(page_title="Register - MediaHub", page_icon="📝", layout="wide")

# ======================================================================
# SIDEBAR
# ======================================================================
from utils.ui import sidebar_v2
with st.sidebar:
    sidebar_v2()

# ======================================================================
# CHECK IF ALREADY LOGGED IN
# ======================================================================
if Auth.is_authenticated():
    user = Auth.get_current_user()
    st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="max-width: 500px; margin: 100px auto; background: white; padding: 48px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); text-align: center;">
        <div style="width: 80px; height: 80px; margin: 0 auto 20px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 40px;">✓</div>
        <h1 style="font-size: 32px; font-weight: 700; color: #1a202c; margin: 20px 0 10px;">Already Logged In!</h1>
        <p style="font-size: 15px; color: #718096;">Welcome back, {user['username']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.success(f"✅ You are logged in as **{user['username']}** ({user['role']})")
    st.info("👈 Use the sidebar to navigate")
    st.stop()

# ======================================================================
# LEFT SIDE GRAPHICS (using HTML component)
# ======================================================================
graphics_html = """
<!DOCTYPE html>
<html>
<head>
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: 'Poppins', sans-serif;
    background: transparent;
    overflow: hidden;
}

.graphics-wrapper {
    padding: 30px 20px;
    text-align: center;
    height: 700px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.lock-illustration {
    width: 280px;
    height: 280px;
    margin: 0 auto 35px;
    position: relative;
}

.lock-body {
    width: 140px;
    height: 160px;
    background: linear-gradient(135deg, #ffffff, #f0f0f0);
    border-radius: 25px;
    margin: 80px auto 0;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    position: relative;
    animation: lockFloat 3s infinite ease-in-out;
}

@keyframes lockFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-15px); }
}

.lock-shackle {
    width: 65px;
    height: 85px;
    border: 11px solid #667eea;
    border-radius: 35px 35px 0 0;
    border-bottom: none;
    position: absolute;
    top: -65px;
    left: 50%;
    transform: translateX(-50%);
}

.lock-icon {
    font-size: 48px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.floating-circle {
    position: absolute;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    animation: pulse 3s infinite ease-in-out;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.circle-1 {
    width: 70px;
    height: 70px;
    top: 20px;
    left: 20px;
}

.circle-2 {
    width: 55px;
    height: 55px;
    bottom: 40px;
    right: 40px;
    animation-delay: 1s;
}

.circle-3 {
    width: 45px;
    height: 45px;
    top: 40px;
    right: 60px;
    animation-delay: 2s;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.7; }
    50% { transform: scale(1.15); opacity: 1; }
}

.hero-title {
    font-size: 46px;
    font-weight: 700;
    color: white;
    margin: 20px 0 15px 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.hero-subtitle {
    font-size: 17px;
    color: white;
    opacity: 0.95;
    line-height: 1.6;
    margin-bottom: 30px;
}

.feature-cards {
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 15px;
    width: 100%;
    max-width: 500px;
}

.feature-card {
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    padding: 20px 15px;
    border-radius: 16px;
    color: white;
    width: 145px;
    transition: all 0.3s ease;
    cursor: pointer;
    border: 2px solid rgba(255,255,255,0.3);
}

.feature-card:hover {
    transform: translateY(-8px);
    background: rgba(255,255,255,0.3);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.feature-icon {
    font-size: 38px;
    margin-bottom: 10px;
    display: block;
}

.feature-text {
    font-size: 14px;
    font-weight: 600;
    display: block;
}
</style>
</head>
<body>
<div class="graphics-wrapper">
    <div class="lock-illustration">
        <div class="floating-circle circle-1"></div>
        <div class="floating-circle circle-2"></div>
        <div class="floating-circle circle-3"></div>
        <div class="lock-body">
            <div class="lock-shackle"></div>
            <div class="lock-icon">📚</div>
        </div>
    </div>
    
    <div class="hero-title">🎬 MediaHub</div>
    <div class="hero-subtitle">
        Join Our Financial Literacy Platform<br>
        Start your learning journey today!
    </div>
    
    <div class="feature-cards">
        <div class="feature-card">
            <span class="feature-icon">🎓</span>
            <span class="feature-text">Expert Content</span>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🌍</span>
            <span class="feature-text">Multi-Language</span>
        </div>
        <div class="feature-card">
            <span class="feature-icon">📊</span>
            <span class="feature-text">Track Progress</span>
        </div>
    </div>
</div>
</body>
</html>
"""

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

.bg-shape {
    position: fixed;
    border-radius: 50%;
    opacity: 0.1;
    animation: float 20s infinite ease-in-out;
    pointer-events: none;
}

.bg-shape-1 {
    width: 400px;
    height: 400px;
    background: white;
    top: -100px;
    right: -100px;
}

.bg-shape-2 {
    width: 300px;
    height: 300px;
    background: white;
    bottom: -80px;
    left: -80px;
    animation-delay: 3s;
}

@keyframes float {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(20px, -20px) scale(1.1); }
}

.form-logo {
    width: 80px;
    height: 80px;
    margin: 0 auto 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    animation: logoFloat 3s infinite ease-in-out;
}

@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.form-title {
    font-size: 32px;
    font-weight: 700;
    color: #1a202c;
    text-align: center;
    margin: 20px 0 10px;
}

.form-subtitle {
    font-size: 15px;
    color: #718096;
    text-align: center;
    margin-bottom: 10px;
}

.stTextInput > div > div > input,
.stSelectbox > div > div > div {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    background: #f8fafc !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    background: white !important;
}

.stTextInput > label,
.stSelectbox > label {
    font-weight: 600 !important;
    color: #2d3748 !important;
    font-size: 14px !important;
    margin-bottom: 5px !important;
}

.stTextInput {
    margin-bottom: 15px !important;
}

.stSelectbox {
    margin-bottom: 15px !important;
}

/* Main register button styling */
.stForm .stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 24px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4) !important;
}

.stForm .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

/* Action buttons styling - Outside the form */
div[data-testid="column"]:nth-child(1) .stButton > button {
    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(66, 153, 225, 0.3) !important;
}

div[data-testid="column"]:nth-child(1) .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(66, 153, 225, 0.5) !important;
}

div[data-testid="column"]:nth-child(2) .stButton > button {
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(72, 187, 120, 0.3) !important;
}

div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(72, 187, 120, 0.5) !important;
}

/* Ensure proper column spacing */
div[data-testid="column"] {
    padding-left: 8px !important;
    padding-right: 8px !important;
}

.info-box {
    background: linear-gradient(135deg, #f6f8fb 0%, #e9ecef 100%);
    border-radius: 12px;
    padding: 16px;
    margin-top: 16px;
    border-left: 4px solid #667eea;
    font-size: 13px;
    color: #4a5568;
    line-height: 1.6;
}

.info-box strong {
    color: #2d3748;
    display: block;
    margin-bottom: 8px;
}

.register-box {
    background: rgba(255, 255, 255, 0.98);
    border-radius: 24px;
    padding: 10px 40px 48px 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    margin-top: 0 !important;
}

/* Remove extra padding/margin */
[data-testid="column"] {
    padding-top: 0 !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    max-width: 100% !important;
}

/* Remove white space above */
.element-container {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

section[data-testid="stVerticalBlock"] > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Remove gap above form elements */
.stForm {
    margin-top: -15px !important;
    padding-top: 0 !important;
}

div[data-testid="stVerticalBlock"] > div {
    gap: 0 !important;
}

/* Force remove all top spacing in right column */
[data-testid="column"]:last-child > div {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Ensure columns don't have weird gaps */
div[data-testid="column"] > div {
    gap: 0 !important;
}

/* Fix button container spacing */
div[data-testid="stHorizontalBlock"] {
    gap: 12px !important;
}

/* Style for divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    margin: 20px 0;
}

/* Select box styling */
.stSelectbox div[data-baseweb="select"] * {
    color: #2d3748 !important;
}

/* Messages styling */
.stSuccess, .stError, .stInfo, .stWarning {
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin: 12px 0 !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# Background shapes
st.markdown('<div class="bg-shape bg-shape-1"></div><div class="bg-shape bg-shape-2"></div>', unsafe_allow_html=True)

# ======================================================================
# TWO COLUMN LAYOUT
# ======================================================================
col1, col2 = st.columns([1, 1], gap="large")

# LEFT COLUMN - Graphics (HTML Component)
with col1:
    components.html(graphics_html, height=700, scrolling=False)

# RIGHT COLUMN - Register Form
with col2:
    st.markdown("""
    <div class="register-box">
        <div class="form-logo">📝</div>
        <div class="form-title">Create Account</div>
        <div class="form-subtitle">Join our financial literacy platform</div>
    """, unsafe_allow_html=True)
    
    # Registration Form
    with st.form("register_form", clear_on_submit=False):
        col_a, col_b = st.columns(2)
        
        with col_a:
            username = st.text_input(
                "👤 Username",
                placeholder="johndoe",
                help="Choose a unique username",
                key="username_input"
            )
        
        with col_b:
            email = st.text_input(
                "📧 Email",
                placeholder="john@example.com",
                help="Your email address",
                key="email_input"
            )
        
        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter password",
            help="Create a strong password",
            key="password_input"
        )
        
        confirm_password = st.text_input(
            "🔒 Confirm Password",
            type="password",
            placeholder="Re-enter password",
            help="Confirm your password",
            key="confirm_password_input"
        )
        
        role = st.selectbox(
            "👥 Account Type",
            [settings.ROLE_VIEWER, settings.ROLE_CREATOR],
            help="Choose your role"
        )
        
        submit = st.form_submit_button("🚀 Create Account", use_container_width=True)
        
        if submit:
            if not username or not email or not password or not confirm_password:
                st.error("⚠️ Please fill in all fields")
            elif password != confirm_password:
                st.error("⚠️ Passwords do not match")
            elif not Validators.validate_email(email):
                st.error("⚠️ Invalid email format")
            else:
                valid_username, username_msg = Validators.validate_username(username)
                if not valid_username:
                    st.error(f"⚠️ {username_msg}")
                else:
                    valid_password, password_msg = Validators.validate_password(password)
                    if not valid_password:
                        st.error(f"⚠️ {password_msg}")
                    else:
                        success, message = Auth.register(username, email, password, role)
                        
                        if success:
                            st.success("✅ Account created successfully!")
                            st.balloons()
                            st.info("✨ Please navigate to Login page to sign in")
                        else:
                            st.error(f"⚠️ {message}")
    
    # Info Box
    st.markdown(f"""
    <div class="info-box">
        <strong>{'✨ Creator Account' if role == settings.ROLE_CREATOR else '👀 Viewer Account'}</strong>
        {'Upload and manage educational videos, track engagement metrics, and contribute high-quality content to the platform.' if role == settings.ROLE_CREATOR else 'Watch educational videos, leave comments, track your learning progress, and interact with content creators.'}
    </div>
    """, unsafe_allow_html=True)
    
    # Password Requirements
    st.markdown("""
    <div class="info-box">
        <strong>🔐 Password Requirements</strong>
        • Minimum 8 characters<br>
        • At least one uppercase letter<br>
        • At least one lowercase letter<br>
        • Include numbers and special characters
    </div>
    """, unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Action Buttons
    btn_col1, btn_col2 = st.columns([1, 1], gap="medium")
    
    with btn_col1:
        if st.button("🔑 Login Instead", use_container_width=True, key="login_btn"):
            try:
                st.switch_page("pages/2_Login.py")
            except:
                st.info("👈 Please use the sidebar to navigate to the **Login** page")
    
    with btn_col2:
        if st.button("❓ Need Help?", use_container_width=True, key="help_btn"):
            st.markdown("""
            <div style="background: #f7fafc; border-radius: 12px; padding: 20px; margin-top: 16px; border: 2px solid #e2e8f0;">
                <h4 style="color: #2d3748; margin: 0 0 12px 0; font-size: 16px;">📞 Contact Support</h4>
                <p style="margin: 8px 0; color: #4a5568; font-size: 14px;">
                    📧 Email: <strong>support@mediahub.com</strong><br>
                    📱 Phone: <strong>+1 (555) 123-4567</strong><br>
                    ⏰ Hours: <strong>24/7 Support</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: white; opacity: 0.9; font-size: 14px; margin-top: 30px;">
    🔒 Secure Registration • Industry-Standard Encryption<br>
    © 2024 MediaHub. All rights reserved.
</div>
""", unsafe_allow_html=True)