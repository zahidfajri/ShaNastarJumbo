from database.connection import supabase


def get_all_categories():
    response = (
        supabase
        .table("categories")
        .select("*")
        .order("name")
        .execute()
    )

    return response.data


def create_category(name: str):
    return (
        supabase
        .table("categories")
        .insert({
            "name": name.strip()
        })
        .execute()
    )