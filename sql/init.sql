-- =====================================================
-- EXTENSIONS
-- =====================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =====================================================
-- APP USERS
-- =====================================================

CREATE TABLE IF NOT EXISTS app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(100) NOT NULL,

    role VARCHAR(20) NOT NULL
        CHECK (role IN ('OWNER', 'STAFF')),

    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- CATEGORIES
-- =====================================================

CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(100) UNIQUE NOT NULL,

    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- PRODUCTS
-- =====================================================

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(150) UNIQUE NOT NULL,

    category_id UUID NOT NULL
        REFERENCES categories(id),

    price INTEGER NOT NULL
        CHECK (price >= 0),

    current_stock INTEGER NOT NULL DEFAULT 0
        CHECK (current_stock >= 0),

    minimum_stock INTEGER NOT NULL DEFAULT 5
        CHECK (minimum_stock >= 0),

    is_active BOOLEAN DEFAULT TRUE,

    created_by UUID
        REFERENCES app_users(id),

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- PRODUCTION LOGS
-- =====================================================

CREATE TABLE IF NOT EXISTS production_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    product_id UUID NOT NULL
        REFERENCES products(id),

    quantity_added INTEGER NOT NULL
        CHECK (quantity_added > 0),

    created_by UUID
        REFERENCES app_users(id),

    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- SALES
-- =====================================================

CREATE TABLE IF NOT EXISTS sales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    staff_id UUID
        REFERENCES app_users(id),

    payment_method VARCHAR(20) NOT NULL
        CHECK (
            payment_method IN (
                'CASH',
                'QRIS',
                'GOFOOD'
            )
        ),

    total_amount INTEGER NOT NULL
        CHECK (total_amount >= 0),

    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- SALES ITEMS
-- =====================================================

CREATE TABLE IF NOT EXISTS sales_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    sale_id UUID NOT NULL
        REFERENCES sales(id)
        ON DELETE CASCADE,

    product_id UUID NOT NULL
        REFERENCES products(id),

    quantity INTEGER NOT NULL
        CHECK (quantity > 0),

    price INTEGER NOT NULL
        CHECK (price >= 0),

    subtotal INTEGER NOT NULL
        CHECK (subtotal >= 0)
);

-- =====================================================
-- INVENTORY LOGS
-- =====================================================

CREATE TABLE IF NOT EXISTS inventory_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    product_id UUID NOT NULL
        REFERENCES products(id),

    action VARCHAR(30) NOT NULL
        CHECK (
            action IN (
                'PRODUCTION',
                'SALE',
                'ADJUSTMENT'
            )
        ),

    quantity INTEGER NOT NULL,

    before_stock INTEGER NOT NULL,

    after_stock INTEGER NOT NULL,

    notes TEXT,

    user_id UUID
        REFERENCES app_users(id),

    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_products_active
ON products(is_active);

CREATE INDEX IF NOT EXISTS idx_sales_created_at
ON sales(created_at);

CREATE INDEX IF NOT EXISTS idx_sales_payment
ON sales(payment_method);

CREATE INDEX IF NOT EXISTS idx_inventory_product
ON inventory_logs(product_id);

CREATE INDEX IF NOT EXISTS idx_production_product
ON production_logs(product_id);