import streamlit as st
import google.generativeai as genai
import re

# -----------------------------------------------------------------------------
# IMPORTANT: Replace this with your Google Gemini API key.
# genai.configure(api_key="YOUR_GEMINI_API_KEY") 

# If using Streamlit secrets, uncomment the line below and set your key in .streamlit/secrets.toml
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# -----------------------------------------------------------------------------
model = genai.GenerativeModel("gemini-1.5-flash")


# ----------------------------
# Function to clean model output
# ----------------------------
def clean_output(text):
    # Remove <think>...</think> blocks
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# ----------------------------
# Function to generate blog using Ollama (now pointing to Colab)
# ----------------------------
def generate_blog(topic, temperature, word_count_half, tone, language, tldr, emoji_level):
    word_count = word_count_half * 2  # Adjust to match the original word count
    tldr_text = "Include a TL;DR summary at the top.\n" if tldr else ""
    emoji_text = f"Use emojis {emoji_level}ly in headings and text.\n"

    prompt = f"""
You are a professional Medium blog writer.
Write a blog post for the topic: "{topic}" in {language}.
The blog must:
- Not be less than {word_count} words
- Have some more attractive topic name not just the topic
- Be structured with headings and subheadings
- Have an engaging title with emojis
- Use attractive section headings
- Be written in a {tone} tone
- Contain about {word_count} words
- Use bullet points and numbered lists where appropriate
- Be ready to upload without further editing
- Use markdown for formatting
{tldr_text}
{emoji_text}

Write it now:
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": temperature}
        )
        return response.text
    except Exception as e:
        return f"⚠ Could not connect to Gemini API. Error: {e}"


# ----------------------------
# Streamlit App UI
# ----------------------------
st.set_page_config(page_title="Blog Generator", page_icon="📝", layout="wide")
st.title("📝 Blog Generator")
st.markdown("Create *beautiful, ready-to-upload blog posts* instantly using your AI model.")

# Sidebar Settings
st.sidebar.header("⚙ Blog Settings")
st.sidebar.markdown(f"*Using Model:* Gemini 1.5 Flash") # Indicate fixed model
temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.7, 0.1)
word_count = st.sidebar.slider("Target Word Count", 500, 2000, 1200, 100)
tone = st.sidebar.selectbox("Tone", ["Professional", "Casual", "Inspirational", "Funny", "Persuasive"])
language = st.sidebar.selectbox("Language", ["English", "Spanish", "French", "German", "Urdu"])
tldr = st.sidebar.checkbox("Include TL;DR Summary", value=True)
emoji_level = st.sidebar.selectbox("Emoji Usage", ["light", "moderate", "heavy"])

# Store blog in session state so it doesn't disappear
if "blog_content" not in st.session_state:
    st.session_state.blog_content = ""

# User Input
topic = st.text_input("📌 Enter your blog topic:", placeholder="e.g. The Future of AI in Education")

if st.button("🚀 Generate Blog", type="primary"):
    if topic.strip() == "":
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("✨ Crafting your blog... please wait..."):
            st.session_state.blog_content = generate_blog(
                topic, temperature, word_count, tone, language, tldr, emoji_level
            )

# Display Blog
if st.session_state.blog_content:
    st.markdown(st.session_state.blog_content)

    # Download Option
    st.download_button(
        label="📥 Download Blog as Markdown",
        data=st.session_state.blog_content,
        file_name=f"{topic.replace(' ', '_')}.md",
        mime="text/markdown"
    )

st.markdown("---")
st.markdown("💡 Tip: Ensure your Google Colab notebook with Ollama and ngrok is running!")