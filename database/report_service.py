from datetime import datetime, timezone

from database.connection import supabase

from utils.datetime_helper import (
    get_jakarta_today,
    to_jakarta_datetime
)

# =====================================
# USER LOOKUP
# =====================================

def get_user_lookup():

    response = (
        supabase
        .table("app_users")
        .select(
            "id, full_name"
        )
        .execute()
    )

    return {
        user["id"]: user["full_name"]
        for user in response.data
    }
    
# =====================================
# DASHBOARD
# =====================================

def get_today_sales_summary():

    response = (
        supabase
        .table("sales")
        .select("*")
        .eq(
            "is_deleted",
            False
        )
        .execute()
    )

    sales = response.data

    today = get_jakarta_today()

    today_sales = []

    for sale in sales:

        sale_date = to_jakarta_datetime(
            sale["created_at"]
        ).date()

        if sale_date == today:

            today_sales.append(
                sale
            )

    return {
        "transactions": len(
            today_sales
        ),
        "revenue": sum(
            sale["total_amount"]
            for sale in today_sales
        )
    }


def get_low_stock_products():

    response = (
        supabase
        .table("products")
        .select("*")
        .eq(
            "is_active",
            True
        )
        .order("name")
        .execute()
    )

    products = response.data

    return [
        product
        for product in products
        if product["current_stock"]
        <= product["minimum_stock"]
    ]


def get_best_seller_today():

    response = (
        supabase
        .table("sales_items")
        .select("""
            quantity,
            products (
                name
            ),
            sales (
                created_at,
                is_deleted
            )
        """)
        .execute()
    )

    items = response.data

    today = get_jakarta_today()

    product_totals = {}

    for item in items:
        
        if not item.get("sales"):

            continue

        if item["sales"].get(
            "is_deleted"
        ):
            continue

        sale_date = (
            to_jakarta_datetime(
                item["sales"]["created_at"]
            ).date()
        )

        if sale_date != today:
            continue

        product_name = item[
            "products"
        ]["name"]

        product_totals[
            product_name
        ] = (
            product_totals.get(
                product_name,
                0
            )
            + item["quantity"]
        )

    if not product_totals:
        return None

    best_product = max(
        product_totals,
        key=product_totals.get
    )

    return {
        "name": best_product,
        "quantity": product_totals[
            best_product
        ]
    }


def get_recent_dashboard_sales():

    response = (
        supabase
        .table("sales")
        .select("""
            id,
            payment_method,
            total_amount,
            created_at,
            sales_items (
                quantity,
                products (
                    name
                )
            )
        """)
        .order(
            "created_at",
            desc=True
        )
        .limit(5)
        .eq(
            "is_deleted",
            False
        )
        .execute()
    )

    return response.data


# =====================================
# MONTHLY REPORTS
# =====================================

def get_monthly_report(
    year,
    month
):

    sales_response = (
        supabase
        .table("sales")
        .select("*")
        .eq("is_deleted", False)    
        .execute()
    )

    monthly_sales = []

    for sale in sales_response.data:

        sale_date = (
            to_jakarta_datetime(
                sale["created_at"]
            )
        )

        if (
            sale_date.year == year
            and sale_date.month == month
        ):

            monthly_sales.append(
                sale
            )

    total_revenue = sum(
        sale["total_amount"]
        for sale in monthly_sales
    )

    total_transactions = len(
        monthly_sales
    )

    payment_breakdown = {
        "CASH": 0,
        "QRIS": 0,
        "TRANSFER": 0,
        "GOFOOD": 0
    }

    for sale in monthly_sales:

        payment_breakdown[
            sale["payment_method"]
        ] += sale["total_amount"]

    items_response = (
        supabase
        .table("sales_items")
        .select("""
            quantity,
            products (
                name
            ),
            sales (
                created_at,
                is_deleted
            )
        """)
        .execute()
    )

    product_totals = {}

    for item in items_response.data:

        if not item.get(
            "sales"
        ):
            continue
        
        if item["sales"].get(
            "is_deleted"
        ):
            
            continue

        sale_date = (
            to_jakarta_datetime(
                item["sales"]["created_at"]
            )
        )

        if (
            sale_date.year != year
            or sale_date.month != month
        ):
            continue

        product_name = item[
            "products"
        ]["name"]

        product_totals[
            product_name
        ] = (
            product_totals.get(
                product_name,
                0
            )
            + item["quantity"]
        )

    top_products = sorted(
        product_totals.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "revenue": total_revenue,
        "transactions": total_transactions,
        "payments": payment_breakdown,
        "top_products": top_products
    }

