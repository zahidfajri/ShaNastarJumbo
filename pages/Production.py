import streamlit as st

from utils.datetime_helper import (
    format_jakarta_datetime,
)

from utils.page_guard import require_login

from database.product_service import (
    get_all_products
)

from database.inventory_service import (
    add_production,
    get_today_production
)


require_login()

st.title("🥐 Daily Production")

products = get_all_products()

product_map = {}
product_options = []

for product in products:

    option_text = (
        f"{product['name']} "
        f"[{product['current_stock']}]"
    )

    product_map[option_text] = product
    product_options.append(option_text)


# ==========================================
# PRODUCTION INPUT
# ==========================================

if product_options:

    with st.form("production_form"):

        selected_product = st.selectbox(
            "Product",
            product_options
        )

        quantity = st.number_input(
            "Quantity Produced",
            min_value=1,
            step=1
        )

        submitted = st.form_submit_button(
            "Add Production",
            use_container_width=True
        )

    if submitted:

        product = product_map[
            selected_product
        ]

        add_production(
            product_id=product["id"],
            quantity=quantity,
            user_id=st.session_state.user_id
        )

        st.success(
            f"Added {quantity} pcs to "
            f"{product['name']}"
        )

        st.rerun()

else:

    st.info(
        "No products available."
    )


# ==========================================
# PRODUCTION HISTORY
# ==========================================

st.divider()

st.subheader("📋 Production History")

history = get_today_production()

if not history:

    st.info(
        "No production recorded yet."
    )

else:

    for item in history:

        formatted_date = format_jakarta_datetime(
            item["created_at"]
        )

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(
                    f"🥐 {item['products']['name']}"
                )

            with col2:

                st.write(
                    f"+{item['quantity_added']}"
                )

            st.caption(
                formatted_date
            )