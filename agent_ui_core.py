import sys
import io
import builtins
import contextlib
import threading
import asyncio
import chainlit as cl

class ChainlitThinkingStream(io.StringIO):
    """
    IO Stream that intercepts writes and converts them into Chainlit Messages.
    Uses 'author' and markdown styling to distinguish 'Thinking' from 'Talking'.
    """
    def __init__(self):
        super().__init__()
        self.buffer = []
        self.current_phase = "Log"

    def flush_buffer(self):
        """Sends the accumulated log lines as a single 'Thought' message."""
        if not self.buffer:
            return

        content = "\n".join(self.buffer)
        
        # Simplified Styling: Header + Code Block
        formatted_content = f"**{self.current_phase}**\n```text\n{content}\n```"
        
        cl.run_sync(
            cl.Message(
                content=formatted_content, 
                author="Thinking Process"
            ).send()
        )
        self.buffer = []

    def write(self, data):
        if not data: return

        lines = data.split('\n')
        
        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue

            # 1. Check for PHASE (New Thought Block)
            if clean_line.startswith("PHASE:"):
                # Flush previous logs
                self.flush_buffer()
                self.current_phase = clean_line.replace("PHASE:", "").strip()
            
            # 2. Check for SAY (Direct Chat Message - Console Mode)
            elif clean_line.startswith("SAY:"):
                self.flush_buffer() # Finish thinking
                content = clean_line.replace("SAY:", "").strip()
                cl.run_sync(cl.Message(content=content).send())

            # 3. Default: Accumulate logs
            else:
                self.buffer.append(clean_line)
        
        return super().write(data)

    def close(self):
        self.flush_buffer()
        super().close()

# --- PUBLIC HELPERS ---

def flush_thinking():
    """Forces the current accumulated thinking logs to be sent to the UI immediately."""
    if isinstance(sys.stdout, ChainlitThinkingStream):
        sys.stdout.flush_buffer()

@contextlib.contextmanager
def capture_agent_output(message=None):
    """
    Redirects stdout/stderr to Chainlit UI.
    """
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
