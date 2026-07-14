from datetime import datetime

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

        (
            supabase
            .table("products")
            .update({
                "current_stock": after_stock
            })
            .eq("id", item["product_id"])
            .execute()
        )

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


# ==================================
# DELETE (SOFT DELETE) SALE
# ==================================

def delete_sale(
    sale_id: str,
    deleted_by: str
):
    """
    Soft delete a sale.

    - Prevent double delete
    - Restore product stock
    - Create inventory audit log
    - Mark sale as deleted
    """

    # ==================================
    # PREVENT DOUBLE DELETE
    # ==================================

    sale_response = (
        supabase
        .table("sales")
        .select("is_deleted")
        .eq("id", sale_id)
        .single()
        .execute()
    )

    if sale_response.data["is_deleted"]:
        raise Exception(
            "Transaction has already been deleted."
        )

    # ==================================
    # LOAD SALE ITEMS
    # ==================================

    items_response = (
        supabase
        .table("sales_items")
        .select("""
            *,
            products (
                current_stock,
                name
            )
        """)
        .eq("sale_id", sale_id)
        .execute()
    )

    sale_items = items_response.data

    # ==================================
    # RESTORE STOCK
    # ==================================

    for item in sale_items:

        before_stock = (
            item["products"]["current_stock"]
        )

        after_stock = (
            before_stock + item["quantity"]
        )

        (
            supabase
            .table("products")
            .update({
                "current_stock": after_stock
            })
            .eq(
                "id",
                item["product_id"]
            )
            .execute()
        )

        (
            supabase
            .table("inventory_logs")
            .insert({
                "product_id": item["product_id"],
                "action": "VOID_SALE",
                "quantity": item["quantity"],
                "before_stock": before_stock,
                "after_stock": after_stock,
                "user_id": deleted_by,
                "notes": f"Deleted transaction {sale_id}"
            })
            .execute()
        )

    # ==================================
    # SOFT DELETE SALE
    # ==================================

    (
        supabase
        .table("sales")
        .update({
            "is_deleted": True,
            "deleted_at": datetime.utcnow().isoformat(),
            "deleted_by": deleted_by
        })
        .eq("id", sale_id)
        .execute()
    )

    return True


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
        .eq(
            "is_deleted",
            False
        )
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
        .eq(
            "is_deleted",
            False
        )
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return response.data
