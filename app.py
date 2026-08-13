import streamlit as st
import feedparser
from urllib.parse import quote
import html

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SewaAI | Live News Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   GLOBAL
========================================================== */

.stApp {
    background:
        linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef4ff 50%,
            #f8fafc 100%
        );
}

.block-container {
    max-width: 950px;
    padding-top: 1.5rem;
    padding-bottom: 7rem;
}


/* ==========================================================
   HEADER
========================================================== */

.sewa-header {
    background:
        linear-gradient(
            135deg,
            #111827,
            #1e3a8a
        );

    padding: 24px;

    border-radius: 22px;

    color: white;

    box-shadow:
        0 12px 35px rgba(30, 58, 138, 0.20);

    margin-bottom: 22px;
}

.sewa-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.sewa-logo {
    width: 54px;
    height: 54px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: rgba(255,255,255,0.14);

    border:
        1px solid
        rgba(255,255,255,0.20);

    border-radius: 16px;

    font-size: 29px;
}

.sewa-name {
    font-size: 30px;

    font-weight: 800;

    letter-spacing: -0.5px;
}

.sewa-status {
    font-size: 12px;

    margin-top: 4px;

    opacity: 0.9;
}

.status-dot {
    display: inline-block;

    width: 8px;
    height: 8px;

    background: #22c55e;

    border-radius: 50%;

    margin-right: 6px;

    box-shadow:
        0 0 8px rgba(34,197,94,0.8);
}

.sewa-description {
    margin-top: 15px;

    font-size: 14px;

    line-height: 1.6;

    color:
        rgba(255,255,255,0.82);
}


/* ==========================================================
   WELCOME CARD
========================================================== */

.welcome-card {
    background: white;

    border:
        1px solid
        #e5e7eb;

    border-radius: 20px;

    padding: 26px;

    text-align: center;

    margin: 25px 0;

    box-shadow:
        0 8px 30px
        rgba(15,23,42,0.05);
}

.welcome-icon {
    font-size: 42px;
}

.welcome-title {
    margin-top: 6px;

    font-size: 23px;

    font-weight: 800;

    color: #111827;
}

.welcome-text {
    margin-top: 7px;

    color: #6b7280;

    font-size: 14px;

    line-height: 1.5;
}


/* ==========================================================
   USER MESSAGE
========================================================== */

.user-message {
    background:
        linear-gradient(
            135deg,
            #2563eb,
            #1d4ed8
        );

    color: white;

    padding: 13px 17px;

    border-radius:
        18px 18px 5px 18px;

    margin:
        10px 0
        14px auto;

    max-width: 82%;

    font-size: 15px;

    line-height: 1.5;

    box-shadow:
        0 6px 18px
        rgba(29,78,216,0.16);
}


/* ==========================================================
   AI MESSAGE
========================================================== */

.ai-message {
    background: white;

    color: #111827;

    padding: 15px 17px;

    border-radius:
        18px 18px 18px 5px;

    margin:
        8px auto
        16px 0;

    max-width: 90%;

    border:
        1px solid
        #e5e7eb;

    box-shadow:
        0 5px 20px
        rgba(15,23,42,0.05);

    font-size: 14px;
}

.ai-label {
    color: #1d4ed8;

    font-size: 12px;

    font-weight: 800;

    margin-bottom: 7px;
}


/* ==========================================================
   NEWS CARD
========================================================== */

.news-card {
    background: white;

    border:
        1px solid
        #e5e7eb;

    border-radius: 16px;

    padding: 16px;

    margin:
        10px 0;

    box-shadow:
        0 4px 15px
        rgba(15,23,42,0.04);

    transition:
        all 0.2s ease;
}

.news-card:hover {
    transform:
        translateY(-2px);

    border-color:
        #bfdbfe;

    box-shadow:
        0 9px 25px
        rgba(15,23,42,0.08);
}

.news-header {
    display: flex;

    align-items:
        flex-start;

    gap: 10px;
}

.news-number {
    min-width: 28px;

    height: 28px;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        #eff6ff;

    color:
        #1d4ed8;

    border-radius: 8px;

    font-size: 12px;

    font-weight: 800;
}

.news-title {
    font-size: 16px;

    font-weight: 700;

    color:
        #111827;

    line-height: 1.45;
}

