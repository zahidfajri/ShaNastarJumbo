import streamlit as st

from utils.sidebar import render_sidebar


def require_login():

    if not st.session_state.get(
        "logged_in",
        False
    ):

        st.warning(
            "Please login first."
        )

        st.stop()

    render_sidebar()


def require_owner():

    require_login()

    if st.session_state.get(
        "role"
    ) != "OWNER":

        st.error(
            "Access denied."
        )

        st.stop()