import os
import random
import streamlit as st
from google import genai

# python -m streamlit run lovechatbot.py
# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="LoveBot ❤️",
    page_icon="❤️",
    layout="wide"
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.0-flash"  # double-check this against Google's current model list

sys_prompt = """
You are LoveBot ❤️, an AI Relationship Coach.

You help users with:

- Proposal ideas
- Dating advice
- Relationship guidance
- Conversation starters
- Flirting tips
- Breakup recovery
- Long-distance relationships
- Confidence building
- First date ideas
- Romantic messages

Rules:

• Always encourage respect and consent.
• Never promote manipulation or harassment.
• Keep responses friendly.
• Be supportive and positive.
• Give practical advice.
"""


def ask_lovebot(user_prompt: str) -> str:
    """Call Gemini with the system prompt + user request, with basic error handling."""
    full_prompt = f"{sys_prompt}\n\nUser request: {user_prompt}"
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ Sorry, something went wrong talking to the AI: {e}"


# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("❤️ LoveBot")

    st.markdown("---")

    st.subheader("Categories")

    category = st.selectbox(
        "",
        [
            "💍 Proposal Tips",
            "💕 Relationship Advice",
            "😍 Flirting",
            "💬 Conversation",
            "🎁 Date Ideas",
            "💔 Breakup Help",
            "❤️ Self Confidence"
        ]
    )

    st.markdown("---")

    mood = st.select_slider(
        "Your Mood",
        [
            "😊 Happy",
            "🥰 Excited",
            "😍 In Love",
            "😔 Sad",
            "💔 Heartbroken"
        ]
    )

    confidence = st.slider(
        "Confidence",
        0,
        100,
        70
    )

    st.progress(confidence)

    st.markdown("---")

    if st.button("🎈 Celebrate Love"):
        st.balloons()

# ---------------- HEADER ---------------- #

st.markdown(
"""
<h1 style='text-align:center;color:#ff4b6e;'>
❤️ LoveBot AI ❤️
</h1>

<h4 style='text-align:center;'>
Your Personal Relationship Coach
</h4>
""",
unsafe_allow_html=True
)

# ---------------- DAILY QUOTE ---------------- #

quotes = [

"Love begins with respect. ❤️",

"Communication builds strong relationships.",

"Trust takes years to build.",

"Be yourself. That's attractive.",

"A smile is the best first impression.",

"Confidence is more attractive than perfection."

]

st.info(random.choice(quotes))

# ---------------- LOVE TIP ---------------- #

st.success("💡 Love Tip of the Day")

st.write(
"Instead of trying to impress someone, focus on making them feel comfortable around you."
)

# ---------------- QUICK BUTTONS ---------------- #

st.subheader("🔥 Quick Questions")

c1, c2, c3 = st.columns(3)

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = ""

with c1:
    if st.button("💍 How to Propose"):
        st.session_state.quick_prompt = "How should I propose to my crush?"

with c2:
    if st.button("😍 Impress Someone"):
        st.session_state.quick_prompt = "How can I impress someone?"

with c3:
    if st.button("💕 First Date"):
        st.session_state.quick_prompt = "Give me first date ideas."

# ---------------- PROPOSAL GENERATOR ---------------- #

st.markdown("---")

st.subheader("🎁 Proposal Generator")

col1, col2 = st.columns(2)

with col1:
    partner = st.text_input("Partner Name")

with col2:
    style = st.selectbox(
        "Proposal Style",
        [
            "Romantic ❤️",
            "Cute 😊",
            "Funny 😂",
            "Poetic 🌹",
            "Formal 💌"
        ]
    )

if st.button("Generate Proposal ❤️"):

    if partner != "":

        prompt = f"Write a {style} proposal for {partner}."

        with st.spinner("Writing your proposal ❤️..."):
            answer = ask_lovebot(prompt)

        st.success(answer)
    else:
        st.warning("Please enter a partner name first.")

# ---------------- CHAT HISTORY ---------------- #

st.markdown("---")

st.subheader("💬 Chat with LoveBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "Ask anything about love..."
)

if prompt is None and st.session_state.quick_prompt != "":
    prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = ""

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("LoveBot is thinking ❤️..."):
        answer = ask_lovebot(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ---------------- RELATIONSHIP CARD ---------------- #

st.markdown("---")

st.markdown(
"""
<div style="
background-color:#ffe6ee;
padding:20px;
border-radius:15px;
text-align:center;
">

<h2>❤️ Relationship Advice ❤️</h2>

<p>
Healthy relationships are built on honesty,
communication,
trust,
respect,
and mutual understanding.
</p>

</div>
""",
unsafe_allow_html=True
)

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown(
"""
<center>

Made with ❤️ using Streamlit + Gemini AI

</center>
""",
unsafe_allow_html=True
)