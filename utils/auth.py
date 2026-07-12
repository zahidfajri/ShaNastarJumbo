import streamlit as st


def login_user(user):
    st.session_state.logged_in = True
    st.session_state.user_id = user["id"]
    st.session_state.username = user["username"]
    st.session_state.full_name = user["full_name"]
    st.session_state.role = user["role"]


def logout_user():
    st.session_state.clear()


def is_logged_in():
    return st.session_state.get(
        "logged_in",
        False
    )


def is_owner():
    return st.session_state.get(
        "role"
    ) == "OWNER"