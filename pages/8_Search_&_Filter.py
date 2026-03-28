# ======================================================================
# FILE: pages/8_Search_&_Filter.py  (clean UI, no ghost placeholders)
# ======================================================================
import streamlit as st
from utils.auth import Auth
from models.video import VideoModel
from models.channel import ChannelModel
from utils.helpers import Helpers
from config.settings import settings
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Search & Filter - MediaHub",
    page_icon="🔍",
    layout="wide",
)

from utils.ui import sidebar_v2

# Sidebar
with st.sidebar:
    sidebar_v2()

Auth.require_auth()

user = Auth.get_current_user()
video_model = VideoModel()
channel_model = ChannelModel()

# Session state
if "search_performed" not in st.session_state:
    st.session_state.search_performed = False

# ======================================================================
# MAIN STYLING
# ======================================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header {
    display: none !important;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Main container – spacing only, NO white background */
.block-container {
    padding: 2rem 1rem !important;
    max-width: 1400px !important;
}

/* Search + Results wrapper – transparent (no white bars) */
.search-container,
.results-container {
    background: transparent !important;
    border-radius: 0 !important;
    border: none !important;
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: none !important;
}

/* Section headers */
.section-header {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin: 24px 0 16px 0;
    padding-bottom: 12px;
    border-bottom: 3px solid #ffffff55;
}

/* Page title inside sections */
.page-title {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 12px 0;
}

/* Expander Styling */
.streamlit-expanderHeader {
    background: #ffffff10 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    font-weight: 600 !important;
    color: #ffffff !important;
    border: 1px solid #ffffff33 !important;
}

.streamlit-expanderHeader:hover {
    background: #ffffff20 !important;
    border-color: #ffffff55 !important;
}

.streamlit-expanderContent {
    background: transparent !important;
    border: none !important;
    color: #ffffff !important;
}

/* Inputs – light background, BLACK text */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input,
.stMultiSelect > div > div {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    background: #f8fafc !important;
    color: #000000 !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #555 !important;
}

.stSelectbox > div > div > div {
    color: #000000 !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus,
.stMultiSelect > div > div:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    background: #ffffff !important;
    color: #000000 !important;
}

/* Labels */
.stTextInput > label,
.stTextArea > label,
.stSelectbox > label,
.stNumberInput > label,
.stMultiSelect > label {
    font-weight: 600 !important;
    color: #ffffff !important;
    font-size: 14px !important;
    margin-bottom: 5px !important;
}

/* Remove duplicate spacing for collapsed label search box */
.stTextInput > label[data-testid="stWidgetLabel"] {
    display: none;
}
.stTextInput > div {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Buttons */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 12px 30px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4) !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 22px rgba(102, 126, 234, 0.55) !important;
}

/* ✅ White cards for video & channel results */
.video-card,
.channel-card {
    background: #ffffff !important;
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 16px;
    border: 2px solid #e2e8f0;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
    transition: all 0.2s ease;
    color: #1a202c !important;
}

.video-card:hover,
.channel-card:hover {
    border-color: #667eea;
    box-shadow: 0 8px 22px rgba(102, 126, 234, 0.25);
    transform: translateY(-2px);
}

