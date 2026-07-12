from database.connection import supabase


def process_sale(
    cart_items: list,
    payment_method: str,
    staff_id: str
):
    """
    cart_items:
    [
        {
            "product_id": "...",
            "name": "...",
            "quantity": 2,
            "price": 25000
        }
    ]
    """

    total_amount = 0

    # ==================================
    # VALIDATE STOCK
    # ==================================

    for item in cart_items:

        product_response = (
            supabase
            .table("products")
            .select("*")
            .eq("id", item["product_id"])
            .single()
            .execute()
        )

        product = product_response.data

        if product["current_stock"] < item["quantity"]:
            raise Exception(
                f"Not enough stock for {product['name']}"
            )

        total_amount += (
            item["quantity"] * item["price"]
        )

    # ==================================
    # CREATE SALE
    # ==================================

    sale_response = (
        supabase
        .table("sales")
        .insert({
            "staff_id": staff_id,
            "payment_method": payment_method,
            "total_amount": total_amount
        })
        .execute()
    )

    sale_id = sale_response.data[0]["id"]

    # ==================================
    # CREATE SALES ITEMS
    # UPDATE STOCK
    # CREATE INVENTORY LOGS
    # ==================================

    for item in cart_items:

        product_response = (
            supabase
            .table("products")
            .select("*")
            .eq("id", item["product_id"])
            .single()
            .execute()
        )

        product = product_response.data

        before_stock = product["current_stock"]

        after_stock = (
            before_stock - item["quantity"]
        )

        subtotal = (
            item["quantity"] * item["price"]
        )

        # Sales item
        (
            supabase
            .table("sales_items")
            .insert({
                "sale_id": sale_id,
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "price": item["price"],
                "subtotal": subtotal
            })
            .execute()
        )

        # Update stock
        (
            supabase
            .table("products")
            .update({
                "current_stock": after_stock
            })
            .eq("id", item["product_id"])
            .execute()
        )

        # Inventory log
        (
            supabase
            .table("inventory_logs")
            .insert({
                "product_id": item["product_id"],
                "action": "SALE",
                "quantity": -item["quantity"],
                "before_stock": before_stock,
                "after_stock": after_stock,
                "user_id": staff_id,
                "notes": "Sales transaction"
            })
            .execute()
        )

    return total_amount


def get_recent_sales():

    response = (
        supabase
        .table("sales")
        .select("""
            *,
            sales_items (
                quantity,
                subtotal,
                products (
                    name
                )
            )
        """)
        .order(
            "created_at",
            desc=True
        )
        .limit(10)
        .execute()
    )

    return response.data


def get_all_sales():

    response = (
        supabase
        .table("sales")
        .select("""
            *,
            sales_items (
                quantity,
                subtotal,
                products (
                    name
                )
            )
        """)
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return response.data