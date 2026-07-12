import streamlit as st

from utils.page_guard import require_login
from utils.formatter import format_currency
from utils.datetime_helper import format_jakarta_datetime

from database.report_service import (
    get_today_sales_summary,
    get_low_stock_products,
    get_best_seller_today,
    get_recent_dashboard_sales
)

require_login()

st.title("📊 Dashboard")

# =====================================
# LOAD DATA
# =====================================

summary = get_today_sales_summary()
best_seller = get_best_seller_today()
low_stock = get_low_stock_products()
recent_sales = get_recent_dashboard_sales()

# =====================================
# METRICS
# =====================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Today's Revenue",
        format_currency(summary["revenue"])
    )

with col2:

    st.metric(
        "Transactions",
        summary["transactions"]
    )

with col3:

    if best_seller:

        st.metric(
            "Best Seller",
            best_seller["name"]
        )

        st.caption(
            f"{best_seller['quantity']} pcs sold"
        )

    else:

        st.metric(
            "Best Seller",
            "-"
        )

# =====================================
# RECENT ACTIVITIES
# =====================================

st.divider()

st.subheader("🧾 Recent Activities")

if not recent_sales:

    st.info(
        "No recent transactions."
    )

else:

    for sale in recent_sales:

        with st.container(border=True):

            formatted_date = format_jakarta_datetime(
                sale["created_at"]
            )

            col1, col2 = st.columns([3, 1])

            with col1:

                st.write(
                    f"💳 {sale['payment_method']}"
                )

            with col2:

                st.write(
                    format_currency(
                        sale["total_amount"]
                    )
                )

            items_text = []

            for item in sale.get("sales_items", []):

                items_text.append(
                    f"{item['products']['name']} "
                    f"x{item['quantity']}"
                )

            if items_text:

                st.caption(
                    " • ".join(items_text)
                )

            st.caption(
                formatted_date
            )

# =====================================
# LOW STOCK
# =====================================

st.divider()

st.subheader("⚠️ Low Stock Products")

if not low_stock:

    st.success(
        "All products have sufficient stock."
    )

else:

    for product in low_stock:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(
                    f"🥐 {product['name']}"
                )

            with col2:

                st.write(
                    f"[{product['current_stock']}]"
                )

            st.caption(
                f"Minimum: {product['minimum_stock']}"
            )