/* Image inside card */
.video-thumb {
    width: 100%;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Text inside video card */
.video-title {
    margin: 4px 0 4px 0;
    font-size: 16px;
    font-weight: 700;
}

.video-meta {
    margin: 0 0 6px 0;
    font-size: 13px;
    color: #4a5568;
}

.video-stats {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #4a5568;
    margin-bottom: 6px;
    gap: 6px;
    flex-wrap: wrap;
}

.video-desc {
    font-size: 13px;
    color: #4a5568;
    margin-top: 4px;
}

/* Caption text */
.stCaption {
    color: #718096 !important;
    font-size: 13px !important;
}

/* Images */
.stImage > img {
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

/* Columns */
div[data-testid="column"] {
    padding: 0 8px;
}

/* Divider */
hr {
    margin: 24px 0;
    border: none;
    border-top: 2px solid #e2e8f0;
}

/* Filter badge chips */
.filter-badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 4px 4px 4px 0;
}

/* Info/Warning/Success/Error boxes */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 12px !important;
    padding: 16px 20px !important;
    margin: 12px 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* Tips card – no white block */
.tips-card {
    background: transparent !important;
    border-radius: 0;
    padding: 0;
    box-shadow: none !important;
    border-left: none;
    margin-top: 18px;
    color: #ffffff !important;
}

/* Responsive */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.5rem !important;
    }
    .search-container, .results-container {
        padding: 16px !important;
    }
    .page-title {
        font-size: 26px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# ======================================================================
# SEARCH SECTION
# ======================================================================
st.markdown('<div class="search-container">', unsafe_allow_html=True)

st.markdown('<h2 class="page-title">🔎 Search</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input(
        "Search",
        placeholder="What are you looking for?",
        label_visibility="collapsed",
        key="main_search",
    )

with col2:
    search_type = st.selectbox(
        "Search Type", ["Videos", "Channels", "Both"], label_visibility="collapsed"
    )

# Advanced filters
with st.expander("🎛️ Advanced Filters", expanded=False):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📁 Content Filters**")
        category_filter = st.multiselect("Category", settings.VIDEO_CATEGORIES)
        sort_by = st.selectbox(
            "Sort by", ["Most Recent", "Most Viewed", "Most Liked", "Oldest"]
        )

    with col2:
        st.markdown("**📅 Time Filters**")
        date_filter = st.selectbox(
            "Upload Date",
            ["Any Time", "Today", "This Week", "This Month", "This Year"],
        )
        min_views = st.number_input(
            "Minimum Views", min_value=0, value=0, step=100
        )

    with col3:
        st.markdown("**👤 Creator Filters**")
        creator_filter = st.text_input(
            "Creator Name", placeholder="Filter by creator"
        )
        min_likes = st.number_input(
            "Minimum Likes", min_value=0, value=0, step=10
        )

# Search button
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    search_button = st.button(
        "🔍 Search Now", type="primary", use_container_width=True
    )

st.markdown("</div>", unsafe_allow_html=True)

if search_button:
    st.session_state.search_performed = True
    st.session_state.search_query = search_query
    st.session_state.search_type = search_type
    st.session_state.filters = {
        "category": category_filter,
        "sort_by": sort_by,
        "date_filter": date_filter,
        "min_views": min_views,
        "min_likes": min_likes,
        "creator_filter": creator_filter,
    }

st.markdown("---")

# ======================================================================
# RESULTS SECTION
# ======================================================================
if st.session_state.get("search_performed", False):
    query = st.session_state.get("search_query", "")
    search_type = st.session_state.get("search_type", "Videos")
    filters = st.session_state.get("filters", {})

    st.markdown('<div class="results-container">', unsafe_allow_html=True)

    # Active filters display
    if any(
        [
            filters.get("category"),
            filters.get("min_views"),
            filters.get("min_likes"),
            filters.get("creator_filter"),
            filters.get("date_filter") != "Any Time",
        ]
    ):
        st.markdown("**🏷️ Active Filters:**")
        filter_display = ""
        if filters.get("category"):
            filter_display += (
                f"<span class='filter-badge'>📁 {', '.join(filters['category'])}</span>"
            )
        if filters.get("date_filter") and filters["date_filter"] != "Any Time":
            filter_display += (
                f"<span class='filter-badge'>📅 {filters['date_filter']}</span>"
            )
        if filters.get("min_views") and filters["min_views"] > 0:
            filter_display += (
                f"<span class='filter-badge'>👁️ Min Views: {filters['min_views']}</span>"
            )
        if filters.get("min_likes") and filters["min_likes"] > 0:
            filter_display += (
                f"<span class='filter-badge'>👍 Min Likes: {filters['min_likes']}</span>"
            )
        if filters.get("creator_filter"):
            filter_display += (
                f"<span class='filter-badge'>👤 Creator: {filters['creator_filter']}</span>"
            )
        st.markdown(filter_display, unsafe_allow_html=True)
        st.markdown("---")

    # ===================== VIDEO RESULTS =====================
    if search_type in ["Videos", "Both"]:
        st.markdown(
            '<h3 class="section-header">🎥 Video Results</h3>',
            unsafe_allow_html=True,
        )

        mongo_filters = {}

        if filters.get("category"):
            mongo_filters["category"] = {"$in": filters["category"]}

        if filters.get("min_views"):
            mongo_filters["views"] = {"$gte": filters["min_views"]}

        if filters.get("min_likes"):
            mongo_filters["likes"] = {"$gte": filters["min_likes"]}

        if filters.get("creator_filter"):
            mongo_filters["creator_name"] = {
                "$regex": filters["creator_filter"],
                "$options": "i",
            }

        # Date filter
        if filters.get("date_filter") and filters["date_filter"] != "Any Time":
            now = datetime.now()
            if filters["date_filter"] == "Today":
                start_date = now.replace(hour=0, minute=0, second=0)
            elif filters["date_filter"] == "This Week":
                start_date = now - timedelta(days=7)
            elif filters["date_filter"] == "This Month":
                start_date = now - timedelta(days=30)
            elif filters["date_filter"] == "This Year":
                start_date = now - timedelta(days=365)
            else:
                start_date = None

            if start_date is not None:
                mongo_filters["created_at"] = {"$gte": start_date}

        # Perform search
        if query:
            videos = video_model.search(query, mongo_filters)
        else:
            from config.database import db

            database = db.get_db()
            videos = list(database.videos.find(mongo_filters))

        # Sort results
        if filters.get("sort_by") == "Most Viewed":
            videos = sorted(videos, key=lambda x: x.get("views", 0), reverse=True)
        elif filters.get("sort_by") == "Most Liked":
            videos = sorted(videos, key=lambda x: x.get("likes", 0), reverse=True)
        elif filters.get("sort_by") == "Oldest":
            videos = sorted(videos, key=lambda x: x.get("created_at", datetime.now()))
        else:  # Most Recent
            videos = sorted(
                videos,
                key=lambda x: x.get("created_at", datetime.now()),
                reverse=True,
            )

        # Display results – full white cards
        if videos:
            st.success(f"✅ Found {len(videos)} video(s)")

            for video in videos:
                thumbnail = video.get(
                    "thumbnail",
                    "https://via.placeholder.com/300x200",
                )
                title = video.get("title", "Untitled")
                creator = video.get("creator_name", "Unknown")
                category = video.get("category", "N/A")
                views = Helpers.format_number(video.get("views", 0))
                likes = Helpers.format_number(video.get("likes", 0))
                created_ago = Helpers.time_ago(video.get("created_at"))

                # Tags
                tags_html = ""
                if video.get("tags"):
                    tags_html = " ".join(
                        [
                            f"<span class='filter-badge'>🏷️ {tag}</span>"
                            for tag in video["tags"][:5]
                        ]
                    )

                # Description (short)
                desc_html = ""
                if video.get("description"):
                    desc = (
                        video["description"][:150] + "..."
                        if len(video["description"]) > 150
                        else video["description"]
                    )
                    desc_html = f"<p class='video-desc'>{desc}</p>"

                card_html = f"""
                <div class="video-card">
                    <img src="{thumbnail}" class="video-thumb" />
                    <h3 class="video-title">🎬 {title}</h3>
                    <p class="video-meta">
                        👤 by <strong>{creator}</strong> •
                        📁 Category: <strong>{category}</strong>
                    </p>
                    <div class="video-stats">
                        <span>👁️ <strong>{views}</strong> views</span>
                        <span>👍 <strong>{likes}</strong> likes</span>
                        <span>📅 {created_ago}</span>
                    </div>
                    {tags_html}
                    {desc_html}
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info(
                "🔭 No videos found matching your criteria. Try adjusting your filters!"
            )

    # ===================== CHANNEL RESULTS =====================
    if search_type in ["Channels", "Both"]:
        st.markdown(
            '<h3 class="section-header">📺 Channel Results</h3>',
            unsafe_allow_html=True,
        )

        if query:
            from config.database import db

            database = db.get_db()
            channels = list(
                database.channels.find(
                    {
                        "$or": [
                            {"channel_name": {"$regex": query, "$options": "i"}},
                            {"description": {"$regex": query, "$options": "i"}},
                            {"creator_name": {"$regex": query, "$options": "i"}},
                        ]
                    }
                )
            )
        else:
            channels = channel_model.get_all()

        if channels:
            st.success(f"✅ Found {len(channels)} channel(s)")

            cols = st.columns(3)
            for idx, channel in enumerate(channels):
                with cols[idx % 3]:
                    st.markdown(
                        f"""
                        <div class="channel-card">
                            <h3 style="margin: 0 0 8px 0; color: #1a202c;">
                                📺 {channel['channel_name']}
                            </h3>
                            <p style="color: #718096; font-size: 14px; margin-bottom: 12px;">
                                {channel.get('description', 'No description')[:100]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.caption(f"👤 by **{channel['creator_name']}**")
                    st.metric(
                        "Subscribers",
                        Helpers.format_number(channel.get("subscribers", 0)),
                    )
        else:
            st.info("🔭 No channels found matching your criteria")

    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ==================================================================
    # DEFAULT VIEW – TRENDING VIDEOS
    # ==================================================================
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown(
        '<h2 class="page-title">🔥 Trending Videos</h2>',
        unsafe_allow_html=True,
    )

    popular_videos = video_model.get_top_videos("views", 6)

    if popular_videos:
        cols = st.columns(3)
        for idx, video in enumerate(popular_videos):
            with cols[idx % 3]:
                thumbnail = video.get(
                    "thumbnail",
                    "https://via.placeholder.com/300x200?text=No+Thumbnail",
                )
                title = video.get("title", "Untitled")
                creator = video.get("creator_name", "Unknown")
                views = Helpers.format_number(video.get("views", 0))
                likes = Helpers.format_number(video.get("likes", 0))

                card_html = f"""
                <div class="video-card">
                    <img src="{thumbnail}" class="video-thumb" />
                    <h3 class="video-title">🎬 {title}</h3>
                    <p class="video-meta">👤 {creator}</p>
                    <div class="video-stats">
                        <span>👁️ {views} views</span>
                        <span>👍 {likes} likes</span>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
    else:
        st.info("🔭 No popular content available yet")

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================================
# TIPS SECTION
# ======================================================================
st.markdown(
    """
<div class="tips-card">
    <h4 style="color: #ffffff; margin: 0 0 8px 0; font-size: 15px; font-weight: 700;">
       💡 Search Tips
    </h4>
    <ul style="margin: 0; padding-left: 18px; color: #edf2f7; font-size: 13px; line-height: 1.6;">
        <li>Use specific keywords for better results.</li>
        <li>Combine keywords with category filters to narrow down content.</li>
        <li>Filter by creator name to see videos from a specific channel.</li>
        <li>Use the sort option to quickly see the most recent or most popular content.</li>
    </ul>
</div>
""",
    unsafe_allow_html=True,
)
