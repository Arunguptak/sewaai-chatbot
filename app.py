import streamlit as st
import requests

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

st.markdown(
    """
    <style>

    .main {
        max-width: 900px;
        margin: auto;
    }

    .sewa-title {
        text-align: center;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 2px;
    }

    .sewa-subtitle {
        text-align: center;
        font-size: 13px;
        color: #64748b;
        margin-bottom: 20px;
    }

    .source-box {
        font-size: 12px;
    }

    @media (max-width: 600px) {

        .sewa-title {
            font-size: 23px;
        }

        .sewa-subtitle {
            font-size: 11px;
        }

        .main {
            padding: 5px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="sewa-title">
        🤖 SewaAI
    </div>

    <div class="sewa-subtitle">
        Your Smart Learning Assistant<br>
        AI • GenAI • Data • Databricks • Cloud
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# API URL
# ============================================================

API_URL = ""



# ============================================================
# SESSION
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# DISPLAY CHAT
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# USER QUESTION
# ============================================================

question = st.chat_input(
    "Ask SewaAI anything..."
)


# ============================================================
# ASK SEWAAI
# ============================================================

if question:

    # --------------------------------------------------------
    # User message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # --------------------------------------------------------
    # Assistant
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("SewaAI is thinking..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=90
                )

                response.raise_for_status()

                result = response.json()

                answer = result.get(
                    "answer",
                    "No answer returned."
                )

                sources = result.get(
                    "sources",
                    []
                )


                # ------------------------------------------------
                # Answer
                # ------------------------------------------------

                st.markdown(answer)


                # ------------------------------------------------
                # Sources
                # ------------------------------------------------

                if sources:

                    with st.expander(
                        "📚 Sources"
                    ):

                        for i, source in enumerate(
                            sources[:5],
                            start=1
                        ):

                            source_name = source.get(
                                "source_name",
                                "Unknown"
                            )

                            title = source.get(
                                "title",
                                ""
                            )

                            url = source.get(
                                "url",
                                ""
                            )

                            st.markdown(
                                f"**{i}. {source_name}**"
                            )

                            if title:

                                st.write(title)

                            if url:

                                st.markdown(
                                    f"[🔗 Read source]({url})"
                                )


                # ------------------------------------------------
                # Save assistant response
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            except Exception as e:

                error_message = (
                    "❌ **SewaAI Connection Error**\n\n"
                    "The backend did not return a response.\n\n"
                    f"`{str(e)}`"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )
