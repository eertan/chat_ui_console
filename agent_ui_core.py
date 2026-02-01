import sys
import io
import builtins
import contextlib
import threading
import asyncio
import chainlit as cl

class ChainlitThinkingStream(io.StringIO):
    """
    IO Stream that intercepts writes and converts them into Chainlit Messages 
    using sorted, collapsible Markdown blocks.
    """
    def __init__(self):
        super().__init__()
        self.buffer = []
        self.current_phase = "Thinking"

    def flush_buffer(self):
        """Sends the logs as a formatted Message."""
        if not self.buffer:
            return

        logs = "\n".join(self.buffer)
        
        # Strict Markdown Formatting to ensure rendering:
        # 1. Blockquote for the Title (Subtle)
        # 2. Blank lines before/after HTML tags
        # 3. Code block for logs inside details
        content = f"""> 🧠 **{self.current_phase}**

<details>
<summary>View Logs</summary>

```text
{logs}
```

</details>"""
        
        cl.run_sync(
            cl.Message(
                content=content,
                author="System"
            ).send()
        )
        self.buffer = []

    def write(self, data):
        if not data: return
        try:
            lines = data.split('\n')
            for line in lines:
                clean_line = line.strip()
                if not clean_line: continue

                if clean_line.startswith("PHASE:"):
                    self.flush_buffer()
                    self.current_phase = clean_line.replace("PHASE:", "").strip()
                elif clean_line.startswith("SAY:"):
                    self.flush_buffer()
                    content = clean_line.replace("SAY:", "").strip()
                    cl.run_sync(cl.Message(content=content).send())
                else:
                    self.buffer.append(clean_line)
        except Exception:
            pass
        return super().write(data)

    def close(self):
        self.flush_buffer()
        super().close()

# --- PUBLIC HELPERS ---

def flush_thinking():
    if isinstance(sys.stdout, ChainlitThinkingStream):
        sys.stdout.flush_buffer()

def update_thinking_parent(message):
    """No-op: Chronological mode doesn't need parenting."""
    pass

@contextlib.contextmanager
def capture_agent_output(message=None):
    thinking_ui = ChainlitThinkingStream()
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = thinking_ui
    sys.stderr = thinking_ui
    try:
        yield
    finally:
        thinking_ui.close()
        sys.stdout = original_stdout
        sys.stderr = original_stderr