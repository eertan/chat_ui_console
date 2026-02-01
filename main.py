import chainlit as cl
import asyncio
import sys
from agent_ui_core import capture_agent_output, flush_thinking

async def my_soar_agent(user_message: str):
    # 1. THINKING 
    print(f"PHASE: Analyzing input")
    print(f"INFO: User said: {user_message}")
    print("DEBUG: Checking production rules...")
    await asyncio.sleep(0.8)
    
    # 2. UTTERANCE
    # flush_thinking() marks the current step as done so the bubble comes next
    flush_thinking()
    await cl.Message(content="I'm checking that for you...").send()
    
    # 3. MORE THINKING 
    print("PHASE: Database Query")
    print("INFO: Connecting to weather_db...")
    print("DEBUG: SQL: SELECT * FROM weather WHERE city='Paris'")
    await asyncio.sleep(0.8)
    
    # 4. FINAL UTTERANCE
    return "The weather is currently 22°C and sunny."

@cl.on_message
async def on_message(message: cl.Message):
    with capture_agent_output():
        final_response = await my_soar_agent(message.content)
        
    await cl.Message(content=final_response).send()