# =====================================
# EXPORT REPORT
# =====================================

def get_monthly_sales(
    year: int,
    month: int
):

    sales_response = (
        supabase
        .table("sales")
        .select("""
            *,
            sales_items(
                quantity,
                subtotal,
                products(
                    name
                )
            )
        """)
        .order(
            "created_at",
            desc=False
        )
        .eq(
            "is_deleted",
            False   
        )
        .execute()
    )

    users_response = (
        supabase
        .table("app_users")
        .select(
            "id, full_name, username"
        )
        .execute()
    )

    user_lookup = {
        user["id"]: user
        for user in users_response.data
    }

    monthly_sales = []

    for sale in sales_response.data:

        sale_date = to_jakarta_datetime(
            sale["created_at"]
        )

        if (
            sale_date.year != year
            or sale_date.month != month
        ):
            continue

        cashier = user_lookup.get(
            sale["staff_id"],
            {}
        )

        sale["cashier_name"] = cashier.get(
            "full_name",
            "-"
        )

        sale["cashier_username"] = cashier.get(
            "username",
            "-"
        )

        monthly_sales.append(
            sale
        )

    return monthly_sales

# =====================================
# REPORT HELPERS
# =====================================

def calculate_summary(
    sales: list
):

    return {
        "revenue": sum(
            sale["total_amount"]
            for sale in sales
        ),
        "transactions": len(sales)
    }


def calculate_payment_breakdown(
    sales: list
):

    payments = {}

    for sale in sales:

        method = sale["payment_method"]

        payments[method] = (
            payments.get(method, 0)
            + sale["total_amount"]
        )

    return payments


def calculate_top_products(
    sales: list
):

    totals = {}

    for sale in sales:

        for item in sale["sales_items"]:

            product = item["products"]["name"]

            totals[product] = (
                totals.get(product, 0)
                + item["quantity"]
            )

    return sorted(
        totals.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
# =====================================
# MONTHLY PRODUCTION
# =====================================

def get_monthly_production(
    year: int,
    month: int
):

    production_response = (
        supabase
        .table("production_logs")
        .select("""
            quantity_added,
            created_by,
            created_at,
            products(
                name
            )
        """)
        .order(
            "created_at",
            desc=False
        )
        .execute()
    )

    users_response = (
        supabase
        .table("app_users")
        .select(
            "id, full_name"
        )
        .execute()
    )

    user_lookup = {
        user["id"]: user["full_name"]
        for user in users_response.data
    }

    productions = []

    for item in production_response.data:

        production_date = to_jakarta_datetime(
            item["created_at"]
        )

        if (
            production_date.year != year
            or production_date.month != month
        ):
            continue

        item["staff_name"] = user_lookup.get(
            item["created_by"],
            "-"
        )

        productions.append(item)

    return productions

# =====================================
# MONTHLY STOCK MOVEMENTS
# =====================================

def get_monthly_inventory(
    year: int,
    month: int
):

    inventory_response = (
        supabase
        .table("inventory_logs")
        .select("""
            action,
            quantity,
            before_stock,
            after_stock,
            notes,
            user_id,
            created_at,
            products(
                name
            )
        """)
        .order(
            "created_at",
            desc=False
        )
        .execute()
    )

    users_response = (
        supabase
        .table("app_users")
        .select(
            "id, full_name"
        )
        .execute()
    )

    user_lookup = {
        user["id"]: user["full_name"]
        for user in users_response.data
    }

    movements = []

    for item in inventory_response.data:

        movement_date = to_jakarta_datetime(
            item["created_at"]
        )

        if (
            movement_date.year != year
            or movement_date.month != month
        ):
            continue

        item["staff_name"] = user_lookup.get(
            item["user_id"],
            "-"
        )

        movements.append(item)

    return movements