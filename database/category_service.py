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
    
def get_products_by_category(
    category_id: str
):

    response = (
        supabase
        .table("products")
        .select(
            "id, name"
        )
        .eq(
            "category_id",
            category_id
        )
        .execute()
    )

    return response.data


def delete_category(
    category_id: str
):

    products = get_products_by_category(
        category_id
    )

    if products:

        names = ", ".join(
            product["name"]
            for product in products
        )

        raise Exception(
            f"Category is still used by: {names}"
        )

    return (
        supabase
        .table("categories")
        .delete()
        .eq(
            "id",
            category_id
        )
        .execute()
    )