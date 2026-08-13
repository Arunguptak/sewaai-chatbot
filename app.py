import streamlit as st
import feedparser
from urllib.parse import quote
from html import escape
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SewaAI News Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 80% 10%, rgba(37, 99, 235, 0.16), transparent 28%),
        radial-gradient(circle at 20% 80%, rgba(124, 58, 237, 0.10), transparent 30%),
        #050914;
    color: #f8fafc;
}

/* Remove default top space */

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #080d1b 0%, #050914 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.15);
}

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 5px 25px 5px;
}

.logo-circle {
    width: 54px;
    height: 54px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    box-shadow: 0 0 30px rgba(37, 99, 235, 0.35);
}

.logo-name {
    font-size: 25px;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo-sub {
    color: #94a3b8;
    font-size: 12px;
}

.sidebar-menu {
    margin-top: 10px;
}

.menu-item {
    padding: 13px 15px;
    margin: 6px 0;
    border-radius: 13px;
    color: #cbd5e1;
    font-size: 14px;
}

.menu-active {
    background: linear-gradient(
        90deg,
        rgba(37,99,235,0.9),
        rgba(79,70,229,0.85)
    );
    color: white;
    box-shadow: 0 10px 30px rgba(37,99,235,0.20);
}

.menu-icon {
    font-size: 20px;
    margin-right: 10px;
}

.menu-title {
    font-weight: 600;
}

.menu-description {
    color: #cbd5e1;
    font-size: 11px;
    margin-left: 31px;
    margin-top: 2px;
}

.sidebar-card {
    margin-top: 30px;
    padding: 18px;
    border: 1px solid rgba(96,165,250,0.25);
    border-radius: 18px;
    background: linear-gradient(
        145deg,
        rgba(37,99,235,0.18),
        rgba(124,58,237,0.18)
    );
}

.sidebar-card-title {
    font-size: 19px;
    font-weight: 700;
}

.sidebar-card-text {
    color: #cbd5e1;
    font-size: 12px;
    line-height: 1.7;
    margin-top: 8px;
}

.sidebar-footer {
    position: fixed;
    bottom: 20px;
    color: #64748b;
    font-size: 11px;
    text-align: center;
}


/* ============================================================
   HEADER
   ============================================================ */

.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
}

.header-title {
    font-size: 20px;
    font-weight: 700;
}

.online {
    color: #cbd5e1;
    font-size: 13px;
}

.online-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 7px;
    box-shadow: 0 0 10px #22c55e;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;
    overflow: hidden;
    padding: 30px;
    border-radius: 22px;
    border: 1px solid rgba(96,165,250,0.28);
    background:
        radial-gradient(circle at 90% 30%, rgba(0,180,255,0.18), transparent 35%),
        linear-gradient(
            135deg,
            rgba(15,23,42,0.95),
            rgba(15,23,70,0.90)
        );
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-title span {
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    color: #cbd5e1;
    font-size: 15px;
    line-height: 1.7;
    max-width: 600px;
}

.hero-robot {
    position: absolute;
    right: 45px;
    top: 35px;
    font-size: 90px;
    opacity: 0.9;
    filter: drop-shadow(0 0 30px rgba(0,149,255,0.35));
}


/* ============================================================
   QUICK BUTTONS
   ============================================================ */

.quick-label {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 20px;
    margin-bottom: 8px;
}

div.stButton > button {
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(96,165,250,0.35);
    color: #e2e8f0;
    border-radius: 10px;
    min-height: 38px;
    font-size: 12px;
    transition: 0.2s;
}

div.stButton > button:hover {
    border-color: #60a5fa;
    background: rgba(37,99,235,0.20);
    color: white;
}


/* ============================================================
   CHAT
   ============================================================ */

.user-bubble {
    background: linear-gradient(135deg, #2563eb, #4338ca);
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    margin-left: auto;
    margin-top: 18px;
    font-size: 14px;
    box-shadow: 0 10px 30px rgba(37,99,235,0.18);
}

.bot-row {
    display: flex;
    gap: 12px;
    margin-top: 22px;
}

.bot-avatar {
    min-width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    font-size: 21px;
}

.bot-bubble {
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(96,165,250,0.14);
    padding: 13px 17px;
    border-radius: 5px 18px 18px 18px;
    color: #e2e8f0;
    font-size: 14px;
}


/* ============================================================
   SUMMARY
   ============================================================ */

.summary-card {
    margin-top: 18px;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(99,102,241,0.35);
    background:
        linear-gradient(
            135deg,
            rgba(30,41,100,0.55),
            rgba(15,23,42,0.90)
        );
}

.summary-title {
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 10px;
}

.summary-text {
    color: #cbd5e1;
    line-height: 1.7;
    font-size: 13px;
}


/* ============================================================
   NEWS
   ============================================================ */

.news-heading {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 25px 0 12px;
}

.news-heading-title {
    font-size: 18px;
    font-weight: 700;
}

.result-badge {
    background: rgba(79,70,229,0.25);
    border: 1px solid rgba(99,102,241,0.35);
    color: #c7d2fe;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 11px;
}

.news-card {
    display: flex;
    gap: 15px;
    padding: 17px;
    margin-bottom: 12px;
    border-radius: 17px;
    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,0.95),
            rgba(17,24,60,0.90)
        );
    border: 1px solid rgba(96,165,250,0.13);
    transition: all 0.2s ease;
}

