🥐 Sha Nastar Jumbo – Bakery Management System

A web-based bakery management system built with Python, Streamlit, and Supabase to help small businesses manage products, production, inventory, sales, and reporting in one place.

Version: v1.0.0
Status: Production Release

⸻

📌 Overview

Sha Nastar Jumbo is designed to simplify daily bakery operations by providing an easy-to-use interface for recording production, tracking inventory, processing sales, and generating operational reports.

The application was developed with a focus on simplicity, reliability, and real-world usability for small bakery businesses.

⸻

✨ Features

🔐 Authentication

* Secure login system
* Password hashing with bcrypt
* Protected application pages
* User session management

📦 Product Management

* Add product categories
* Add new products
* Edit product information
* Deactivate products
* Low stock monitoring

🥐 Production Management

* Record daily production
* Automatic stock updates
* Production history

📋 Inventory Management

* Automatic stock movement logging
* Before/After stock tracking
* Audit trail
* Current stock monitoring

🛒 Point of Sale (POS)

* Shopping cart
* Quantity adjustment (+ / -)
* Remove items
* Clear cart
* Automatic stock deduction

Supported Payment Methods

* Cash
* Transfer
* QRIS
* GoFood

📊 Dashboard

* Daily revenue
* Daily transaction count
* Best-selling products
* Low stock alerts
* Recent business activities

🧾 Transaction History

* View all transactions
* Filter by:
    * Today
    * This Week
    * This Month
    * All Time

📈 Reports

Monthly reporting including:

* Revenue
* Number of transactions
* Payment breakdown
* Top-selling products

📥 Excel Export

Export a professional Excel report containing:

* Summary
* Transactions
* Payment Breakdown
* Top Products
* Production History
* Stock Movements

⸻

🏗️ Tech Stack

Technology	Purpose
Python	Backend
Streamlit	Web Application
Supabase	Database & Backend Services
PostgreSQL	Database
OpenPyXL	Excel Report Generation
Pandas	Data Processing
bcrypt	Password Hashing
python-dotenv	Environment Variables

⸻

📁 Project Structure

ShaNastarJumbo/
│
├── app.py
├── database/
├── pages/
├── utils/
├── .streamlit/
├── requirements.txt
├── README.md
└── .env

⸻

🚀 Installation

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

2. Install dependencies

pip install -r requirements.txt

3. Configure environment variables

Create a .env file in the project root.

SUPABASE_URL=YOUR_SUPABASE_URL
SUPABASE_KEY=YOUR_SUPABASE_KEY

⸻

4. Run the application

streamlit run app.py

⸻

🗄️ Database

The application uses Supabase (PostgreSQL).

Main tables include:

* app_users
* categories
* products
* production_logs
* inventory_logs
* sales
* sales_items

⸻

🔄 Business Workflow

Login
   ↓
Manage Products
   ↓
Record Production
   ↓
Inventory Updated
   ↓
Process Sales
   ↓
Inventory Reduced
   ↓
Dashboard Updated
   ↓
Generate Monthly Report
   ↓
Export Excel

⸻

📸 Screenshots

Recommended screenshots to include:

* Login Page
* Dashboard
* Product Management
* Production
* Sales (POS)
* Transaction History
* Monthly Reports
* Excel Report

⸻

Known Limitations (v1.0)

* Product categories cannot be deleted.
* Deactivated products cannot yet be restored through the interface.

These enhancements are planned for a future release.

⸻

Future Improvements (v1.1)

* Restore inactive products
* Category management
* Dashboard charts
* PDF report export
* Search and filtering
* Supplier management
* Purchase order management
* Profit & loss analytics

⸻

License

This project was developed as a custom bakery management system for Sha Nastar Jumbo.

⸻

Acknowledgements

Developed using:

* Python
* Streamlit
* Supabase
* OpenPyXL

Special thanks to everyone who provided feedback throughout the development process.
