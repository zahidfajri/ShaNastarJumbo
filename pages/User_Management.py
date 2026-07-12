import streamlit as st

from utils.page_guard import require_login

from database.user_service import (
    get_all_users,
    create_staff_user,
    deactivate_user,
    activate_user
)


require_login()

# ==================================
# OWNER ONLY ACCESS
# ==================================

if st.session_state.role != "OWNER":

    st.error(
        "Only owners can access this page."
    )

    st.stop()


# ==================================
# PAGE TITLE
# ==================================

st.title("👥 User Management")


# ==================================
# ADD NEW STAFF
# ==================================

with st.expander("➕ Add New Staff"):

    with st.form("create_staff_form"):

        full_name = st.text_input(
            "Full Name"
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Staff"
        )

    if submitted:

        try:

            if not full_name.strip():
                st.error(
                    "Full name cannot be empty."
                )

            elif not username.strip():
                st.error(
                    "Username cannot be empty."
                )

            elif len(password) < 6:
                st.error(
                    "Password must be at least 6 characters."
                )

            else:

                create_staff_user(
                    username=username,
                    password=password,
                    full_name=full_name
                )

                st.success(
                    "Staff created successfully!"
                )

                st.rerun()

        except Exception as e:

            st.error(str(e))


# ==================================
# USER LIST
# ==================================

st.divider()

st.subheader("Current Users")

users = get_all_users()

for user in users:

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(
                f"**{user['full_name']}**"
            )

            st.write(
                f"Username: {user['username']}"
            )

            st.write(
                f"Role: {user['role']}"
            )

            status = (
                "🟢 Active"
                if user["is_active"]
                else "🔴 Inactive"
            )

            st.write(
                f"Status: {status}"
            )

        with col2:

            # Owner cannot deactivate themselves
            if user["role"] == "OWNER":

                st.button(
                    "Protected",
                    disabled=True,
                    key=f"owner_{user['id']}"
                )

            else:

                if user["is_active"]:

                    if st.button(
                        "Deactivate",
                        key=f"deactivate_{user['id']}"
                    ):

                        try:

                            deactivate_user(
                                user["id"]
                            )

                            st.success(
                                "User deactivated."
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(str(e))

                else:

                    if st.button(
                        "Activate",
                        key=f"activate_{user['id']}"
                    ):

                        activate_user(
                            user["id"]
                        )

                        st.success(
                            "User activated."
                        )

                        st.rerun()