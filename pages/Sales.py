import streamlit as st
from utils.datetime_helper import (
    format_jakarta_datetime,
)

from utils.page_guard import require_login
from utils.formatter import format_currency

from database.product_service import get_all_products
from database.sales_service import (
    process_sale,
    get_recent_sales,
    delete_sale
)

require_login()

if "confirm_delete_sale" not in st.session_state:
    st.session_state.confirm_delete_sale = None

st.title("🛒 Sales")

# =====================================
# CART
# =====================================

if "cart" not in st.session_state:
    st.session_state.cart = []

products = get_all_products()

products = [p for p in products if p["current_stock"] > 0]

product_map = {}
product_options = []

for product in products:
    option_text = f"{product['name']} [{product['current_stock']}]"
    product_map[option_text] = product
    product_options.append(option_text)

if product_options:

    with st.form("add_item_form"):

        selected_product = st.selectbox("Product", product_options)

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1
        )

        submitted = st.form_submit_button("Add Item")

    if submitted:

        product = product_map[selected_product]

        existing_item = None

        for item in st.session_state.cart:
            if item["product_id"] == product["id"]:
                existing_item = item
                break

        if existing_item:

            new_quantity = existing_item["quantity"] + quantity

            if new_quantity > product["current_stock"]:
                st.error("Total quantity exceeds current stock!")
            else:
                existing_item["quantity"] = new_quantity
                st.success("Cart updated!")
                st.rerun()

        else:

            if quantity > product["current_stock"]:
                st.error("Not enough stock!")
            else:
                st.session_state.cart.append({
                    "product_id": product["id"],
                    "name": product["name"],
                    "quantity": quantity,
                    "price": product["price"]
                })
                st.success("Item added!")
                st.rerun()

else:
    st.warning("No products with available stock.")

st.divider()
st.subheader("🛒 Current Cart")

total_amount = 0

if not st.session_state.cart:
    st.info("Cart is empty.")
else:

    latest_products = {p["id"]: p for p in get_all_products()}

    for i, item in enumerate(st.session_state.cart):

        subtotal = item["quantity"] * item["price"]
        total_amount += subtotal
        current_stock = latest_products[item["product_id"]]["current_stock"]

        with st.container(border=True):

            st.write(f"🥐 {item['name']}")

            col1, col2, col3 = st.columns([1,2,1])

            with col1:
                if st.button("➖", key=f"minus_{i}"):
                    item["quantity"] -= 1
                    if item["quantity"] <= 0:
                        st.session_state.cart.pop(i)
                    st.rerun()

            with col2:
                st.markdown(
                    f"<div style='text-align:center'><b>{item['quantity']}</b><br>{format_currency(item['price'])}/pcs</div>",
                    unsafe_allow_html=True
                )

            with col3:
                if st.button("➕", key=f"plus_{i}"):
                    if item["quantity"] < current_stock:
                        item["quantity"] += 1
                        st.rerun()
                    else:
                        st.error("Stock limit reached.")

            st.write(f"Subtotal: {format_currency(subtotal)}")

            if st.button("🗑️ Remove", key=f"remove_{i}", use_container_width=True):
                st.session_state.cart.pop(i)
                st.rerun()

    st.divider()

    if st.button("🗑️ Clear Cart", use_container_width=True):
        st.session_state.cart = []
        st.rerun()

    payment_method = st.radio(
        "Payment Method",
        ["CASH","TRANSFER","QRIS","GOFOOD"],
        horizontal=True
    )

    st.subheader("✅ Transaction Summary")

    for item in st.session_state.cart:
        st.write(f"• {item['name']} x{item['quantity']}")

    st.write(f"**Payment:** {payment_method}")
    st.subheader(f"TOTAL: {format_currency(total_amount)}")

    if st.button("Confirm Transaction", type="primary", use_container_width=True):
        try:
            process_sale(
                cart_items=st.session_state.cart,
                payment_method=payment_method,
                staff_id=st.session_state.user_id
            )
            st.success("Transaction saved successfully!")
            st.session_state.cart = []
            st.rerun()
        except Exception as e:
            st.error(str(e))

st.divider()
st.subheader("🧾 Recent Transactions")

recent_sales = get_recent_sales()

if not recent_sales:
    st.info("No transactions yet.")
else:

    for sale in recent_sales:

        with st.container(border=True):

            formatted_date = format_jakarta_datetime(sale["created_at"])

            st.write(f"💳 {sale['payment_method']}")
            st.write(f"Total: {format_currency(sale['total_amount'])}")
            st.write("Items:")

            for item in sale.get("sales_items", []):
                st.write(f"• {item['products']['name']} x{item['quantity']}")

            st.caption(formatted_date)

            st.divider()

            sale_id = sale["id"]

            if st.session_state.confirm_delete_sale != sale_id:

                if st.button(
                    "🗑 Delete Transaction",
                    key=f"delete_{sale_id}",
                    use_container_width=True
                ):
                    st.session_state.confirm_delete_sale = sale_id
                    st.rerun()

            else:

                st.warning(
                    "Delete this transaction? Stock will be restored."
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "✅ Confirm",
                        key=f"confirm_{sale_id}",
                        use_container_width=True
                    ):
                        try:
                            delete_sale(
                                sale_id=sale_id,
                                deleted_by=st.session_state.user_id
                            )
                            st.session_state.confirm_delete_sale = None
                            st.success("Transaction deleted.")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))

                with col2:
                    if st.button(
                        "Cancel",
                        key=f"cancel_{sale_id}",
                        use_container_width=True
                    ):
                        st.session_state.confirm_delete_sale = None
                        st.rerun()
