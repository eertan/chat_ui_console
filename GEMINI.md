
# GEMINI.md: Agentic GUI Implementation Guide

## 1. Project Overview

**Goal:** Build a conversational GUI for a Python-based intelligent agent using **Streamlit**.
**Core Requirement:** The UI must visually distinguish between "Reasoning/Thinking" (internal operations) and "Conversational Output" while maintaining strict chronological order.
**Mechanism:** Intercept `sys.stdout` to dynamically generate Streamlit chat elements (`st.status` and `st.chat_message`) based on specific console prefixes.

## 2. Technical Stack

* **Frontend:** Streamlit
* **Agent Logic:** (Already built—this wrapper is non-intrusive)
* **Icons:** Material Design Symbols (`:material/psychology:`, `:material/smart_toy:`, `:material/person:`)

## 3. The "Thinking" Protocol

The coding agent uses a redirection layer that parses the following console triggers:

| Console Prefix | UI Action |
| --- | --- |
| `PHASE:` | Creates a new collapsible `st.status` block (e.g., `PHASE: Analyzing Graph`) |
| `SAY:` | Creates a final `st.chat_message` response from the agent |
| *Standard Print* | Streams as a log inside the current active "Thinking" block |

## 4. Implementation Blueprint

### The Integration Module (`streamlit_agent_ui.py`)

This reusable module allows any script to pipe its output into the Streamlit UI.

```python
from streamlit_agent_ui import capture_agent_output, apply_custom_css

# inside your app loop:
with capture_agent_output():
    my_agent.run(prompt)
```

### The Stream Logic

The `StreamlitThinkingStream` class handles the state machine:
- **Thinking Mode**: Activated by `PHASE:`. Content goes into an `st.status` container with a Brain icon. Labels are styled gray/italic.
- **Speaking Mode**: Activated by `SAY:`. Content goes into an `st.chat_message` container with a Robot icon.

## 5. Coding Agent Instructions

1.  **Isolation**: The UI logic is isolated in `streamlit_agent_ui.py`.
2.  **State Management**: Streamlit handles history in `st.session_state`.
3.  **Aesthetics**: Use `apply_custom_css()` to ensure status widgets are distinct.


## 6. Example Usage in Agent Code

When writing your agent logic, use this format to control the GUI:

```python
print("PHASE: Personalizing for Data Science Context")
print("INFO: Scanning user preferences...")
print("INFO: Matching ontology nodes for 'Pydantic Graph'")

print("PHASE: Reasoning")
print("DEBUG: Conflict detected at node 0x45. Resolving...")

```


