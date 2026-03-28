# ============================================================================
# COMPLETE ADMIN PANEL - admin_panel.py
# Save this and run: streamlit run admin_panel.py
# ============================================================================

import streamlit as st
from config.database import db
from datetime import datetime
from collections import defaultdict

st.set_page_config(page_title="Admin Panel", page_icon="🔧", layout="wide")

st.title("🔧 Database Admin Panel")
st.caption("Complete control over your database")

database = db.get_db()

# ============================================================================
# SIDEBAR - Quick Stats
# ============================================================================
with st.sidebar:
    st.markdown("### 📊 Database Stats")
    
    total_users = database.users.count_documents({})
    total_channels = database.channels.count_documents({})
    total_videos = database.videos.count_documents({})
    total_playlists = database.playlists.count_documents({})
    total_comments = database.comments.count_documents({})
    
    st.metric("👥 Users", total_users)
    st.metric("📺 Channels", total_channels)
    st.metric("🎬 Videos", total_videos)
    st.metric("📋 Playlists", total_playlists)
    st.metric("💬 Comments", total_comments)
    
    st.markdown("---")
    
    if st.button("🔄 Refresh Stats", use_container_width=True):
        st.rerun()

# ============================================================================
# MAIN TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["🗑️ Clean Duplicates", "👀 View Data", "💣 Delete All", "📊 Analytics"])

# ============================================================================
# TAB 1: Clean Duplicates
# ============================================================================
with tab1:
    st.header("🧹 Clean Duplicate Entries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📺 Channels")
        
        channels = list(database.channels.find())
        seen = defaultdict(list)
        
        for ch in channels:
            key = (ch['channel_name'].lower(), ch['creator_id'])
            seen[key].append(ch)
        
        duplicates = {k: v for k, v in seen.items() if len(v) > 1}
        
        if duplicates:
            st.warning(f"⚠️ Found {len(duplicates)} duplicate channel groups")
            
            for key, chs in duplicates.items():
                with st.expander(f"📺 {chs[0]['channel_name']} - {len(chs)} copies"):
                    for idx, ch in enumerate(chs):
                        created = ch.get('created_at', 'Unknown')
                        if isinstance(created, datetime):
                            created = created.strftime('%Y-%m-%d %H:%M:%S')
                        
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            label = "✓ OLDEST (Keep)" if idx == 0 else f"✗ Duplicate {idx}"
                            st.caption(f"{label} - Created: {created}")
                        with col_b:
                            if idx > 0:
                                if st.button("Delete", key=f"del_ch_{ch['_id']}"):
                                    database.channels.delete_one({'_id': ch['_id']})
                                    st.success("Deleted!")
                                    st.rerun()
            
            st.markdown("---")
            
            if st.button("🧹 Auto-Clean All Channel Duplicates", type="primary"):
                deleted = 0
                for key, chs in duplicates.items():
                    chs.sort(key=lambda x: x.get('created_at', datetime.now()))
                    for ch in chs[1:]:
                        database.channels.delete_one({'_id': ch['_id']})
                        deleted += 1
                
                st.success(f"✅ Deleted {deleted} duplicate channels!")
                st.balloons()
                st.rerun()
        else:
            st.success("✅ No duplicate channels found!")
    
    with col2:
        st.subheader("🎬 Videos")
        
        videos = list(database.videos.find())
        seen = defaultdict(list)
        
        for v in videos:
            key = (v['title'].lower(), v['creator_id'], v.get('created_at', ''))
            seen[key].append(v)
        
        duplicates = {k: v for k, v in seen.items() if len(v) > 1}
        
        if duplicates:
            st.warning(f"⚠️ Found {len(duplicates)} duplicate video groups")
            
            for key, vids in duplicates.items():
                with st.expander(f"🎬 {vids[0]['title']} - {len(vids)} copies"):
                    for idx, v in enumerate(vids):
                        created = v.get('created_at', 'Unknown')
                        if isinstance(created, datetime):
                            created = created.strftime('%Y-%m-%d %H:%M:%S')
                        
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            label = "✓ OLDEST (Keep)" if idx == 0 else f"✗ Duplicate {idx}"
                            st.caption(f"{label} - Created: {created}")
                        with col_b:
                            if idx > 0:
                                if st.button("Delete", key=f"del_v_{v['_id']}"):
                                    database.videos.delete_one({'_id': v['_id']})
                                    st.success("Deleted!")
                                    st.rerun()
            
            st.markdown("---")
            
            if st.button("🧹 Auto-Clean All Video Duplicates", type="primary"):
                deleted = 0
                for key, vids in duplicates.items():
                    vids.sort(key=lambda x: x.get('created_at', datetime.now()))
                    for v in vids[1:]:
                        database.videos.delete_one({'_id': v['_id']})
                        deleted += 1
                
                st.success(f"✅ Deleted {deleted} duplicate videos!")
                st.balloons()
                st.rerun()
        else:
            st.success("✅ No duplicate videos found!")
    
    st.markdown("---")
    
    st.subheader("💬 Comments")
    
    comments = list(database.comments.find())
    seen = defaultdict(list)
    
    for c in comments:
        key = (c['text'], c['user_id'], c['video_id'], c.get('parent_id', 'root'))
        seen[key].append(c)
    
    duplicates = {k: v for k, v in seen.items() if len(v) > 1}
    
    if duplicates:
        st.warning(f"⚠️ Found {len(duplicates)} duplicate comment groups ({sum(len(v)-1 for v in duplicates.values())} duplicates total)")
        
        if st.button("🧹 Auto-Clean All Comment Duplicates", type="primary"):
            deleted = 0
            for key, comms in duplicates.items():
                comms.sort(key=lambda x: x.get('created_at', datetime.now()))
                for c in comms[1:]:
                    database.comments.delete_one({'_id': c['_id']})
                    deleted += 1
            
            st.success(f"✅ Deleted {deleted} duplicate comments!")
            st.balloons()
            st.rerun()
    else:
        st.success("✅ No duplicate comments found!")

