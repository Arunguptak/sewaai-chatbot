import streamlit as st
import feedparser
from urllib.parse import quote
from datetime import datetime
from html import escape

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SewaAI | AI News Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.html("""
<style>

/* ---------------------------------------------------------
   GLOBAL
--------------------------------------------------------- */

.stApp {
    background: linear-gradient(
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

/* Remove Streamlit default spacing */

div[data-testid="stVerticalBlock"] {
    gap: 0.7rem;
}

/* ---------------------------------------------------------
   HEADER
--------------------------------------------------------- */

.sewa-header {
    background: linear-gradient(
        135deg,
        #111827,
        #1e3a8a
    );

    padding: 22px 24px;
    border-radius: 20px;

    color: white;

    box-shadow:
        0 10px 30px rgba(30, 58, 138, 0.20);

    margin-bottom: 20px;
}

.sewa-brand {
    display: flex;
    align-items: center;
    gap: 13px;
}

.sewa-logo {
    width: 52px;
    height: 52px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: rgba(255,255,255,0.14);

    border: 1px solid rgba(255,255,255,0.20);

    border-radius: 15px;

    font-size: 28px;
}

.sewa-name {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.sewa-status {
    font-size: 12px;
    margin-top: 3px;
    opacity: 0.85;
}

.status-dot {
    display: inline-block;

    width: 8px;
    height: 8px;

    background: #22c55e;

    border-radius: 50%;

    margin-right: 6px;
}

.sewa-description {
    margin-top: 14px;

    font-size: 14px;

    line-height: 1.5;

    color: rgba(255,255,255,0.82);
}

/* ---------------------------------------------------------
   CHAT USER MESSAGE
--------------------------------------------------------- */

.user-message {
    background: #1d4ed8;

    color: white;

    padding: 12px 16px;

    border-radius: 18px 18px 5px 18px;

    margin: 8px 0 14px auto;

    max-width: 82%;

    font-size: 15px;

    line-height: 1.5;

    box-shadow:
        0 5px 15px rgba(29,78,216,0.15);
}

/* ---------------------------------------------------------
   AI MESSAGE
--------------------------------------------------------- */

.ai-message {
    background: white;

    color: #111827;

    padding: 14px 17px;

    border-radius: 18px 18px 18px 5px;

    margin: 8px auto 16px 0;

    max-width: 88%;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.05);

    font-size: 14px;
}

/* ---------------------------------------------------------
   AI LABEL
--------------------------------------------------------- */

.ai-label {
    font-size: 12px;

    color: #1d4ed8;

    font-weight: 700;

    margin-bottom: 7px;
}

/* ---------------------------------------------------------
   NEWS CARD
--------------------------------------------------------- */

.news-card {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 16px;

    padding: 16px;

    margin: 10px 0;

    transition: all 0.2s ease;

    box-shadow:
        0 4px 15px rgba(15,23,42,0.04);
}

.news-card:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 25px rgba(15,23,42,0.08);

    border-color: #bfdbfe;
}

.news-number {
    display: inline-flex;

    width: 28px;
    height: 28px;

    align-items: center;
    justify-content: center;

    background: #eff6ff;

    color: #1d4ed8;

    border-radius: 8px;

    font-size: 12px;

    font-weight: 700;

    margin-right: 8px;
}

.news-title {
    display: inline;

    font-size: 16px;

    font-weight: 700;

    color: #111827;

    line-height: 1.4;
}

.news-meta {
    margin-top: 9px;

    font-size: 12px;

    color: #6b7280;
}

.news-source {
    color: #1d4ed8;

    font-weight: 600;
}

.read-button {
    display: inline-block;

    margin-top: 12px;

    padding: 7px 12px;

    border-radius: 8px;

    background: #eff6ff;

    color: #1d4ed8 !important;

    text-decoration: none !important;

    font-size: 12px;

    font-weight: 700;
}

.read-button:hover {
    background: #dbeafe;
}

/* ---------------------------------------------------------
   WELCOME CARD
--------------------------------------------------------- */

.welcome-card {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 20px;

    padding: 24px;

    text-align: center;

    margin: 25px 0;

    box-shadow:
        0 8px 30px rgba(15,23,42,0.05);
}

.welcome-icon {
    font-size: 42px;

    margin-bottom: 5px;
}

.welcome-title {
    font-size: 22px;

    font-weight: 800;

    color: #111827;
}

.welcome-text {
    color: #6b7280;

    font-size: 14px;

    margin-top: 7px;
}

/* ---------------------------------------------------------
   SECTION TITLE
--------------------------------------------------------- */

.section-title {
    font-size: 14px;

    font-weight: 700;

    color: #374151;

    margin: 18px 0 8px;
}

/* ---------------------------------------------------------
   STREAMLIT BUTTONS
--------------------------------------------------------- */

.stButton > button {
    border-radius: 10px;

    border: 1px solid #dbe3ef;

    background: white;

    color: #374151;

    font-size: 13px;

    font-weight: 600;

    min-height: 40px;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #93c5fd;

    color: #1d4ed8;

    background: #eff6ff;
}

/* ---------------------------------------------------------
   CHAT INPUT
--------------------------------------------------------- */

.stChatInput {
    border-radius: 16px !important;
}

/* ---------------------------------------------------------
   MOBILE
--------------------------------------------------------- */

@media (max-width: 600px) {

    .block-container {
        padding: 10px 12px 100px;
    }

    .sewa-header {
        padding: 18px;
        border-radius: 16px;
    }

    .sewa-name {
        font-size: 24px;
    }

    .sewa-logo {
        width: 45px;
        height: 45px;
        font-size: 23px;
    }

    .user-message {
        max-width: 90%;
    }

    .ai-message {
        max-width: 94%;
    }

    .news-card {
        padding: 13px;
    }

    .news-title {
        font-size: 14px;
    }
}

</style>
""")


