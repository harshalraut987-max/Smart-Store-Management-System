import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Store Management system",
    page_icon="🛒",
    layout="wide"
)

# Initialize store data

# Initialize store data
if "products" not in st.session_state:
    st.session_state.products = pd.DataFrame([
        {"ID": 101, "Product": "Laptop",
         "Category": "Electronics", "Price": 55000, "Stock": 20},

        {"ID": 102, "Product": "Mobile",
         "Category": "Electronics", "Price": 25000, "Stock": 30},

        {"ID": 103, "Product": "Keyboard",
         "Category": "Accessories", "Price": 1000, "Stock": 40},

        {"ID": 104, "Product": "Mouse",
         "Category": "Accessories", "Price": 500, "Stock": 50},

        {"ID": 105, "Product": "Headphone",
         "Category": "Accessories", "Price": 2000, "Stock": 30}
    ])

if "sales" not in st.session_state:
    st.session_state.sales = []

products = st.session_state.products


# Sidebar navigation
st.sidebar.title("🛒 Smart Store")
st.sidebar.write("Store Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Product Management",
        "Purchase Product",
        "Sales History",
        "Sales Analysis",
        "Low Stock"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Smart Store System | Python + Streamlit")

# Dashboard
if page == "Dashboard":
    st.title("📊 Store Dashboard")
    st.write("Welcome to your Smart Store Management System!")

    total_products = len(products)
    total_stock = int(products["Stock"].sum())
    stock_value = (products["Price"] * products["Stock"]).sum()
    total_sales = sum(s["Total"] for s in st.session_state.sales)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Product Types", total_products)
    c2.metric("Units in Stock", total_stock)
    c3.metric("Inventory Value", f"₹{stock_value:,.2f}")
    c4.metric("Total Sales", f"₹{total_sales:,.2f}")

    st.subheader("📦 Available Products")
    st.dataframe(products, use_container_width=True, hide_index=True)

    st.subheader("💰 Recent Sales")
    if st.session_state.sales:
        st.dataframe(
            pd.DataFrame(st.session_state.sales).tail(5),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No sales recorded yet.")

# Product Management
elif page == "Product Management":
    st.title("📦 Product Management")

    search = st.text_input("🔍 Search product by name")

    if search:
        filtered = products[
            products["Product"].str.contains(
                search, case=False, na=False
            )
        ]
    else:
        filtered = products

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.subheader("➕ Add New Product")

    with st.form("add_product"):
        product_id = st.number_input(
            "Product ID", min_value=1, step=1, value=106
        )
        name = st.text_input("Product Name")
        category = st.selectbox(
            "Category",
            ["Grocery", "Dairy", "Bakery", "Personal Care", "Other"]
        )
        price = st.number_input("Price (₹)", min_value=0.01, value=50.0)
        stock = st.number_input("Initial Stock", min_value=0, step=1)
        add = st.form_submit_button("Add Product")

        if add:
            if not name.strip():
                st.error("Please enter a product name.")
            elif int(product_id) in products["ID"].tolist():
                st.error("This Product ID already exists.")
            else:
                new_product = pd.DataFrame([{
                    "ID": int(product_id),
                    "Product": name.strip(),
                    "Category": category,
                    "Price": float(price),
                    "Stock": int(stock)
                }])
                st.session_state.products = pd.concat(
                    [products, new_product], ignore_index=True
                )
                st.success(f"{name} added successfully!")
                st.rerun()

# Purchase Product
elif page == "Purchase Product":
    st.title("🛍️ Customer Purchase")

    if products.empty:
        st.warning("Please add products first.")
    else:
        with st.form("purchase_form"):
            customer = st.text_input("Customer Name")
            available_products = products["Product"].tolist()
            selected = st.selectbox(
                "Select Product", available_products
            )
            quantity = st.number_input(
                "Quantity", min_value=1, step=1, value=1
            )
            purchase = st.form_submit_button("Complete Purchase")

            if purchase:
                if not customer.strip():
                    st.error("Please enter customer name.")
                else:
                    idx = st.session_state.products.index[
                        st.session_state.products["Product"] == selected
                    ][0]
                    current_stock = int(
                        st.session_state.products.loc[idx, "Stock"]
                    )

                    if quantity > current_stock:
                        st.error(
                            f"Insufficient stock! Available: {current_stock}"
                        )
                    else:
                        unit_price = float(
                            st.session_state.products.loc[idx, "Price"]
                        )
                        total = unit_price * quantity

                        st.session_state.products.loc[idx, "Stock"] = (
                            current_stock - quantity
                        )

                        st.session_state.sales.append({
                            "Customer": customer.strip(),
                            "Product": selected,
                            "Quantity": int(quantity),
                            "Unit Price": unit_price,
                            "Total": total,
                            "Date": pd.Timestamp.now().strftime(
                                "%Y-%m-%d %H:%M"
                            )
                        })

                        st.success("Purchase completed successfully!")
                        st.metric("Bill Amount", f"₹{total:,.2f}")

# Sales History
elif page == "Sales History":
    st.title("🧾 Sales History")

    if st.session_state.sales:
        sales_df = pd.DataFrame(st.session_state.sales)
        st.dataframe(sales_df, use_container_width=True, hide_index=True)
        st.metric(
            "Total Revenue",
            f"₹{sales_df['Total'].sum():,.2f}"
        )

        csv = sales_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Sales CSV",
            data=csv,
            file_name="sales_history.csv",
            mime="text/csv"
        )
    else:
        st.info("No sales available. Make a purchase first.")

# Sales Analysis
elif page == "Sales Analysis":
    st.title("📈 Sales Analysis")

    if st.session_state.sales:
        sales_df = pd.DataFrame(st.session_state.sales)

        total_revenue = sales_df["Total"].sum()
        units_sold = sales_df["Quantity"].sum()
        transactions = len(sales_df)

        c1, c2, c3 = st.columns(3)
        c1.metric("Revenue", f"₹{total_revenue:,.2f}")
        c2.metric("Units Sold", int(units_sold))
        c3.metric("Transactions", transactions)

        st.subheader("Revenue by Product")
        revenue = sales_df.groupby("Product")["Total"].sum()
        st.bar_chart(revenue)

        st.subheader("Quantity Sold by Product")
        quantities = sales_df.groupby("Product")["Quantity"].sum()
        st.bar_chart(quantities)
    else:
        st.info("Sales analysis will appear after the first purchase.")

# Low Stock
elif page == "Low Stock":
    st.title("⚠️ Low Stock Alert")

    threshold = st.slider(
        "Show products with stock at or below",
        min_value=1,
        max_value=20,
        value=5
    )

    low_stock = products[products["Stock"] <= threshold]

    if low_stock.empty:
        st.success("All products have sufficient stock.")
    else:
        st.warning(f"{len(low_stock)} product(s) need stock replenishment.")
        st.dataframe(
            low_stock, use_container_width=True, hide_index=True
        )
