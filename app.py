"""
Root launcher for FACTS Topic Opportunity Scout Streamlit Dashboard.
Allows running `streamlit run app.py` directly from the repository root.
"""

import os
import sys

CHALLENGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Challenge 1: FACTS Topic Opportunity Scout")
sys.path.insert(0, CHALLENGE_DIR)

# Execute the main application
app_path = os.path.join(CHALLENGE_DIR, "app.py")
with open(app_path, "r", encoding="utf-8") as f:
    code = compile(f.read(), app_path, 'exec')
    exec(code, globals())

