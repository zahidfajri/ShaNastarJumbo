from database.connection import supabase


def add_production(
    product_id: str,
    quantity: int,
    user_id: str
):
    # Get current product
    product_response = (
        supabase
        .table("products")
        .select("*")
        .eq("id", product_id)
        .single()
        .execute()
    )

    product = product_response.data

    before_stock = product["current_stock"]
    after_stock = before_stock + quantity

    # Update stock
    (
        supabase
        .table("products")
        .update({
            "current_stock": after_stock
        })
        .eq("id", product_id)
        .execute()
    )

    # Production log
    (
        supabase
        .table("production_logs")
        .insert({
            "product_id": product_id,
            "quantity_added": quantity,
            "created_by": user_id
        })
        .execute()
    )

    # Inventory log
    (
        supabase
        .table("inventory_logs")
        .insert({
            "product_id": product_id,
            "action": "PRODUCTION",
            "quantity": quantity,
            "before_stock": before_stock,
            "after_stock": after_stock,
            "user_id": user_id,
            "notes": "Daily production input"
        })
        .execute()
    )


def get_today_production():

    response = (
        supabase
        .table("production_logs")
        .select("""
            *,
            products (
                name
            )
        """)
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return response.data


def adjust_inventory(
    product_id: str,
    adjustment_type: str,
    quantity: int,
    reason: str,
    user_id: str
):

    product_response = (
        supabase
        .table("products")
        .select("*")
        .eq("id", product_id)
        .single()
        .execute()
    )

    product = product_response.data

    before_stock = product["current_stock"]

    if adjustment_type == "ADD":

        after_stock = before_stock + quantity
        inventory_quantity = quantity

    else:

        if quantity > before_stock:
            raise Exception(
                "Cannot reduce more than current stock."
            )

        after_stock = before_stock - quantity
        inventory_quantity = -quantity

    # Update stock
    (
        supabase
        .table("products")
        .update({
            "current_stock": after_stock
        })
        .eq("id", product_id)
        .execute()
    )

    # Inventory log
    (
        supabase
        .table("inventory_logs")
        .insert({
            "product_id": product_id,
            "action": "ADJUSTMENT",
            "quantity": inventory_quantity,
            "before_stock": before_stock,
            "after_stock": after_stock,
            "user_id": user_id,
            "notes": reason
        })
        .execute()
    )


def get_recent_inventory_logs():

    response = (
        supabase
        .table("inventory_logs")
        .select("""
            *,
            products (
                name
            )
        """)
        .order(
            "created_at",
            desc=True
        )
        .limit(20)
        .execute()
    )

    return response.data