# ============================================================
# HEADER
# ============================================================

st.html("""
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
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 SewaAI")

    st.markdown("### Quick Topics")

    if st.button("🤖 AI News", use_container_width=True):
        st.session_state.quick_question = "Latest AI news"

    if st.button("## 🇮🇳 India Technology", use_container_width=True):
        st.session_state.quick_question = "Latest technology news in India"

    if st.button("💻 Technology News", use_container_width=True):
        st.session_state.quick_question = "Latest technology news"

    if st.button("🧠 OpenAI News", use_container_width=True):
        st.session_state.quick_question = "Latest OpenAI news"

    if st.button("🔵 Google AI News", use_container_width=True):
        st.session_state.quick_question = "Latest Google AI news"

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# NEWS FUNCTION
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
# QUESTION PROCESSING
# ============================================================

def answer_question(question):

    question_lower = question.lower()

    if "openai" in question_lower:
        search_query = "OpenAI"

    elif "chatgpt" in question_lower:
        search_query = "ChatGPT OpenAI"

    elif "google" in question_lower:
        search_query = "Google AI"

    elif "microsoft" in question_lower:
        search_query = "Microsoft AI"

    elif "india" in question_lower:
        search_query = "India AI technology"

    elif "technology" in question_lower:
        search_query = "technology"

    elif "ai" in question_lower:
        search_query = "artificial intelligence"

    else:
        search_query = question

    return get_news(search_query, 10)


# ============================================================
# WELCOME SCREEN
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_question" not in st.session_state:
    st.session_state.quick_question = None


if len(st.session_state.messages) == 0:

    st.html("""
    <div class="welcome-card">

        <div class="welcome-icon">
            🤖
        </div>

        <div class="welcome-title">
            Welcome to SewaAI
        </div>

        <div class="welcome-text">
            Your intelligent news assistant.
            Ask me about AI, technology,
            India and the latest news.
        </div>

    </div>
    """)

    st.html(
        '<div class="section-title">Try asking</div>')

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🤖 Latest AI News",
            use_container_width=True
        ):
            st.session_state.quick_question = \
                "Latest AI news"

    with col2:

        if st.button(
            "🇮🇳 India AI News",
            use_container_width=True
        ):
            st.session_state.quick_question = \
                "Latest AI news in India"


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.html(
            f"""
            <div class="user-message">
                {escape(str(message["content"]))}
            </div>
            """)

    else:

        st.html(
            """
            <div class="ai-message">

                <div class="ai-label">
                    🤖 SewaAI
                </div>

                Here are the latest news results:
            </div>
            """)

        for index, article in enumerate(
            message["articles"],
            start=1
        ):

            st.html(
                f"""
                <div class="news-card">

                    <div>
                        <span class="news-number">
                            {index}
                        </span>

                        <span class="news-title">
                            {escape(str(article['title']))}
                        </span>
                    </div>

                    <div class="news-meta">

                        <span class="news-source">
                            {escape(str(article['source']))}
                        </span>

                        &nbsp; • &nbsp;

                        {escape(str(article['published']))}

                    </div>

                    <a
                        href="{escape(str(article['link']), quote=True)}"
                        target="_blank"
                        class="read-button"
                    >
                        🔗 Read Full Article →
                    </a>

                </div>
                """)


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.chat_input(
    "Ask SewaAI about the latest news..."
)


# ============================================================
# QUICK QUESTION
# ============================================================

if st.session_state.quick_question:
    question = st.session_state.quick_question
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

    st.html(
        f"""
        <div class="user-message">
            {escape(str(question))}
        </div>
        """)

    # --------------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------------

    with st.spinner(
        "🔎 SewaAI is searching live news..."
    ):

        try:

            articles = answer_question(question)

            if not articles:

                st.warning(
                    "No news articles found. "
                    "Try another question."
                )

                articles = []

            else:

                st.html(
                    f"""
                    <div class="ai-message">

                        <div class="ai-label">
                            🤖 SewaAI
                        </div>

                        Found
                        <strong>{len(articles)}</strong>
                        latest news articles for you.
                    </div>
                    """)

                for index, article in enumerate(
                    articles,
                    start=1
                ):

                    st.html(
                        f"""
                        <div class="news-card">

                            <div>

                                <span class="news-number">
                                    {index}
                                </span>

                                <span class="news-title">
                                    {escape(str(article['title']))}
                                </span>

                            </div>

                            <div class="news-meta">

                                <span class="news-source">
                                    {escape(str(article['source']))}
                                </span>

                                &nbsp; • &nbsp;

                                {escape(str(article['published']))}

                            </div>

                            <a
                                href="{escape(str(article['link']), quote=True)}"
                                target="_blank"
                                class="read-button"
                            >
                                🔗 Read Full Article →
                            </a>

                        </div>
                        """)

            # ------------------------------------------------
            # SAVE RESPONSE
            # ------------------------------------------------

            st.session_state.messages.append({
                "role": "assistant",
                "articles": articles
            })

        except Exception as e:

            st.error(
                f"⚠️ Unable to fetch news: {e}"
            )
