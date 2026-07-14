import streamlit as st

from utils.page_guard import require_login
from utils.formatter import format_currency

from database.category_service import (
    get_all_categories,
    create_category,
    delete_category
)

from database.product_service import (
    get_all_products,
    get_inactive_products,
    get_product_by_name,
    create_product,
    update_product,
    deactivate_product,
    restore_product
)


# ==========================================
# PAGE GUARD
# ==========================================

require_login()


# ==========================================
# PAGE TITLE
# ==========================================

st.title("📦 Product Management")


# ==========================================
# ADD CATEGORY
# ==========================================

with st.expander("➕ Add Category"):

    with st.form("add_category_form"):

        category_name = st.text_input(
            "Category Name"
        )

        submitted = st.form_submit_button(
            "Save Category",
            use_container_width=True
        )

    if submitted:

        if not category_name.strip():

            st.error(
                "Category name cannot be empty."
            )

        else:

            try:

                create_category(category_name)

                st.success(
                    "Category added successfully!"
                )

                st.rerun()

            except Exception as e:

                st.error(str(e))


# ==========================================
# LOAD CATEGORIES
# ==========================================

categories = get_all_categories()

category_map = {
    category["name"]: category["id"]
    for category in categories
}

# ==========================================
# CATEGORY MANAGEMENT
# ==========================================

st.divider()

st.subheader("📂 Category Management")

for category in categories:

    with st.container(border=True):

        col1, col2 = st.columns([4, 1])

        with col1:

            st.write(category["name"])

        with col2:

            if st.button(
                "🗑 Delete",
                key=f"delete_category_{category['id']}"
            ):

                try:

                    delete_category(
                        category["id"]
                    )

                    st.success(
                        "Category deleted."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(str(e))

# ==========================================
# ADD PRODUCT
# ==========================================

with st.expander("➕ Add Product"):

    if not categories:

        st.warning(
            "Please create a category first."
        )

    else:

        with st.form("add_product_form"):

            product_name = st.text_input(
                "Product Name"
            )

            selected_category = st.selectbox(
                "Category",
                list(category_map.keys())
            )

            price = st.number_input(
                "Price",
                min_value=0,
                step=1000,
                format="%d"
            )

            minimum_stock = st.number_input(
                "Minimum Stock",
                min_value=0,
                value=5,
                format="%d"
            )

            submitted = st.form_submit_button(
                "Save Product",
                use_container_width=True
            )

        if submitted:

            if not product_name.strip():

                st.error(
                    "Product name cannot be empty."
                )

            else:

                try:

                    existing_product = get_product_by_name(
                        product_name
                    )

                    if existing_product:

                        if existing_product["is_active"]:

                            st.error(
                                "Product already exists."
                            )

                        else:

                            restore_product(
                                existing_product["id"]
                            )

                            update_product(
                                product_id=existing_product["id"],
                                name=product_name,
                                category_id=category_map[
                                    selected_category
                                ],
                                price=int(price),
                                minimum_stock=int(
                                    minimum_stock
                                )
                            )

                            st.success(
                                "Inactive product restored!"
                            )

                            st.rerun()

                    else:

                        create_product(
                            name=product_name,
                            category_id=category_map[
                                selected_category
                            ],
                            price=int(price),
                            minimum_stock=int(
                                minimum_stock
                            ),
                            created_by=st.session_state.user_id
                        )

                        st.success(
                            "Product added successfully!"
                        )

                        st.rerun()

                except Exception as e:

                    st.error(str(e))


# ==========================================
# PRODUCT LIST
# ==========================================

st.divider()

st.subheader("Product List")

products = get_all_products()
inactive_products = get_inactive_products()

if not products:

    st.info(
        "No products found."
    )

else:

    for product in products:

        stock = product["current_stock"]
        minimum_stock = product["minimum_stock"]

        with st.container(border=True):

            st.subheader(
                product["name"]
            )

            st.write(
                f"Category: "
                f"{product['categories']['name']}"
            )

            st.write(
                f"Price: "
                f"{format_currency(product['price'])}"
            )

            st.write(
                f"Current Stock: {stock}"
            )

            st.write(
                f"Minimum Stock: "
                f"{minimum_stock}"
            )

            if stock <= minimum_stock:

                st.warning(
                    f"⚠️ Low Stock "
                    f"({stock} remaining)"
                )

            else:

                st.success(
                    "✅ Stock level is healthy"
                )

            # ==========================================
            # EDIT PRODUCT
            # ==========================================

            with st.expander(
                f"✏️ Edit {product['name']}"
            ):

                category_names = list(
                    category_map.keys()
                )

                current_category = (
                    product["categories"]["name"]
                )

                with st.form(
                    f"edit_form_{product['id']}"
                ):

                    edit_name = st.text_input(
                        "Product Name",
                        value=product["name"],
                        key=f"name_{product['id']}"
                    )

                    selected_category = st.selectbox(
                        "Category",
                        category_names,
                        index=category_names.index(
                            current_category
                        ),
                        key=f"category_{product['id']}"
                    )

                    edit_price = st.number_input(
                        "Price",
                        min_value=0,
                        value=int(product["price"]),
                        step=1000,
                        format="%d",
                        key=f"price_{product['id']}"
                    )

                    edit_minimum_stock = st.number_input(
                        "Minimum Stock",
                        min_value=0,
                        value=int(
                            product["minimum_stock"]
                        ),
                        format="%d",
                        key=f"minimum_{product['id']}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        save_clicked = (
                            st.form_submit_button(
                                "💾 Save Changes",
                                use_container_width=True
                            )
                        )

                    with col2:

                        deactivate_clicked = (
                            st.form_submit_button(
                                "🗑️ Deactivate",
                                use_container_width=True
                            )
                        )

                # ==========================
                # SAVE PRODUCT
                # ==========================

                if save_clicked:

                    try:

                        update_product(
                            product_id=product["id"],
                            name=edit_name,
                            category_id=category_map[
                                selected_category
                            ],
                            price=int(edit_price),
                            minimum_stock=int(
                                edit_minimum_stock
                            )
                        )

                        st.success(
                            "Product updated!"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(str(e))

                # ==========================
                # DEACTIVATE PRODUCT
                # ==========================

                if deactivate_clicked:

                    try:

                        deactivate_product(
                            product["id"]
                        )

                        st.success(
                            "Product deactivated!"
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(str(e))

# ==========================================
# INACTIVE PRODUCTS
# ==========================================

if inactive_products:

    st.divider()

    st.subheader("⚪ Inactive Products")

    for product in inactive_products:

        with st.container(border=True):

            st.subheader(product["name"])

            st.write(
                f"Category: {product['categories']['name']}"
            )

            st.write(
                f"Price: {format_currency(product['price'])}"
            )

            st.write(
                f"Current Stock: {product['current_stock']}"
            )

            st.write(
                f"Minimum Stock: {product['minimum_stock']}"
            )

            if st.button(
                "♻️ Restore Product",
                key=f"restore_{product['id']}",
                use_container_width=True
            ):

                try:

                    restore_product(
                        product["id"]
                    )

                    st.success(
                        f"{product['name']} restored!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(str(e))