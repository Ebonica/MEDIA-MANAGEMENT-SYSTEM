"""
EMERGENCY ONE-CLICK FIX SCRIPT
Save this as emergency_fix.py and run: python emergency_fix.py
"""

import os
import shutil

def emergency_fix():
    print("🚨 EMERGENCY FIX STARTING...\n")
    
    # Step 1: Backup existing pages
    print("Step 1: Backing up existing pages...")
    if os.path.exists('pages'):
        if os.path.exists('pages_backup'):
            shutil.rmtree('pages_backup')
        shutil.copytree('pages', 'pages_backup')
        print("✅ Backup created: pages_backup/\n")
    
    # Step 2: Clear pages directory
    print("Step 2: Clearing pages directory...")
    if os.path.exists('pages'):
        for file in os.listdir('pages'):
            if file.endswith('.py'):
                os.remove(os.path.join('pages', file))
        print("✅ Cleared old page files\n")
    else:
        os.makedirs('pages')
    
    # Step 3: Create simple working pages
    print("Step 3: Creating simple working pages...")
    
    pages = {
        'pages/1_Home.py': '''import streamlit as st
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
st.title("🏠 Home")
st.info("Navigate using the sidebar")
''',
        
        'pages/2_Login.py': '''import streamlit as st
from utils.auth import Auth

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login")

if Auth.is_authenticated():
    st.success("Already logged in!")
    st.stop()

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")
    
    if submit and username and password:
        user = Auth.login(username, password)
        if user:
            st.session_state.user = user
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

st.info("Demo: admin / admin123")
''',
        
        'pages/3_Register.py': '''import streamlit as st
from utils.auth import Auth
from utils.validators import Validators
from config.settings import settings

st.set_page_config(page_title="Register", layout="centered")
st.title("📝 Register")

if Auth.is_authenticated():
    st.warning("Already logged in!")
    st.stop()

with st.form("register_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", [settings.ROLE_VIEWER, settings.ROLE_CREATOR])
    submit = st.form_submit_button("Register")
    
    if submit:
        if username and email and password:
            if Validators.validate_email(email):
                success, msg = Auth.register(username, email, password, role)
                if success:
                    st.success("Registration successful! Go to Login.")
                else:
                    st.error(msg)
            else:
                st.error("Invalid email")
        else:
            st.error("Fill all fields")
''',
        
        'pages/4_Channels.py': '''import streamlit as st
from utils.auth import Auth
from models.channel import ChannelModel

st.set_page_config(page_title="Channels", layout="wide")
Auth.require_auth()

st.title("📺 Channels")
user = Auth.get_current_user()
channel_model = ChannelModel()

if user['role'] in ['Creator', 'Admin']:
    with st.form("create_channel"):
        name = st.text_input("Channel Name")
        submit = st.form_submit_button("Create")
        if submit and name:
            channel_model.create({
                'channel_name': name,
                'description': '',
                'category': 'General',
                'creator_id': str(user['_id']),
                'creator_name': user['username']
            })
            st.success("Channel created!")
            st.rerun()
    
    channels = channel_model.get_by_creator(str(user['_id']))
    for ch in channels:
        st.write(f"📺 {ch['channel_name']}")
else:
    st.warning("Only Creators can create channels")
''',
        
        'pages/5_Videos.py': '''import streamlit as st
from utils.auth import Auth
from models.video import VideoModel

st.set_page_config(page_title="Videos", layout="wide")
Auth.require_auth()

st.title("🎥 Videos")
user = Auth.get_current_user()
video_model = VideoModel()

videos = video_model.get_all(limit=10)
for video in videos:
    st.write(f"**{video['title']}**")
    st.caption(f"Views: {video.get('views', 0)}")
    st.write("---")

if not videos:
    st.info("No videos yet")
'''
    }
    
    for filepath, content in pages.items():
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {filepath}")
    
    print("\n" + "="*60)
    print("✅ EMERGENCY FIX COMPLETED!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run: streamlit run app.py")
    print("2. Login with: admin / admin123")
    print("3. Navigate pages using sidebar")
    print("\nIf you see errors, check:")
    print("- MongoDB is running")
    print("- All dependencies installed")
    print("\nYour old pages are backed up in: pages_backup/")

if __name__ == "__main__":
    try:
        emergency_fix()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTry manually:")
        print("1. Delete all files in pages/ folder")
        print("2. Copy the simple page files from the artifact")
        print("3. Save them as 1_Home.py, 2_Login.py, etc.")