.news-meta {
    margin-top: 10px;

    font-size: 12px;

    color:
        #6b7280;
}

.news-source {
    color:
        #1d4ed8;

    font-weight: 700;
}

.read-button {
    display: inline-block;

    margin-top: 12px;

    padding:
        7px 12px;

    border-radius: 8px;

    background:
        #eff6ff;

    color:
        #1d4ed8 !important;

    text-decoration:
        none !important;

    font-size: 12px;

    font-weight: 700;
}

.read-button:hover {
    background:
        #dbeafe;
}


/* ==========================================================
   QUICK QUESTIONS
========================================================== */

.quick-title {
    font-size: 14px;

    font-weight: 700;

    color: #374151;

    margin:
        18px 0 10px;
}


/* ==========================================================
   STREAMLIT BUTTONS
========================================================== */

.stButton > button {
    border-radius: 10px;

    border:
        1px solid
        #dbe3ef;

    background:
        white;

    color:
        #374151;

    font-size: 13px;

    font-weight: 600;

    min-height: 40px;

    transition:
        all 0.2s ease;
}

.stButton > button:hover {
    border-color:
        #93c5fd;

    color:
        #1d4ed8;

    background:
        #eff6ff;
}


/* ==========================================================
   SIDEBAR
========================================================== */

section[data-testid="stSidebar"] {
    background:
        #f8fafc;
}


/* ==========================================================
   MOBILE
========================================================== */