.news-card:hover {
    border-color: rgba(96,165,250,0.45);
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.20);
}

.news-number {
    width: 34px;
    height: 34px;
    min-width: 34px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    font-weight: 700;
    font-size: 13px;
}

.news-content {
    flex: 1;
}

.news-title {
    font-size: 15px;
    font-weight: 700;
    line-height: 1.4;
    color: #f8fafc;
}

.news-meta {
    color: #64748b;
    font-size: 11px;
    margin-top: 7px;
}

.news-link {
    display: inline-block;
    margin-top: 10px;
    color: #60a5fa !important;
    font-size: 12px;
    text-decoration: none;
}

.news-link:hover {
    color: #93c5fd !important;
}


/* ============================================================
   INPUT
   ============================================================ */

div[data-testid="stChatInput"] {
    background: rgba(15,23,42,0.95);
}

div[data-testid="stChatInput"] textarea {
    color: white !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 22px;
    }

    .hero-title {
        font-size: 25px;
    }

    .hero-robot {
        display: none;
    }

    .news-card {
        padding: 13px;
    }

    .user-bubble {
        max-width: 90%;
    }

    .header-title {
        font-size: 17px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCTIONS
# ============================================================

def get_news(query, limit=10):

    encoded_query = quote(query)

    rss_url = (
        "https://news.google.com/rss/search?"
        f"q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(rss_url)

    articles = []

    for entry in feed.entries[:limit]:

        title = entry.get("title", "No title")
        link = entry.get("link", "")
        published = entry.get("published", "Date unavailable")

        source = "Google News"

        if hasattr(entry, "source"):
            try:
                source = entry.source.get(
                    "title",
                    "Google News"
                )
            except Exception:
                source = "Google News"

        articles.append({
            "title": title,
            "link": link,
            "published": published,
            "source": source
        })

    return articles


def detect_topic(question):

    q = question.lower().strip()

    if "openai" in q or "chatgpt" in q or "gpt" in q:
        return "OpenAI OR ChatGPT OR GPT"

    if "google" in q or "gemini" in q or "deepmind" in q:
        return "Google AI OR Gemini OR DeepMind"

    if "microsoft" in q or "copilot" in q:
        return "Microsoft AI OR Copilot"

    if "india" in q or "indian" in q:
        return "India AI technology"

    if "startup" in q:
        return "AI startups"

    if "machine learning" in q:
        return "machine learning"

    if "technology" in q or "tech" in q:
        return "technology"

    if "ai" in q or "artificial intelligence" in q:
        return "artificial intelligence"

    return question


def create_summary(question, articles):

    if not articles:
        return "I couldn't find relevant news articles for your question."

    titles = [
        article["title"]
        for article in articles[:5]
    ]

    topic = question.strip()

    return (
        f"Here are the latest results related to "
        f"<b>{escape(topic)}</b>. "
        f"The current coverage includes "
        f"{len(articles)} relevant articles from multiple news sources. "
        f"Use the links below to read the original reports and verify "
        f"the latest details."
    )


def display_news(articles):

    for index, article in enumerate(articles, 1):

        title = escape(article["title"])
        source = escape(article["source"])
        published = escape(article["published"])
        link = escape(article["link"], quote=True)

        st.markdown(
            f"""
            <div class="news-card">

                <div class="news-number">
                    {index}
                </div>

                <div class="news-content">

                    <div class="news-title">
                        {title}
                    </div>

                    <div class="news-meta">
                        {source} &nbsp;•&nbsp; {published}
                    </div>

                    <a
                        class="news-link"
                        href="{link}"
                        target="_blank"
                    >
                        🔗 Read Full Article →
                    </a>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


def search_and_display(question):

    with st.spinner("🔎 Searching latest news..."):

        search_query = detect_topic(question)
        articles = get_news(search_query, 10)

    return articles


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-logo">

            <div class="logo-circle">
                🤖
            </div>

            <div>
                <div class="logo-name">
                    SewaAI
                </div>

                <div class="logo-sub">
                    News Assistant
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-menu">

            <div class="menu-item menu-active">
                <span class="menu-icon">💬</span>
                <span class="menu-title">Chat</span>
                <div class="menu-description">
                    Ask for latest news
                </div>
            </div>

            <div class="menu-item">
                <span class="menu-icon">⚡</span>
                <span class="menu-title">Top Headlines</span>
                <div class="menu-description">
                    Today's top news
                </div>
            </div>

            <div class="menu-item">
                <span class="menu-icon">🤖</span>
                <span class="menu-title">AI & Technology</span>
                <div class="menu-description">
                    AI, Tech & Innovation
                </div>
            </div>

            <div class="menu-item">
                <span class="menu-icon">🇮🇳</span>
                <span class="menu-title">India News</span>
                <div class="menu-description">
                    India & Global News
                </div>
            </div>

            <div class="menu-item">
                <span class="menu-icon">🔖</span>
                <span class="menu-title">Saved</span>
                <div class="menu-description">
                    Saved articles
                </div>
            </div>

            <div class="menu-item">
                <span class="menu-icon">ⓘ</span>
                <span class="menu-title">About SewaAI</span>
                <div class="menu-description">
                    About this assistant
                </div>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    today = datetime.now().strftime("%d %B %Y")

    st.markdown(
        f"""
        <div class="sidebar-card">

            <div class="sidebar-card-title">
                📅 Today at a glance
            </div>

            <div class="sidebar-card-text">
                {today}
            </div>

            <hr style="border-color:rgba(148,163,184,0.12);">

            <div style="
                display:flex;
                justify-content:space-between;
                text-align:center;
            ">

                <div>
                    <b style="font-size:20px;">AI</b>
                    <br>
                    <small>Focus</small>
                </div>

                <div>
                    <b style="font-size:20px;">10</b>
                    <br>
                    <small>Articles</small>
                </div>

                <div>
                    <b style="font-size:20px;">24/7</b>
                    <br>
                    <small>Updates</small>
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-card">

            <div class="sidebar-card-title">
                🚀 Stay Ahead with SewaAI
            </div>

            <div class="sidebar-card-text">
                Your intelligent assistant for the latest
                AI & Technology news.
            </div>

        </div>

        <div class="sidebar-footer">
            Made with ❤️ by <b>SewaAI</b><br>
            Empowering Knowledge Through AI
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="top-header">

        <div class="header-title">
            🤖 SewaAI News Assistant
        </div>

        <div class="online">
            <span class="online-dot"></span>
            Online
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            Hello! I'm <span>SewaAI</span> 👋
        </div>

        <div class="hero-description">
            Ask me about the latest AI & Technology news
            and discover what's happening around the world.
        </div>

        <div class="hero-robot">
            🤖
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# QUICK QUESTIONS
# ============================================================

st.markdown(
    '<div class="quick-label">Try a quick search</div>',
    unsafe_allow_html=True
)

quick_questions = [
    "OpenAI latest news",
    "Google AI updates",
    "Microsoft AI news",
    "Latest AI news",
    "India AI technology"
]

cols = st.columns(5)

for i, question_text in enumerate(quick_questions):

    with cols[i]:

        if st.button(
            question_text,
            key=f"quick_{i}",
            use_container_width=True
        ):

            st.session_state.selected_topic = question_text


# ============================================================
# QUICK QUESTION PROCESSING
# ============================================================

if st.session_state.selected_topic:

    question = st.session_state.selected_topic

    st.session_state.selected_topic = None

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    articles = search_and_display(question)

    st.session_state.messages.append({
        "role": "assistant",
        "question": question,
        "articles": articles
    })

    st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-bubble">
                {escape(message["content"])}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        question = message.get(
            "question",
            "latest news"
        )

        articles = message.get(
            "articles",
            []
        )

        st.markdown(
            """
            <div class="bot-row">

                <div class="bot-avatar">
                    🤖
                </div>

                <div class="bot-bubble">
                    Here are the latest news results for you.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if articles:

            summary = create_summary(
                question,
                articles
            )

            st.markdown(
                f"""
                <div class="summary-card">

                    <div class="summary-title">
                        📝 Summary
                    </div>

                    <div class="summary-text">
                        {summary}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="news-heading">

                    <div class="news-heading-title">
                        📰 Top 10 Latest News
                    </div>

                    <div class="result-badge">
                        {len(articles)} Results Found
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            display_news(articles)

        else:

            st.warning(
                "No relevant news articles were found."
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask anything about AI & Technology news..."
)


if question:

    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    articles = search_and_display(question)

    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "question": question,
        "articles": articles
    })

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#475569;
        font-size:10px;
        margin-top:30px;
        padding-bottom:10px;
    ">
        SewaAI can make mistakes. Please verify information
        from the original source.
    </div>
    """,
    unsafe_allow_html=True
)
