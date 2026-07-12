import streamlit as st

from utils.auth import logout_user


def render_sidebar():

    with st.sidebar:

        st.title("🍍 Sha Nastar Jumbo")

        st.write(
            f"👋 {st.session_state.full_name}"
        )

        st.caption(
            f"Role: {st.session_state.role}"
        )

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout_user()

            st.switch_page(
                "app.py"
            )