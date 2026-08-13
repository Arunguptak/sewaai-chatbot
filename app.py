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
# SESSION
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.html("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 80% 10%,
            rgba(37,99,235,.16),
            transparent 30%
        ),
        #050914;
    color: #ffffff;
}

.block-container {
    max-width: 1200px;
    padding-top: 25px;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #070b17;
    border-right: 1px solid #1e293b;
}

.sidebar-logo {
    display:flex;
    align-items:center;
    gap:12px;
    padding:15px 5px 25px 5px;
}

.logo {
    width:55px;
    height:55px;
    border-radius:16px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:30px;
    background:linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
}

.logo-name {
    font-size:25px;
    font-weight:bold;
    color:#60a5fa;
}

.logo-sub {
    color:#94a3b8;
    font-size:12px;
}

.side-item {
    padding:14px;
    margin:6px 0;
    border-radius:12px;
    color:#cbd5e1;
}

.side-active {
    background:linear-gradient(
        90deg,
        #2563eb,
        #4338ca
    );
    color:white;
}

.side-title {
    font-weight:bold;
}

.side-text {
    font-size:11px;
    color:#94a3b8;
    margin-top:3px;
}

.side-card {
    margin-top:25px;
    padding:18px;
    border-radius:18px;
    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,.18),
            rgba(124,58,237,.18)
        );
    border:1px solid #263b76;
}

.side-card-title {
    font-size:18px;
    font-weight:bold;
}

.side-card-text {
    color:#cbd5e1;
    font-size:12px;
    line-height:1.7;
    margin-top:8px;
}


/* HEADER */

.topbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:20px;
}

.top-title {
    font-size:20px;
    font-weight:bold;
}

.online {
    color:#cbd5e1;
    font-size:13px;
}

.online-dot {
    display:inline-block;
    width:8px;
    height:8px;
    border-radius:50%;
    background:#22c55e;
    box-shadow:0 0 10px #22c55e;
    margin-right:6px;
}


/* HERO */

.hero {
    padding:30px;
    border-radius:22px;
    border:1px solid #263b76;
    background:
        linear-gradient(
            135deg,
            rgba(15,23,42,.96),
            rgba(15,23,70,.92)
        );
    margin-bottom:20px;
}

.hero-title {
    font-size:34px;
    font-weight:bold;
}

.hero-title span {
    color:#38bdf8;
}

.hero-text {
    margin-top:10px;
    color:#cbd5e1;
    line-height:1.7;
}

.robot {
    font-size:75px;
    text-align:center;
}


/* SUMMARY */

.summary {
    margin-top:20px;
    padding:20px;
    border-radius:18px;
    border:1px solid #263b76;
    background:
        linear-gradient(
            135deg,
            rgba(30,41,100,.55),
            rgba(15,23,42,.9)
        );
}

.summary-title {
    font-size:17px;
    font-weight:bold;
    margin-bottom:10px;
}

.summary-text {
    color:#cbd5e1;
    font-size:13px;
    line-height:1.7;
}


/* NEWS */

.news-header {
    display:flex;
    justify-content:space-between;
    margin-top:25px;
    margin-bottom:12px;
}

.news-header-title {
    font-size:19px;
    font-weight:bold;
}

.badge {
    padding:6px 12px;
    border-radius:20px;
    background:#172554;
    color:#93c5fd;
    font-size:11px;
}

.news-card {
    display:flex;
    gap:14px;
    padding:17px;
    margin-bottom:12px;
    border-radius:16px;
    background:#0d1428;
    border:1px solid #1e2b4b;
}

.news-number {
    width:34px;
    height:34px;
    min-width:34px;
    border-radius:50%;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(
        135deg,
        #2563eb,
        #4f46e5
    );
    font-weight:bold;
}

.news-title {
    font-weight:bold;
    font-size:15px;
    line-height:1.5;
}

.news-source {
    margin-top:7px;
    color:#64748b;
    font-size:11px;
}

.news-link {
    display:inline-block;
    margin-top:9px;
    color:#60a5fa;
    text-decoration:none;
    font-size:12px;
}


/* CHAT */

.user-msg {
    margin-top:20px;
    margin-left:auto;
    max-width:75%;
    padding:14px 18px;
    border-radius:18px 18px 4px 18px;
    background:linear-gradient(
        135deg,
        #2563eb,
        #4338ca
    );
}

.bot-msg {
    display:flex;
    gap:12px;
    margin-top:20px;
}

.bot-avatar {
    width:42px;
    height:42px;
    min-width:42px;
    border-radius:50%;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
    font-size:20px;
}

.bot-text {
    padding:13px 17px;
    border-radius:5px 18px 18px 18px;
    background:#0f172a;
    border:1px solid #1e293b;
}


/* MOBILE */

@media(max-width:768px) {

    .hero-title {
        font-size:25px;
    }

    .robot {
        display:none;
    }

    .user-msg {
        max-width:90%;
    }

    .block-container {
        padding-left:12px;
        padding-right:12px;
    }

}

