def update_product(
    product_id: str,
    name: str,
    category_id: str,
    price: int,
    minimum_stock: int
):
    return (
        supabase
        .table("products")
        .update({
            "name": name.strip(),
            "category_id": category_id,
            "price": price,
            "minimum_stock": minimum_stock
        })
        .eq("id", product_id)
        .execute()
    )