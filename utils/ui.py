import streamlit as st
from utils.auth import Auth
from config.database import db

def sidebar_v2():
    """Shared sidebar with clean white text and refined typography."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        /* Base sidebar style */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0e1f33 0%, #143a5d 100%) !important;
            color: #ffffff !important;
            font-family: 'Poppins', sans-serif !important;
            padding: 20px 16px !important;
        }

        /* Force all text to pure white with maximum specificity */
        [data-testid="stSidebar"] *,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] strong,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stMarkdown * {
            color: #ffffff !important;
        }

        /* Brand styling */
        .sb-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 16px;
        }
        .sb-brand .logo {
            width: 48px; height: 48px;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            background: linear-gradient(135deg,#3b82f6,#7c3aed);
            font-weight: 700; font-size: 20px; color: white;
        }
        .sb-brand .title {
            font-weight: 700; font-size: 17px; line-height: 1.2;
            color: #ffffff !important;
        }
        .sb-brand .tag {
            font-size: 13px; opacity: 0.85;
            color: #ffffff !important;
        }

        /* Guest/User info */
        .user-box {
            background: rgba(255,255,255,0.06);
            border-radius: 10px;
            padding: 10px;
            text-align: center;
            margin-bottom: 16px;
        }
        .user-box div {
            margin: 2px 0;
            color: #ffffff !important;
        }

        /* Navigation heading */
        .nav-heading {
            font-weight: 700;
            font-size: 15px;
            margin-bottom: 8px;
            opacity: 0.95;
            color: #ffffff !important;
        }

        /* Navigation info */
        .nav-info {
            background: rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 14px 16px;
            font-size: 14px;
            line-height: 1.6;
            box-shadow: 0 4px 10px rgba(0,0,0,0.25);
            margin-bottom: 18px;
            color: #ffffff !important;
        }
        .nav-info strong {
            font-weight: 600;
            color: #ffffff !important;
        }

        /* Stat boxes */
        .sb-stat {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 10px 14px;
            margin: 6px 0;
            font-size: 14px;
            font-weight: 500;
            color: #ffffff !important;
        }
        .sb-stat div {
            color: #ffffff !important;
        }
        .sb-stat div:last-child {
            font-weight: 700;
            font-size: 16px;
            text-shadow: 0 0 4px rgba(255,255,255,0.8);
            color: #ffffff !important;
        }

        /* Footer */
        .sb-footer {
            text-align: center;
            font-size: 13px;
            margin-top: 18px;
            opacity: 0.9;
            color: #ffffff !important;
        }

        /* Buttons */
        /* === Blue Sign Out Button (Global Sidebar Style) === */
        .stButton>button,
        .stButton>button[kind],
        .stButton>button[data-testid] {
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            padding: 10px 14px !important;
            width: 100% !important;
            font-family: 'Poppins', sans-serif !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 14px rgba(66, 153, 225, 0.3) !important;
        }

        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(66, 153, 225, 0.5) !important;
        }
        
        /* Force caption text to white */
        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] .stCaption * {
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Brand Section ---
    st.markdown(
        """
        <div class="sb-brand">
            <div class="logo">MH</div>
            <div>
                <div class="title">MediaHub</div>
                <div class="tag">Content Management</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- User Block ---
    if Auth.is_authenticated():
        user = Auth.get_current_user()
        avatar = user['username'][0].upper()
        st.markdown(
            f"""
            <div class="user-box" style="display:flex;align-items:center;gap:10px;text-align:left;">
                <div style="width:44px;height:44px;border-radius:8px;background:linear-gradient(135deg,#60a5fa,#7c3aed);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:20px;color:#ffffff;">{avatar}</div>
                <div>
                    <div style="font-weight:600;font-size:15px;color:#ffffff;">{user['username']}</div>
                    <div style="font-size:12px;opacity:0.8;color:#ffffff;">{user['role']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🚪 Sign Out", key="logout", use_container_width=True):
            Auth.logout()
            st.rerun()
    else:
        st.markdown(
            """
            <div class="user-box">
                <div style="font-weight:600;font-size:15px;color:#ffffff;">Guest</div>
                <div style="font-size:12px;opacity:0.8;color:#ffffff;">Please sign in</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Navigation Info ---
    st.markdown(
        """
        <div class="nav-heading">📍 Navigation</div>
        <div class="nav-info">
            <strong>Use the page links above ☝️</strong><br><br>
            <strong>Available Pages:</strong><br>
            • Home - Main dashboard<br>
            • Login - Sign into your account<br>
            • Register - Create new account<br>
            • Channel Management - Manage channels<br>
            • Video Management - Upload videos<br>
            • Playlist Management - Create playlists<br>
            • Comment System - View comments<br>
            • Analytics Reports - View stats<br>
            • Search Filter - Find content<br>
            • Settings - Account settings
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Stats Section ---
    try:
        if st.session_state.get("db_connected", False):
            database = db.get_db()
            total_users = database.users.count_documents({})
            total_videos = database.videos.count_documents({})
            total_channels = database.channels.count_documents({})

            st.markdown(f'<div class="sb-stat"><div>👥 Users</div><div>{total_users}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sb-stat"><div>🎬 Videos</div><div>{total_videos}</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sb-stat"><div>📺 Channels</div><div>{total_channels}</div></div>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<div style="text-align:center;font-size:13px;color:#ffffff;opacity:0.8;">Stats unavailable</div>', unsafe_allow_html=True)

    # --- Footer ---
    st.markdown('<div class="sb-footer">© 2024 MediaHub • v1.0</div>', unsafe_allow_html=True)