# ============================================================================
# TAB 2: View Data
# ============================================================================
with tab2:
    st.header("👀 View All Data")
    
    view_tab1, view_tab2, view_tab3, view_tab4 = st.tabs(["Channels", "Videos", "Comments", "Users"])
    
    with view_tab1:
        st.subheader("📺 All Channels")
        channels = list(database.channels.find())
        
        if channels:
            for ch in channels:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{ch['channel_name']}**")
                with col2:
                    st.caption(f"by {ch.get('creator_name', 'Unknown')}")
                with col3:
                    st.caption(f"👥 {ch.get('subscribers', 0)}")
        else:
            st.info("No channels")
    
    with view_tab2:
        st.subheader("🎬 All Videos")
        videos = list(database.videos.find())
        
        if videos:
            for v in videos:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{v['title']}**")
                    st.caption(f"by {v.get('creator_name', 'Unknown')}")
                with col2:
                    st.caption(f"👁️ {v.get('views', 0)}")
        else:
            st.info("No videos")
    
    with view_tab3:
        st.subheader("💬 All Comments")
        comments = list(database.comments.find())
        
        if comments:
            for c in comments:
                st.write(f"**{c['username']}:** {c['text'][:100]}")
                st.caption(f"👍 {c.get('likes', 0)} likes")
                st.markdown("---")
        else:
            st.info("No comments")
    
    with view_tab4:
        st.subheader("👥 All Users")
        users = list(database.users.find())
        
        if users:
            for u in users:
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"**{u['username']}**")
                with col2:
                    st.caption(u['email'])
                with col3:
                    st.caption(u['role'])
        else:
            st.info("No users")

# ============================================================================
# TAB 3: Delete All
# ============================================================================
with tab3:
    st.header("💣 Danger Zone")
    st.error("⚠️ WARNING: These actions cannot be undone!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Delete Collections")
        
        if st.button("🗑️ Delete All Channels", type="secondary", use_container_width=True):
            result = database.channels.delete_many({})
            st.success(f"Deleted {result.deleted_count} channels")
            st.rerun()
        
        if st.button("🗑️ Delete All Videos", type="secondary", use_container_width=True):
            result = database.videos.delete_many({})
            st.success(f"Deleted {result.deleted_count} videos")
            st.rerun()
        
        if st.button("🗑️ Delete All Comments", type="secondary", use_container_width=True):
            result = database.comments.delete_many({})
            st.success(f"Deleted {result.deleted_count} comments")
            st.rerun()
        
        if st.button("🗑️ Delete All Playlists", type="secondary", use_container_width=True):
            result = database.playlists.delete_many({})
            st.success(f"Deleted {result.deleted_count} playlists")
            st.rerun()
    
    with col2:
        st.subheader("Nuclear Option")
        st.markdown("---")
        
        confirm = st.checkbox("I understand this will delete EVERYTHING")
        
        if confirm:
            if st.button("💥 DELETE ALL DATA (EXCEPT USERS)", type="primary", use_container_width=True):
                ch = database.channels.delete_many({})
                v = database.videos.delete_many({})
                p = database.playlists.delete_many({})
                c = database.comments.delete_many({})
                
                st.success(f"""
                ✅ Deleted:
                - {ch.deleted_count} channels
                - {v.deleted_count} videos
                - {p.deleted_count} playlists
                - {c.deleted_count} comments
                """)
                st.balloons()
                st.rerun()

# ============================================================================
# TAB 4: Analytics
# ============================================================================
with tab4:
    st.header("📊 Database Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", total_users)
        creators = database.users.count_documents({"role": "Creator"})
        viewers = database.users.count_documents({"role": "Viewer"})
        admins = database.users.count_documents({"role": "Admin"})
        st.caption(f"Creators: {creators}")
        st.caption(f"Viewers: {viewers}")
        st.caption(f"Admins: {admins}")
    
    with col2:
        st.metric("Total Channels", total_channels)
        if total_channels > 0:
            pipeline = [{"$group": {"_id": None, "total": {"$sum": "$subscribers"}}}]
            result = list(database.channels.aggregate(pipeline))
            total_subs = result[0]['total'] if result else 0
            st.caption(f"Total Subscribers: {total_subs}")
    
    with col3:
        st.metric("Total Videos", total_videos)
        if total_videos > 0:
            pipeline = [{"$group": {"_id": None, "total": {"$sum": "$views"}}}]
            result = list(database.videos.aggregate(pipeline))
            total_views = result[0]['total'] if result else 0
            st.caption(f"Total Views: {total_views:,}")
    
    with col4:
        st.metric("Total Comments", total_comments)
        if total_comments > 0:
            pipeline = [{"$group": {"_id": None, "total": {"$sum": "$likes"}}}]
            result = list(database.comments.aggregate(pipeline))
            total_likes = result[0]['total'] if result else 0
            st.caption(f"Total Comment Likes: {total_likes}")

st.markdown("---")
st.caption("🔧 Database Admin Panel v1.0 | Built with Streamlit")