import bcrypt

from database.connection import supabase


# ==================================
# AUTHENTICATION
# ==================================

def get_user_by_username(username: str):

    response = (
        supabase
        .table("app_users")
        .select("*")
        .eq("username", username)
        .eq("is_active", True)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def verify_password(
    password: str,
    password_hash: str
):

    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode()
    )


# ==================================
# USER MANAGEMENT
# ==================================

def get_all_users():

    response = (
        supabase
        .table("app_users")
        .select("*")
        .order(
            "created_at",
            desc=False
        )
        .execute()
    )

    return response.data


def create_staff_user(
    username: str,
    password: str,
    full_name: str
):

    # Check duplicate username
    existing_user = get_user_by_username(
        username
    )

    if existing_user:
        raise Exception(
            "Username already exists."
        )

    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    (
        supabase
        .table("app_users")
        .insert({
            "username": username,
            "password_hash": password_hash,
            "full_name": full_name,
            "role": "STAFF",
            "is_active": True
        })
        .execute()
    )


def deactivate_user(user_id: str):

    user_response = (
        supabase
        .table("app_users")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    user = user_response.data

    if user["role"] == "OWNER":
        raise Exception(
            "Owner account cannot be deactivated."
        )

    (
        supabase
        .table("app_users")
        .update({
            "is_active": False
        })
        .eq("id", user_id)
        .execute()
    )


def activate_user(user_id: str):

    (
        supabase
        .table("app_users")
        .update({
            "is_active": True
        })
        .eq("id", user_id)
        .execute()
    )