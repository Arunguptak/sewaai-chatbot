import streamlit as st
import feedparser
from urllib.parse import quote

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SewaAI",
    page_icon="🤖",
    layout="centered"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.main {
    max-width: 900px;
    margin: auto;
}

.sewa-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
}

.sewa-subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 25px;
}

.news-card {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 12px;
}

.news-title {
    font-size: 18px;
    font-weight: 600;
}

.news-source {
    font-size: 13px;
    color: #777;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="sewa-title">🤖 SewaAI </div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sewa-subtitle">Ask SewaAI anything...</div>',
    unsafe_allow_html=True
)

# ============================================================
# NEWS FUNCTION
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
# ANSWER FUNCTION
# ============================================================

def answer_question(question):

    question_lower = question.lower()

    # Determine search topic

    if "openai" in question_lower:
        search_query = "OpenAI"

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

    articles = get_news(search_query, 10)

    return articles


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "user":

            st.write(message["content"])

        else:

            for article in message["articles"]:

                st.markdown(
                    f"""
                    <div class="news-card">

                    <div class="news-title">
                    📰 {article['title']}
                    </div>

                    <div class="news-source">
                    {article['source']} • {article['published']}
                    </div>

                    <br>

                    <a href="{article['link']}" target="_blank">
                    🔗 Read Full Article
                    </a>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask about latest news..."
)


if question:

    # User message

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # Assistant response

    with st.chat_message("assistant"):

        with st.spinner("🔎 Searching latest news..."):

            try:

                articles = answer_question(question)

                if not articles:

                    st.warning(
                        "No news articles found."
                    )

                else:

                    st.success(
                        f"Found {len(articles)} latest articles."
                    )

                    for article in articles:

                        st.markdown(
                            f"""
                            <div class="news-card">

                            <div class="news-title">
                            📰 {article['title']}
                            </div>

                            <div class="news-source">
                            {article['source']} • {article['published']}
                            </div>

                            <br>

                            <a href="{article['link']}" target="_blank">
                            🔗 Read Full Article
                            </a>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                st.session_state.messages.append({
                    "role": "assistant",
                    "articles": articles
                })

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )
