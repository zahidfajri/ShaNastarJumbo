from database.connection import supabase


def get_all_products(active_only=True):

    query = (
        supabase
        .table("products")
        .select("""
            *,
            categories (
                id,
                name
            )
        """)
        .order("name")
    )

    if active_only:

        query = query.eq(
            "is_active",
            True
        )

    response = query.execute()

    return response.data

# =====================================
# FIND PRODUCT BY NAME
# =====================================

def get_product_by_name(
    name: str
):

    response = (
        supabase
        .table("products")
        .select("*")
        .ilike(
            "name",
            name.strip()
        )
        .limit(1)
        .execute()
    )

    if response.data:

        return response.data[0]

    return None

def create_product(
    name: str,
    category_id: str,
    price: int,
    minimum_stock: int,
    created_by: str
):

    return (
        supabase
        .table("products")
        .insert({
            "name": name.strip(),
            "category_id": category_id,
            "price": price,
            "minimum_stock": minimum_stock,
            "created_by": created_by
        })
        .execute()
    )


def update_product(
    product_id: str,
    name: str,
    category_id: str,
    price: int,
    minimum_stock: int
):

    return (
        supabase
        .table("products")
        .update({
            "name": name.strip(),
            "category_id": category_id,
            "price": price,
            "minimum_stock": minimum_stock
        })
        .eq("id", product_id)
        .execute()
    )


def deactivate_product(
    product_id: str
):

    return (
        supabase
        .table("products")
        .update({
            "is_active": False
        })
        .eq(
            "id",
            product_id
        )
        .execute()
    )
    
# =====================================
# INACTIVE PRODUCTS
# =====================================

def get_inactive_products():

    response = (
        supabase
        .table("products")
        .select("""
            *,
            categories (
                id,
                name
            )
        """)
        .eq(
            "is_active",
            False
        )
        .order("name")
        .execute()
    )

    return response.data

# =====================================
# RESTORE PRODUCT
# =====================================

def restore_product(
    product_id: str
):

    return (
        supabase
        .table("products")
        .update({
            "is_active": True
        })
        .eq(
            "id",
            product_id
        )
        .execute()
    )