
# GEMINI.md: Agentic GUI Implementation Guide

## 1. Project Overview

**Goal:** Build a conversational GUI for a Python-based intelligent agent using **Chainlit**.
**Core Requirement:** The UI must visually distinguish between "Reasoning/Thinking" (internal operations) and "Conversational Output."
**Mechanism:** Intercept `sys.stdout` to dynamically generate UI "Steps" based on specific console prefixes.

## 2. Technical Stack

* **Backend:** Python 3.10+
* **Frontend:** Chainlit (React-based Python Framework)
* **Agent Logic:** (Already built—this wrapper must be non-intrusive)

## 3. The "Thinking" Protocol

The coding agent must implement a redirection layer that parses the following console triggers:

| Console Prefix | UI Action |
| --- | --- |
| `PHASE:` | Creates a new high-level Step/Title (e.g., `PHASE: Analyzing Graph`) |
| `INFO:` | Streams as a standard log inside the current step |
| `DEBUG:` | (Optional) Streams as a code block within the step |
| *Standard Print* | Defaults to "Process Log" inside the active step |

## 4. Implementation Blueprint

### A. The Interceptor Class

This class wraps `io.StringIO` to handle the real-time UI updates within the Chainlit event loop.

```python
import sys
import io
import chainlit as cl

class ChainlitThinkingStream(io.StringIO):
    def __init__(self):
        super().__init__()
        self.active_step = None

    def write(self, data):
        clean_data = data.strip()
        if not clean_data: return

        if clean_data.startswith("PHASE:"):
            title = clean_data.replace("PHASE:", "").strip()
            # Close/Remove old step if necessary and start new
            self.active_step = cl.Step(name=title, type="run")
            cl.run_sync(self.active_step.send())
        else:
            if self.active_step:
                # Stream the details into the toggleable section
                cl.run_sync(self.active_step.stream_token(f"{clean_data}\n"))
        
        return super().write(data)

```

### B. The Integration Wrapper

Ensure the agent logic is wrapped in a `try...finally` block to prevent `stdout` from staying hijacked if the agent crashes.

```python
@cl.on_message
async def on_message(message: cl.Message):
    # Setup the thinking UI
    thinking_ui = ChainlitThinkingStream()
    original_stdout = sys.stdout
    sys.stdout = thinking_ui

    try:
        # EXECUTE YOUR AGENT HERE
        # Example: response = await my_agent.run(message.content)
        pass 
    finally:
        # Always restore console output
        sys.stdout = original_stdout

```

## 5. Coding Agent Instructions

1. **Isolation:** Do not modify the core agent logic. Only modify the entry point where the agent is called.
2. **State Management:** Ensure that each user message generates a fresh set of UI steps.
3. **Formatting:** Use Markdown within the `stream_token` calls to make logs scannable (e.g., wrap JSON in code blocks).
4. **Aesthetics:** Default the steps to a "collapsed" state unless a critical error occurs.

## 6. Example Usage in Agent Code

When writing your agent logic, use this format to control the GUI:

```python
print("PHASE: Personalizing for Data Science Context")
print("INFO: Scanning user preferences...")
print("INFO: Matching ontology nodes for 'Pydantic Graph'")

print("PHASE: Reasoning")
print("DEBUG: Conflict detected at node 0x45. Resolving...")

```


