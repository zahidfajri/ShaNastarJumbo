import streamlit as st

from utils.page_guard import require_login
from utils.formatter import format_currency
from utils.datetime_helper import format_jakarta_datetime

from database.report_service import (
    get_today_sales_summary,
    get_dashboard_stock,
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
dashboard_stock = get_dashboard_stock()
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
# PRODUCT STOCK
# =====================================

st.divider()

st.subheader("📦 Product Stock")

stock_data = []

for product in dashboard_stock:

    stock_data.append({
        "Status": (
            "⚠️"
            if product["current_stock"] <= product["minimum_stock"]
            else "✅"
        ),
        "Product": product["name"],
        "Current Stock": product["current_stock"],
        "Minimum Stock": product["minimum_stock"]
    })

st.dataframe(
    stock_data,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Status": st.column_config.TextColumn(
            width="small"
        ),
        "Product": st.column_config.TextColumn(
            width="large"
        ),
        "Current Stock": st.column_config.NumberColumn(
            width="small"
        ),
        "Minimum Stock": st.column_config.NumberColumn(
            width="small"
        ),
    },
)