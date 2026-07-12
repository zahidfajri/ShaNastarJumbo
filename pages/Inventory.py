import streamlit as st
from datetime import datetime

from utils.page_guard import require_login

from database.product_service import get_all_products

from database.inventory_service import (
    adjust_inventory,
    get_recent_inventory_logs
)


require_login()

st.title("📦 Inventory Adjustment")

products = get_all_products()

# Hide products with zero stock
products = [
    product
    for product in products
    if product["current_stock"] > 0
]

product_map = {}
product_options = []

for product in products:

    option_text = (
        f"{product['name']} "
        f"[{product['current_stock']}]"
    )

    product_map[option_text] = product
    product_options.append(option_text)


# ==================================
# ADJUSTMENT FORM
# ==================================

if product_options:

    with st.form("inventory_adjustment"):

        selected_product = st.selectbox(
            "Product",
            product_options
        )

        adjustment_type = st.radio(
            "Adjustment Type",
            ["ADD", "DEDUCT"],
            horizontal=True
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1
        )

        reason = st.text_input(
            "Reason",
            placeholder=(
                "Damaged goods, tester, "
                "correction, etc."
            )
        )

        submitted = st.form_submit_button(
            "Save Adjustment",
            use_container_width=True
        )

    if submitted:

        try:

            product = product_map[
                selected_product
            ]

            adjust_inventory(
                product_id=product["id"],
                adjustment_type=adjustment_type,
                quantity=quantity,
                reason=reason,
                user_id=st.session_state.user_id
            )

            st.success(
                "Inventory adjusted successfully!"
            )

            st.rerun()

        except Exception as e:

            st.error(str(e))

else:

    st.info(
        "No products with available stock."
    )


# ==================================
# RECENT ACTIVITIES
# ==================================

st.divider()

st.subheader(
    "📋 Recent Inventory Activities"
)

logs = get_recent_inventory_logs()

if not logs:

    st.info(
        "No inventory activities found."
    )

else:

    for log in logs:

        with st.container(border=True):

            quantity = log["quantity"]

            quantity_text = (
                f"+{quantity}"
                if quantity > 0
                else str(quantity)
            )

            created_at = datetime.fromisoformat(
                log["created_at"]
            )

            formatted_date = created_at.strftime(
                "%d %b %Y, %H:%M"
            )

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(
                    f"🥐 {log['products']['name']}"
                )

            with col2:

                st.write(quantity_text)

            st.caption(
                f"{log['before_stock']} → "
                f"{log['after_stock']}"
            )

            if log["notes"]:

                st.caption(
                    f"Reason: {log['notes']}"
                )

            st.caption(
                formatted_date
            )