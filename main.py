import chainlit as cl
import asyncio
import sys
from agent_ui_core import capture_agent_output, flush_thinking, update_thinking_parent

async def my_soar_agent(user_message: str):
    # 1. THINKING (Attached to User Prompt)
    print(f"PHASE: Analyzing input")
    print(f"INFO: User said: {user_message}")
    await asyncio.sleep(0.5)
    
    # 2. UTTERANCE
    flush_thinking() # Stop the current step
    msg = cl.Message(content="I'm checking that for you...")
    await msg.send()
    
    # Update the parent so the next phase attaches to this new bubble
    update_thinking_parent(msg)
    
    # 3. MORE THINKING (Attached to the "I'm checking" bubble)
    print("PHASE: Database Query")
    print("INFO: Connecting to weather_db...")
    await asyncio.sleep(0.5)
    
    return "The weather is currently 22°C and sunny."

@cl.on_message
async def on_message(message: cl.Message):
    # Pass 'message' to anchor initial thinking to the user input
    with capture_agent_output(message=message):
        final_response = await my_soar_agent(message.content)
        
    await cl.Message(content=final_response).send()

if __name__ == "__main__":
    pass