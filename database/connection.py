from pathlib import Path

import streamlit as st
from dotenv import dotenv_values
from supabase import create_client

# =====================================
# LOAD LOCAL .ENV
# =====================================

ENV_PATH = (
    Path(__file__).resolve().parent.parent
    / ".env"
)

config = dotenv_values(ENV_PATH)

# =====================================
# LOAD SUPABASE CREDENTIALS
# =====================================

try:

    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

except Exception:

    SUPABASE_URL = config["SUPABASE_URL"]
    SUPABASE_KEY = config["SUPABASE_KEY"]

# =====================================
# CREATE CLIENT
# =====================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)