@media (max-width: 600px) {

    .block-container {
        padding:
            10px
            12px
            100px;
    }

    .sewa-header {
        padding: 18px;

        border-radius: 17px;
    }

    .sewa-name {
        font-size: 25px;
    }

    .sewa-logo {
        width: 46px;
        height: 46px;
        font-size: 24px;
    }

    .user-message {
        max-width: 92%;
    }

    .ai-message {
        max-width: 95%;
    }

    .news-card {
        padding: 13px;
    }

    .news-title {
        font-size: 14px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="sewa-header">

    <div class="sewa-brand">

        <div class="sewa-logo">
            🤖
        </div>

        <div>

            <div class="sewa-name">
                SewaAI
            </div>

            <div class="sewa-status">
                <span class="status-dot"></span>
                Live News Assistant
            </div>

        </div>

    </div>

    <div class="sewa-description">
        Ask questions and discover the latest AI,
        technology and India news from live news sources.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 SewaAI")

    st.caption(
        "Live AI & Technology News Assistant"
    )

    st.divider()

    st.markdown("### 🔎 Quick Topics")

    if st.button(
        "🤖 Latest AI News",
        use_container_width=True
    ):
        st.session_state.quick_question = \
            "Latest AI news"

    if st.button(
        "🇮🇳 India AI News",
        use_container_width=True
    ):
        st.session_state.quick_question = \
            "Latest AI news in India"

    if st.button(
        "💻 Technology News",
        use_container_width=True
    ):
        st.session_state.quick_question = \
            "Latest technology news"

    if st.button(
        "🧠 OpenAI News",
        use_container_width=True
    ):
        st.session_state.quick_question = \
            "Latest OpenAI news"

    if st.button(
        "🔵 Google AI News",
        use_container_width=True
    ):
        st.session_state.quick_question = \
            "Latest Google AI news"

    if st.button(
        "🏦 AI Banking News",
        use_container_width=True
    ):
        st.session_state.quick_question = \
            "Latest AI banking news"

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "Powered by Google News RSS + Streamlit"
    )


# ============================================================
# GOOGLE NEWS RSS
# ============================================================

@st.cache_data(ttl=300)
def get_news(query, limit=10):

    encoded_query = quote(query)

    rss_url = (
        "https://news.google.com/rss/search?"
        f"q={encoded_query}"
        "&hl=en-IN"
        "&gl=IN"
        "&ceid=IN:en"
    )

    feed = feedparser.parse(rss_url)

    articles = []

    for entry in feed.entries[:limit]:

        title = entry.get(
            "title",
            "No title"
        )

        link = entry.get(
            "link",
            ""
        )

        published = entry.get(
            "published",
            "Date unavailable"
        )

        source = "Google News"

        if hasattr(entry, "source"):

            source = entry.source.get(
                "title",
                "Google News"
            )

        articles.append({
            "title": title,
            "link": link,
            "published": published,
            "source": source
        })

    return articles


# ============================================================
# QUESTION → SEARCH QUERY
# ============================================================

def answer_question(question):

    question_lower = question.lower()

    if "openai" in question_lower:

        search_query = "OpenAI"

    elif "chatgpt" in question_lower:

        search_query = "ChatGPT OpenAI"

    elif "gemini" in question_lower:

        search_query = "Google Gemini AI"

    elif "google" in question_lower:

        search_query = "Google AI"

    elif "microsoft" in question_lower:

        search_query = "Microsoft AI"

    elif "bank" in question_lower:

        search_query = "AI banking"

    elif "india" in question_lower:

        search_query = "India AI technology"

    elif "technology" in question_lower:

        search_query = "technology"

    elif "business" in question_lower:

        search_query = "technology business"

    elif "startup" in question_lower:

        search_query = "AI startup"

    elif "ai" in question_lower:

        search_query = "artificial intelligence"

    else:

        search_query = question

    return get_news(
        search_query,
        10
    )


# ============================================================
# NEWS CARD
# ============================================================

def display_news(articles):

    for index, article in enumerate(
        articles,
        start=1
    ):

        title = html.escape(
            article["title"]
        )

        source = html.escape(
            article["source"]
        )

        published = html.escape(
            article["published"]
        )

        link = article["link"]

        st.markdown(
            f"""
            <div class="news-card">

                <div class="news-header">

                    <div class="news-number">
                        {index}
                    </div>

                    <div class="news-title">
                        {title}
                    </div>

                </div>

                <div class="news-meta">

                    <span class="news-source">
                        {source}
                    </span>

                    &nbsp; • &nbsp;

                    {published}

                </div>

                <a
                    href="{link}"
                    target="_blank"
                    class="read-button"
                >
                    🔗 Read Full Article →
                </a>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# WELCOME SCREEN
# ============================================================

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="welcome-card">

        <div class="welcome-icon">
            🤖
        </div>

        <div class="welcome-title">
            Welcome to SewaAI
        </div>

        <div class="welcome-text">
            Your intelligent live-news assistant.
            Ask me about AI, technology,
            India, startups, banking and more.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="quick-title">💡 Try asking</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🤖 Latest AI News",
            use_container_width=True
        ):

            st.session_state.quick_question = \
                "Latest AI news"

            st.rerun()

    with col2:

        if st.button(
            "🇮🇳 India AI News",
            use_container_width=True
        ):

            st.session_state.quick_question = \
                "Latest AI news in India"

            st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                {html.escape(message["content"])}
            </div>
            """,
            unsafe_allow_html=True
        )

    elif message["role"] == "assistant":

        st.markdown(
            """
            <div class="ai-message">

                <div class="ai-label">
                    🤖 SewaAI
                </div>

                Here are the latest news results:
                
            </div>
            """,
            unsafe_allow_html=True
        )

        if message["articles"]:

            display_news(
                message["articles"]
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask SewaAI about the latest news..."
)


# ============================================================
# QUICK QUESTION
# ============================================================

if st.session_state.quick_question:

    question = \
        st.session_state.quick_question

    st.session_state.quick_question = None


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    st.markdown(
        f"""
        <div class="user-message">
            {html.escape(question)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    with st.spinner(
        "🔎 SewaAI is searching live news..."
    ):

        try:

            articles = answer_question(
                question
            )

            if not articles:

                st.markdown(
                    """
                    <div class="ai-message">

                        <div class="ai-label">
                            🤖 SewaAI
                        </div>

                        Sorry, I couldn't find
                        relevant news articles.
                        Try another question.

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="ai-message">

                        <div class="ai-label">
                            🤖 SewaAI
                        </div>

                        Found
                        <strong>
                            {len(articles)}
                        </strong>
                        latest news articles.

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                display_news(
                    articles
                )

            # ------------------------------------------------
            # SAVE
            # ------------------------------------------------

            st.session_state.messages.append({
                "role": "assistant",
                "articles": articles
            })

        except Exception as e:

            st.error(
                "⚠️ Unable to fetch news. "
                f"Error: {e}"
            )
