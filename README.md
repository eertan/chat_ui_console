# Agent UI with Chainlit

This project implements a Streamlit-based GUI for a Python agent, featuring a "Thinking" protocol that visually distinguishes internal reasoning from conversational output.

## Setup

Ensure you have [uv](https://github.com/astral-sh/uv) installed.

1.  **Install dependencies:**
    ```bash
    uv sync
    ```

## Running the Application

To start the Streamlit UI:

```bash
uv run streamlit run app.py
```

*   The `-w` flag enables auto-reloading on file changes.

## Features

*   **Thinking Stream:** Intercepts `stdout` to display internal agent steps (`PHASE:`, `INFO:`, `DEBUG:`) as UI elements.
*   **Dummy Agent:** Includes a mock agent to demonstrate the UI capabilities.

## Project Structure

*   `main.py`: Main application entry point containing the `ChainlitThinkingStream` class and agent logic.
*   `GEMINI.md`: Implementation guide and protocol definition.
