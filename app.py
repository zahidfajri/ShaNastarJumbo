import streamlit as st

from database.user_service import (
    get_user_by_username,
    verify_password
)

from utils.auth import (
    login_user,
    is_logged_in
)


st.set_page_config(
    page_title="Sha Nastar Jumbo",
    page_icon="🍍",
    layout="wide"
)


# =====================================
# LOGIN PAGE
# =====================================

if not is_logged_in():

    st.title("🍍 Sha Nastar Jumbo")

    st.caption(
        "Bakery Management System"
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        user = get_user_by_username(
            username
        )

        if user and verify_password(
            password,
            user["password_hash"]
        ):

            login_user(user)

            st.rerun()

        else:

            st.error(
                "Invalid username or password"
            )


# =====================================
# HOME PAGE
# =====================================

else:

    st.title("🍍 Sha Nastar Jumbo")

    st.success(
        f"Welcome, {st.session_state.full_name}!"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"Role: {st.session_state.role}"
        )

    with col2:

        st.info(
            f"User: {st.session_state.username}"
        )

    st.divider()

    st.write(
        """
        ### Welcome to the Bakery Management System

        Use the sidebar to access:

        - 📊 Dashboard
        - 🛒 Sales
        - 🍍 Production
        - 📦 Inventory
        - 📋 Products
        - 📈 Reports
        - 🧾 Transaction History
        - 👥 User Management (Owner only)

        You can logout anytime using the **🚪 Logout** button in the sidebar.
        """
    )