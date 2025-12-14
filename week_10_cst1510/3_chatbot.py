import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="ChatGPT Assistant",
    page_icon="💬",
    layout="wide"
)

# Check authentication (keeps your existing behavior)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

# --- Ensure required session_state keys exist before reading them ---
# These defaults are safe and prevent AttributeError when rendering the sidebar.
if "username" not in st.session_state:
    st.session_state.username = "Unknown"
if "role" not in st.session_state:
    # default role (lowercase expected elsewhere); change to "admin"/"member" as needed
    st.session_state.role = "user"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_domain" not in st.session_state:
    st.session_state.selected_domain = "Cybersecurity"

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title
st.title("💬 ChatGPT - OpenAI API")
st.caption("Powered by GPT-4o")

# Domain-specific system prompts
DOMAIN_PROMPTS = {
    "Cybersecurity": """You are a cybersecurity expert assistant.
Analyze incidents, threats, and provide technical guidance.""",

    "Data Science": """You are a data science expert assistant.
Help with analysis, visualization, and statistical insights.""",

    "IT Operations": """You are an IT operations expert assistant.
Help troubleshoot issues, optimize systems, and manage tickets."""
}

# ---------------- Sidebar ----------------
with st.sidebar:
    st.subheader("User Info")
    # Safe to read now because we initialized above
    st.write(f"👤 {st.session_state.username}")
    # Ensure role is a string before calling .upper()
    st.write(f"🔑 {str(st.session_state.role).upper()}")

    st.markdown("---")
    st.subheader("Domain Selection")

    # Domain selector (use the stored selected_domain as the default)
    domain = st.selectbox(
        "Choose Domain",
        ["Cybersecurity", "Data Science", "IT Operations"],
        index=["Cybersecurity", "Data Science", "IT Operations"].index(st.session_state.selected_domain)
    )

    # Update domain if changed
    if domain != st.session_state.selected_domain:
        st.session_state.selected_domain = domain
        st.session_state.messages = []  # Clear chat when domain changes
        st.success(f"Switched to {domain} domain")
        st.rerun()

    # Display current system prompt
    with st.expander("View System Prompt"):
        st.code(DOMAIN_PROMPTS[domain], language="text")

    st.markdown("---")
    st.subheader("Chat Controls")

    # Display message count (exclude system messages)
    message_count = len([m for m in st.session_state.messages if m.get("role") != "system"])
    st.metric("Messages", message_count)

    # Clear chat button
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Model selection
    model = st.selectbox(
        "Model",
        ["gpt-4o", "gpt-4o-mini"],
        index=1
    )

    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Higher values make output more random"
    )

# --------------- Chat history ---------------
for message in st.session_state.messages:
    # protect against poorly formed messages
    role = message.get("role", "user")
    content = message.get("content", "")
    with st.chat_message(role):
        st.markdown(content)

# --------------- Input & API call ---------------
prompt = st.chat_input("Say something...")

if prompt:
    # Show the user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to session
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Prepare messages with system prompt for the selected domain
    messages_with_system = [
        {"role": "system", "content": DOMAIN_PROMPTS[st.session_state.selected_domain]}
    ] + st.session_state.messages

    # Call OpenAI API with streaming
    with st.spinner("Thinking..."):
        completion = client.chat.completions.create(
            model=model,
            messages=messages_with_system,
            temperature=temperature,
            stream=True
        )

    # Display streaming response
    with st.chat_message("assistant"):
        container = st.empty()
        full_reply = ""

        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta.content:
                full_reply += delta.content
                container.markdown(full_reply + "▌")  # cursor effect

        container.markdown(full_reply)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })
