import streamlit as st
import time
from streamlit_agent_ui import capture_agent_output, apply_custom_css

st.set_page_config(page_title="Agent UI Module Demo")
st.title("Streamlit Agent UI Module")

# Apply the custom styles
apply_custom_css()

# --- THE MOCK AGENT ---
# This represents your existing agent code. 
# It knows nothing about Streamlit. It just prints.
def my_agent_logic(user_input):
    print(f"PHASE: Analysis")
    print(f"Log: interpreting '{user_input}'")
    time.sleep(0.5)
    print("Log: checking context window...")
    time.sleep(0.5)
    
    # Utterance
    print("SAY: I'm checking that for you...")
    
    print(f"PHASE: Tool Execution")
    print("Log: Tool 'weather_api' selected")
    time.sleep(0.5)
    print("Log: Calling API endpoint...")
    time.sleep(0.5)
    
    print("SAY: The weather is 22°C and sunny.")

# --- THE APP LOOP ---

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

if prompt := st.chat_input("Say something..."):
    # User message
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "avatar": ":material/person:", "content": prompt})

    # Run the agent with UI capture
    # note: the capturing handles the rendering of the intermediate steps
    with capture_agent_output():
        my_agent_logic(prompt)
    
    # The agent logic above printed the responses. 
    # If we want to store the final responses in history, we'd need to capture them.
    # For this simplified wrapper, the rendering happens in real-time.
    # To persist history, the agent usually returns the final string or we'd enhance the wrapper 
    # to return the list of "SAY" items it captured.
    
    # For now, we manually append what we know the agent said to keep history consistent on reload
    st.session_state.messages.append({"role": "assistant", "avatar": ":material/smart_toy:", "content": "I'm checking that for you..."})
    st.session_state.messages.append({"role": "assistant", "avatar": ":material/smart_toy:", "content": "The weather is 22°C and sunny."})