</style>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-logo">
        <div class="logo">🤖</div>

        <div>
            <div class="logo-name">
                SewaAI
            </div>

            <div class="logo-sub">
                News Assistant
            </div>
        </div>
    </div>
    """)

    st.html("""
    <div class="side-item side-active">
        💬 <span class="side-title">Chat</span>
        <div class="side-text">
            Ask for latest news
        </div>
    </div>

    <div class="side-item">
        ⚡ <span class="side-title">Top Headlines</span>
        <div class="side-text">
            Today's top news
        </div>
    </div>

    <div class="side-item">
        🤖 <span class="side-title">AI & Technology</span>
        <div class="side-text">
            AI, Tech & Innovation
        </div>
    </div>

    <div class="side-item">
        🇮🇳 <span class="side-title">India News</span>
        <div class="side-text">
            India & Global News
        </div>
    </div>

    <div class="side-item">
        🔖 <span class="side-title">Saved</span>
        <div class="side-text">
            Saved articles
        </div>
    </div>
    """)

    today = datetime.now().strftime("%d %B %Y")

    st.html(f"""
    <div class="side-card">

        <div class="side-card-title">
            📅 Today at a glance
        </div>

        <div class="side-card-text">
            {today}
        </div>

        <hr style="border-color:#1e293b">

        <div style="
            display:flex;
            justify-content:space-between;
            text-align:center;
        ">

            <div>
                <b style="font-size:20px">AI</b><br>
                <small>Focus</small>
            </div>

            <div>
                <b style="font-size:20px">10</b><br>
                <small>Articles</small>
            </div>

            <div>
                <b style="font-size:20px">24/7</b><br>
                <small>Updates</small>
            </div>

        </div>

    </div>
    """)

    st.html("""
    <div class="side-card">

        <div class="side-card-title">
            🚀 Stay Ahead
        </div>

        <div class="side-card-text">
            Your intelligent assistant for
            AI & Technology news.
        </div>

    </div>
    """)


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="topbar">

    <div class="top-title">
        🤖 SewaAI News Assistant
    </div>

    <div class="online">
        <span class="online-dot"></span>
        Online
    </div>

</div>
""")


# ============================================================
# HERO
# ============================================================

col1, col2 = st.columns([4, 1])

with col1:

    st.html("""
    <div class="hero">

        <div class="hero-title">
            Hello! I'm <span>SewaAI</span> 👋
        </div>

        <div class="hero-text">
            Ask me about the latest AI & Technology news
            and discover what's happening around the world.
        </div>

    </div>
    """)

with col2:

    st.html("""
    <div class="hero">
        <div class="robot">🤖</div>
    </div>
    """)


# ============================================================
# QUICK QUESTIONS
# ============================================================

st.caption("Try a quick search")

q1, q2, q3, q4, q5 = st.columns(5)

quick_question = None

with q1:
    if st.button("OpenAI News", use_container_width=True):
        quick_question = "Latest OpenAI news"

with q2:
    if st.button("Google AI", use_container_width=True):
        quick_question = "Latest Google AI news"

with q3:
    if st.button("Microsoft AI", use_container_width=True):
        quick_question = "Latest Microsoft AI news"

with q4:
    if st.button("Latest AI", use_container_width=True):
        quick_question = "Latest AI news"

with q5:
    if st.button("India AI", use_container_width=True):
        quick_question = "Latest AI technology news in India"


# ============================================================
# NEWS SEARCH
# ============================================================

def get_news(query, limit=10):

    url = (
        "https://news.google.com/rss/search?"
        f"q={quote(query)}"
        "&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:limit]:

        source = "Google News"

        try:
            source = entry.source.get(
                "title",
                "Google News"
            )
        except Exception:
            pass

        articles.append({
            "title": entry.get("title", "No title"),
            "link": entry.get("link", ""),
            "published": entry.get(
                "published",
                "Date unavailable"
            ),
            "source": source
        })

    return articles


def detect_topic(question):

    q = question.lower()

    if "openai" in q or "chatgpt" in q:
        return "OpenAI ChatGPT"

    if "google" in q or "gemini" in q:
        return "Google AI Gemini"

    if "microsoft" in q or "copilot" in q:
        return "Microsoft AI Copilot"

    if "india" in q or "indian" in q:
        return "India AI technology"

    if "technology" in q or "tech" in q:
        return "technology"

    if "ai" in q or "artificial intelligence" in q:
        return "artificial intelligence"

    return question


def process_question(question):

    search_query = detect_topic(question)

    with st.spinner("🔎 Searching latest news..."):
        articles = get_news(search_query, 10)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    st.session_state.messages.append({
        "role": "assistant",
        "question": question,
        "articles": articles
    })


# ============================================================
# QUICK SEARCH PROCESS
# ============================================================

if quick_question:

    process_question(quick_question)

    st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.html(
            f"""
            <div class="user-msg">
                {escape(message["content"])}
            </div>
            """
        )

    else:

        articles = message.get("articles", [])

        st.html("""
        <div class="bot-msg">

            <div class="bot-avatar">
                🤖
            </div>

            <div class="bot-text">
                Here are the latest news results for you.
            </div>

        </div>
        """)

        if articles:

            st.html(
                f"""
                <div class="summary">

                    <div class="summary-title">
                        📝 News Summary
                    </div>

                    <div class="summary-text">
                        I found {len(articles)}
                        relevant news articles.
                        These results are collected from
                        Google News and can be opened using
                        the original article links below.
                    </div>

                </div>

                <div class="news-header">

                    <div class="news-header-title">
                        📰 Top Latest News
                    </div>

                    <div class="badge">
                        {len(articles)} Results
                    </div>

                </div>
                """
            )

            for i, article in enumerate(articles, 1):

                title = escape(article["title"])
                source = escape(article["source"])
                published = escape(article["published"])
                link = escape(
                    article["link"],
                    quote=True
                )

                st.html(
                    f"""
                    <div class="news-card">

                        <div class="news-number">
                            {i}
                        </div>

                        <div>

                            <div class="news-title">
                                {title}
                            </div>

                            <div class="news-source">
                                {source} • {published}
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
                    """
                )

        else:

            st.warning(
                "No news articles found."
            )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask anything about AI & Technology news..."
)

if question:

    process_question(question)

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div style="
    text-align:center;
    color:#64748b;
    font-size:10px;
    margin-top:30px;
    padding:20px;
">
    SewaAI can make mistakes.
    Please verify information from the original source.
</div>
""")
