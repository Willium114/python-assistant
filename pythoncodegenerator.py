import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Groq client
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    api_loaded = True
except:
    api_loaded = False

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="Python AI Assistant - Powered by GROQ",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- Custom CSS --------------------
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Main Container */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 1rem;
    }

    /* Header Animation */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Title Styling */
    .main-title {
    background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 3.5rem;
    font-weight: 900;
    margin-bottom: 0.5rem;
    animation: slideInDown 1s ease-out;
}


    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.3rem;
        margin-bottom: 1.5rem;
        font-weight: 300;
        animation: fadeIn 1.5s ease-out;
    }

    /* Chat Message Styling */
    .stChatMessage {
        background: white;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        animation: fadeIn 0.5s ease-out;
    }

    /* User Message */
    [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 15px;
        font-size: 1.05rem;
    }

    /* Code Block Styling */
    code {
        background: #f8f9fa;
        color: #e83e8c;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }

    pre {
        background: #282c34;
        color: #abb2bf;
        padding: 20px;
        border-radius: 10px;
        overflow-x: auto;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }

    section[data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600;
    }

    /* Stats Box */
    .stats-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        margin: 10px 0;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }

    .stats-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
    }

    .stats-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
    }

    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
    }

    /* Feature Card */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }

    .feature-title {
        color: #667eea;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .feature-desc {
        color: #666;
        font-size: 0.95rem;
    }

    /* Badge */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 3px;
        background: linear-gradient(120deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    /* Alert Box */
    .alert-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(120deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        animation: pulse 1s infinite;
    }

    /* Chat Input */
    .stChatInput {
        border-radius: 25px;
    }

    .stChatInput > div > div {
        border-radius: 25px;
        border: 2px solid #667eea;
    }

    /* Divider */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        margin: 30px 0;
    }

    /* Typing Indicator */
    .typing-indicator {
        display: inline-block;
        padding: 10px 20px;
        background: #f8f9fa;
        border-radius: 20px;
        animation: pulse 1.5s infinite;
    }

    .typing-indicator span {
        height: 10px;
        width: 10px;
        background: #667eea;
        border-radius: 50%;
        display: inline-block;
        margin: 0 2px;
        animation: bounce 1.4s infinite ease-in-out both;
    }

    .typing-indicator span:nth-child(1) {
        animation-delay: -0.32s;
    }

    .typing-indicator span:nth-child(2) {
        animation-delay: -0.16s;
    }

    @keyframes bounce {
        0%, 80%, 100% { 
            transform: scale(0);
        } 
        40% { 
            transform: scale(1);
        }
    }

    /* Example Queries */
    .example-query {
        background: linear-gradient(135deg, #e0e7ff 0%, #f3e7ff 100%);
        border-radius: 12px;
        padding: 12px 20px;
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }

    .example-query:hover {
        transform: translateX(8px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        background: linear-gradient(135deg, #c7d5ff 0%, #e5d4ff 100%);
    }

    /* Model Info */
    .model-info {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid #667eea;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    /* Success Message */
    .success-badge {
        background: linear-gradient(120deg, #4facfe, #00f2fe);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        display: inline-block;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- Initialize Session State --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()

# -------------------- Header --------------------
st.markdown("""
<h1 style='
    background-color: black;
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    text-align: center;
'>
🐍 Python AI Assistant
</h1>
""", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by GROQ's LLaMA 3.1 • Your Personal Python Expert</p>", unsafe_allow_html=True)

# API Status
if api_loaded:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <span class='success-badge'>✅ GROQ API Connected</span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class='alert-box' style='text-align: center;'>
            ⚠️ GROQ API Key not found. Please add your API key to .env file.
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("### ⚙️ Assistant Configuration")
    st.markdown("---")

    # Model Selection
    model_option = st.selectbox(
        "🤖 Select Model",
        ["llama-3.1-8b-instant", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
        help="Choose the AI model for responses"
    )

    st.markdown("---")

    # Session Statistics
    st.markdown("### 📊 Session Statistics")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class='stats-box'>
                <div class='stats-number'>{st.session_state.total_queries}</div>
                <div class='stats-label'>Total Queries</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='stats-box'>
                <div class='stats-number'>{len(st.session_state.messages)}</div>
                <div class='stats-label'>Messages</div>
            </div>
        """, unsafe_allow_html=True)

    # Session Duration
    duration = datetime.now() - st.session_state.session_start
    minutes = int(duration.total_seconds() / 60)

    st.markdown(f"""
        <div class='stats-box'>
            <div class='stats-number'>{minutes}</div>
            <div class='stats-label'>Minutes Active</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Model Info
    st.markdown("### 🔧 Model Information")
    st.markdown(f"""
        <div class='model-info'>
            <p><strong>Model:</strong> {model_option}</p>
            <p><strong>Provider:</strong> GROQ</p>
            <p><strong>Type:</strong> Large Language Model</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("📥 Export Conversation", use_container_width=True):
        if st.session_state.messages:
            conversation = "\n\n".join([f"{msg['role'].upper()}: {msg['content']}"
                                        for msg in st.session_state.messages])
            st.download_button(
                label="Download as TXT",
                data=conversation,
                file_name=f"python_assistant_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

    st.markdown("---")

    # Tips
    st.markdown("### 💡 Pro Tips")
    st.info("""
    - Be specific in your questions
    - Ask for code examples
    - Request explanations
    - Debug your Python errors
    - Learn best practices
    """)

# -------------------- Main Chat Area --------------------
col_main, col_examples = st.columns([2.5, 1], gap="large")

with col_main:
    st.markdown("### 💬 Conversation")

    # Chat Container
    chat_container = st.container(height=500)

    with chat_container:
        # Display chat history
        if not st.session_state.messages:
            st.markdown("""
                <div style='text-align: center; padding: 50px; color: #999;'>
                    <div style='font-size: 3rem; margin-bottom: 20px;'>🐍</div>
                    <h3 style='color: #667eea;'>Welcome to Python AI Assistant!</h3>
                    <p>Ask me anything about Python programming, and I'll help you out.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.messages:
                role = msg["role"]
                content = msg["content"]

                with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🤖"):
                    st.markdown(content)

with col_examples:
    st.markdown("### 📚 Example Queries")

    example_queries = [
        "How do I read a CSV file?",
        "Explain list comprehensions",
        "Create a simple class example",
        "What are decorators?",
        "Show me async/await usage",
        "How to handle exceptions?",
        "Explain lambda functions",
        "Create a REST API example"
    ]

    for query in example_queries:
        if st.button(f"💡 {query}", key=query, use_container_width=True):
            st.session_state.example_clicked = query

# -------------------- Chat Input --------------------
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

# Check for example click
if "example_clicked" in st.session_state:
    user_input = st.session_state.example_clicked
    del st.session_state.example_clicked
else:
    user_input = st.chat_input("💭 Ask anything about Python...", key="chat_input")

# -------------------- Process User Input --------------------
if user_input:
    # Increment query counter
    st.session_state.total_queries += 1

    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message immediately
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    # Generate response
    if api_loaded:
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Call GROQ API
                    response = client.chat.completions.create(
                        model=model_option,
                        messages=st.session_state.messages,
                        temperature=0.7,
                        max_tokens=2048
                    )

                    bot_reply = response.choices[0].message.content

                    # Store assistant message
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                    # Display response
                    st.markdown(bot_reply)

                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    else:
        with st.chat_message("assistant", avatar="🤖"):
            fallback_msg = "⚠️ GROQ API is not configured. Please add your API key to continue."
            st.warning(fallback_msg)
            st.session_state.messages.append({"role": "assistant", "content": fallback_msg})

    # Rerun to update chat display
    st.rerun()

# -------------------- Features Section --------------------
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
st.markdown("### 🌟 Key Features")

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>⚡</div>
            <div class='feature-title'>Lightning Fast</div>
            <div class='feature-desc'>Powered by GROQ's ultra-fast inference engine</div>
        </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🧠</div>
            <div class='feature-title'>Smart Responses</div>
            <div class='feature-desc'>Advanced LLaMA 3.1 model for accurate answers</div>
        </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>💻</div>
            <div class='feature-title'>Code Examples</div>
            <div class='feature-desc'>Get working Python code with explanations</div>
        </div>
    """, unsafe_allow_html=True)

# -------------------- Footer --------------------
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p style='font-size: 0.9rem;'>Made with ❤️ using Streamlit & GROQ | Powered by LLaMA 3.1</p>
        <p style='font-size: 0.8rem;'>© 2024 Python AI Assistant. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
st.markdown("""<div style='text-align: center; font-weight: bold; font-size: 1rem; padding: 10px;'>
    Prepared by M. Aqib Javed
</div>""", unsafe_allow_html=True)
