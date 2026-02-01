import streamlit as st
import time

st.set_page_config(page_title="Streamlit Thinking Demo")

st.title("Streamlit Alternative Demo")
st.markdown("This demonstrates `st.status` which is designed for exactly what you want: collapsible, chronological thinking steps.")

# Custom CSS to make the status widget (thinking block) more distinct/visible
st.markdown("""
<style>
    /* Target the status widget container */
    [data-testid="stStatusWidget"] {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #f9f9f9;
        padding: 10px;
        margin-bottom: 10px;
    }
    /* Dark mode adjustments (optional, assuming light mode for now) */
    @media (prefers-color-scheme: dark) {
        [data-testid="stStatusWidget"] {
            border: 1px solid #444;
            background-color: #222;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is the weather?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 1. FIRST THINKING BLOCK (Brain Avatar)
    with st.chat_message("assistant", avatar="🧠"):
        with st.status(":grey[*Analyzing input...*]", expanded=False) as status:
            st.write("Log: Scanning intent...")
            time.sleep(0.5)
            st.write(f"Log: identified entity '{prompt}'")
            status.update(label=":grey[*Analysis Complete*]", state="complete")

    # 2. FIRST UTTERANCE (Robot Avatar)
    response_1 = "I'm checking that for you..."
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response_1)
    # Store just the visible text for history (simplification for demo)
    st.session_state.messages.append({"role": "assistant", "content": response_1})
    
    # 3. SECOND THINKING BLOCK (Brain Avatar)
    with st.chat_message("assistant", avatar="🧠"):
        with st.status(":grey[*Database Query*]", expanded=False) as status:
            st.write("Connecting to weather_db...")
            time.sleep(0.5)
            st.code("SELECT * FROM weather WHERE location = 'Berlin'")
            status.update(label=":grey[*Query Realized*]", state="complete")

    # 4. FINAL RESPONSE (Robot Avatar)
    final_answer = "The weather is currently 22°C and sunny."
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(final_answer)
    st.session_state.messages.append({"role": "assistant", "content": final_answer})
