import streamlit as st
from datetime import timedelta

from utils.datetime_helper import (
    format_jakarta_datetime,
    get_jakarta_today,
    to_jakarta_datetime
)

from utils.page_guard import require_login
from utils.formatter import format_currency

from database.sales_service import get_all_sales


require_login()

st.title("🧾 Transaction History")

# =====================================
# LOAD DATA
# =====================================

sales = get_all_sales()

# =====================================
# FILTERS
# =====================================

period = st.selectbox(
    "Period",
    [
        "Today",
        "This Week",
        "This Month",
        "All"
    ]
)

today = get_jakarta_today()

filtered_sales = []

for sale in sales:

    sale_date = to_jakarta_datetime(
        sale["created_at"]
    )

    include_sale = False

    if period == "Today":

        include_sale = (
            sale_date.date()
            == today
        )

    elif period == "This Week":

        start_of_week = (
            today
            - timedelta(days=today.weekday())
        )

        include_sale = (
            sale_date.date()
            >= start_of_week
        )

    elif period == "This Month":

        include_sale = (
            sale_date.month == today.month
            and sale_date.year == today.year
        )

    else:

        include_sale = True

    if include_sale:

        filtered_sales.append(sale)

# =====================================
# SUMMARY
# =====================================

total_revenue = sum(
    sale["total_amount"]
    for sale in filtered_sales
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Transactions",
        len(filtered_sales)
    )

with col2:

    st.metric(
        "Revenue",
        format_currency(total_revenue)
    )

st.divider()

# =====================================
# TRANSACTION LIST
# =====================================

if not filtered_sales:

    st.info(
        "No transactions found."
    )

else:

    for sale in filtered_sales:

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

            st.caption(
                formatted_date
            )

            st.write("Items:")

            for item in sale.get(
                "sales_items",
                []
            ):

                st.write(
                    f"• {item['products']['name']} "
                    f"x{item['quantity']}"
                )