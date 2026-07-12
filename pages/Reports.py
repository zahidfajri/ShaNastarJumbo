import streamlit as st
from datetime import datetime
from io import BytesIO

from utils.page_guard import require_login
from utils.formatter import format_currency

from database.report_service import (
    get_monthly_sales,
    get_monthly_production,
    get_monthly_inventory,
    calculate_summary,
    calculate_payment_breakdown,
    calculate_top_products
)

from utils.excel_export import (
    create_monthly_report_excel
)


require_login()

st.title("📈 Monthly Reports")

# =====================================
# MONTH SELECTION
# =====================================

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

current_date = datetime.now()

selected_month = st.selectbox(
    "Month",
    months,
    index=current_date.month - 1
)

selected_year = st.number_input(
    "Year",
    min_value=2025,
    max_value=2100,
    value=current_date.year
)

month_number = (
    months.index(selected_month)
    + 1
)

# =====================================
# LOAD REPORT DATA
# =====================================

sales = get_monthly_sales(
    selected_year,
    month_number
)

summary = calculate_summary(
    sales
)

payments = calculate_payment_breakdown(
    sales
)

top_products = calculate_top_products(
    sales
)

production_history = get_monthly_production(
    selected_year,
    month_number
)

stock_movements = get_monthly_inventory(
    selected_year,
    month_number
)

# =====================================
# SUMMARY
# =====================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Revenue",
        format_currency(
            summary["revenue"]
        )
    )

with col2:

    st.metric(
        "Transactions",
        summary["transactions"]
    )

# =====================================
# PAYMENT METHODS
# =====================================

st.divider()

st.subheader("💳 Payment Methods")

if not payments:

    st.info(
        "No payment data."
    )

else:

    for payment, amount in payments.items():

        st.write(
            f"{payment}: "
            f"{format_currency(amount)}"
        )

# =====================================
# TOP PRODUCTS
# =====================================

st.divider()

st.subheader("🥐 Top Products")

if not top_products:

    st.info(
        "No sales for this month."
    )

else:

    for i, (
        product,
        quantity
    ) in enumerate(
        top_products,
        start=1
    ):

        st.write(
            f"{i}. {product} "
            f"({quantity} pcs)"
        )

# =====================================
# EXPORT EXCEL
# =====================================

st.divider()

st.subheader("📥 Export Report")

workbook = create_monthly_report_excel(
    bakery_name="Sha Nastar Jumbo",
    period=f"{selected_month} {selected_year}",
    generated_by=st.session_state.full_name,
    sales=sales,
    summary=summary,
    payments=payments,
    top_products=top_products,
    production_history=production_history,
    stock_movements=stock_movements
)

buffer = BytesIO()

workbook.save(buffer)

buffer.seek(0)

filename = (
    f"ShaNastarJumbo_Report_"
    f"{selected_year}_"
    f"{month_number:02d}.xlsx"
)

st.download_button(
    label="📥 Download Excel Report",
    data=buffer,
    file_name=filename,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True,
    type="primary"
)