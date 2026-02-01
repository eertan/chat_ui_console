import sys
import io
import time
import contextlib
import streamlit as st

class StreamlitThinkingStream(io.StringIO):
    """
    IO Stream that intercepts writes and converts them into Streamlit UI elements.
    - PHASE: ... -> Starts a collapsible 'Brain' block.
    - SAY: ...   -> Starts a 'Robot' block.
    - Logs       -> Written inside the active Brain block.
    """
    def __init__(self):
        super().__init__()
        self.active_status = None  # The st.status object
        self.active_status_label = None # To track name for updates
        
        # We need to buffer partial lines for robust token handling
        self.line_buffer = ""

    def write(self, data):
        if not data: return
        
        # Handle partial writes by buffering
        self.line_buffer += data
        if '\n' not in self.line_buffer:
            return
            
        lines = self.line_buffer.split('\n')
        # The last part might be incomplete, keep it in buffer
        self.line_buffer = lines.pop() 
        
        for line in lines:
            clean_line = line.strip()
            if not clean_line: continue

            if clean_line.startswith("PHASE:"):
                # Complete previous status if needed
                if self.active_status:
                    self.active_status.update(label=f":grey[*{self.active_status_label}*]", state="complete")
                    self.active_status = None
                
                title = clean_line.replace("PHASE:", "").strip()
                self.active_status_label = title
                
                # Start new block
                with st.chat_message("assistant", avatar=":material/psychology:"):
                    # We create the status object and hold a reference to it
                    self.active_status = st.status(f":grey[*{title}*]", expanded=False)
                    
            elif clean_line.startswith("SAY:"):
                 # Complete previous status
                if self.active_status:
                    self.active_status.update(label=f":grey[*{self.active_status_label}*]", state="complete")
                    self.active_status = None
                    
                content = clean_line.replace("SAY:", "").strip()
                with st.chat_message("assistant", avatar=":material/smart_toy:"):
                    st.markdown(content)
                    # We also act as a side-effect to session state for history if needed?
                    # Ideally the calling app handles history appending, 
                    # but here we are just rendering the stream.
                    
            else:
                # Log line
                if self.active_status:
                    # To write INTO the status container from outside the 'with',
                    # we can use `self.active_status.write()`.
                    self.active_status.write(line)
                else:
                    # Fallback if no phase active
                    with st.chat_message("assistant", avatar=":material/psychology:"):
                         st.write(line)

    def close(self):
        if self.active_status:
            self.active_status.update(label=f":grey[*{self.active_status_label}*]", state="complete")
        super().close()


def apply_custom_css():
    st.markdown("""
    <style>
        [data-testid="stStatusWidget"] {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background-color: #f9f9f9;
            padding: 10px;
            margin-bottom: 10px;
        }
        @media (prefers-color-scheme: dark) {
            [data-testid="stStatusWidget"] {
                border: 1px solid #444;
                background-color: #222;
            }
        }
    </style>
    """, unsafe_allow_html=True)


@contextlib.contextmanager
def capture_agent_output():
    ui_stream = StreamlitThinkingStream()
    original_stdout = sys.stdout
    sys.stdout = ui_stream
    try:
        yield
    finally:
        ui_stream.close()
        sys.stdout = original_stdout
