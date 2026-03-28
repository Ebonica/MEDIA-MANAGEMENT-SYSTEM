import streamlit as st
from config.database import db

st.title("🗄️ Database Admin Tool")

database = db.get_db()

st.metric("Total Channels", database.channels.count_documents({}))
st.metric("Total Videos", database.videos.count_documents({}))

st.markdown("---")

st.subheader("📺 Channels")
for ch in database.channels.find():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"{ch['channel_name']} by {ch.get('creator_name')}")
    with col2:
        if st.button("Delete", key=f"del_ch_{ch['_id']}"):
            database.channels.delete_one({'_id': ch['_id']})
            st.rerun()

st.markdown("---")

st.subheader("🎬 Videos")
for v in database.videos.find():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"{v['title']}")
    with col2:
        if st.button("Delete", key=f"del_v_{v['_id']}"):
            database.videos.delete_one({'_id': v['_id']})
            st.rerun()

st.markdown("---")

if st.button("💣 DELETE ALL", type="primary"):
    database.channels.delete_many({})
    database.videos.delete_many({})
    st.success("All deleted!")
    st.rerun()