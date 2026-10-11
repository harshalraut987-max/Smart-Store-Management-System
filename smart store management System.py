#smart store management System
from datetime import datetime
products={
    101:{"name":"laptop", "category":"electronics", "price":55000, "stock":20},
    102:{"name":"mobile", "category":"electronics", "price":25000, "stock":30},
    103:{"name":"keyboard", "category":"accessories", "price":1000, "stock":40},
    104:{"name":"mouse", "category":"accessories", "price":500, "stock":50},
    105:{"name":"headphone", "category":"accessories", "price":2000, "stock":30}
}
#1.View All products
def view_products():
    print("------------- ALL PRODUCTS --------------")
    print("ID\tProduct_name\tCategory\tPrice\tStock")   
    for pid, product in products.items():
        print(f"{pid}\t{product['name']:<15}\t"
              f"{product['category']:<12}\t"
              f"{product['price']:<8}\t"
              f"{product['stock']}")
view_products()

#2. search product
def search_products():
    keyword = input("\nEnter Product ID or Porduct Name:").lower()
    found = False
    
    for pid, product in products.items():
        if not found:
            print("Product Not Found.")
        if str(pid)== keyword or product["name"].lower() == keyword:
            print("\nPorduct Found")
            print("ID:",pid)
            print("Name:",product["name"])
            print("Category:",product["category"])
            print("Price:₹",product["price"])
            print("Stock:",product["stock"])
            found = True

search_products()                

from datetime import datetime

# Fallback dummy data to prevent NameErrors if not defined globally
if 'products' not in globals():
    products = {
        101: {"name": "Laptop", "price": 55000, "stock": 10},
        102: {"name": "Mouse", "price": 1200, "stock": 15},
        103: {"name": "Keyboard", "price": 2500, "stock": 5}
    }

if "sales_history" not in globals() or not isinstance("sales_history", list):
    sales_history = []

try:
    def purchase_products():
        pid = int(input("\nEnter Product ID: "))
        if pid not in products:
            print("Invalid Products ID.")
            return
            
        product = products[pid] 
        quantity = int(input("Enter quantity: "))
        
        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return
            
        if quantity > product['stock']:
            print("Insufficient stock.")
            return
                
        total = product["price"] * quantity
        product["stock"] -= quantity

        sale = {
            "product": product["name"],
            "quantity": quantity,
            "price": product["price"],
            "total": total,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        
        sales_history.append(sale)
        print("\n========== PURCHASE SUCCESSFUL ==========")
        print("Product :", product["name"])
        print("Quantity:", quantity)
        print("Price   : ₹", product["price"])
        print("Total   : ₹", total)
        print("Remaining Stock:", product["stock"])

    purchase_products()

except ValueError:
    print("Please enter a valid number.")

#4. view sales history
def view_sales_history():
    sales_history=[0]
    print("--------------View Sales History---------------")
    print("Product Name\tQuantity\tPrice\tTotal\tRemaining stock")
    if len(sales_history)==0:
        print("No sales history found")
        return
        
        for sale in sales_history:
            print("Product Name\tQuantity\tPrice\tTotal\tRemaining stock")
            print("Name:",sale["name"])
            print("Quantity:",sale["quantity"])
            print("Price:",sale["price"])
            print("Total:",sale["total"])
            print("Remaining stock:",sale["stock"])

view_sales_history()

#5. sales analysis
def sales_analysis():
    # FIXED: Replaced [0] with structured dictionary data so subscripting works
    sales_history = [
        {"product": "Laptop", "quantity": 1, "total": 55000},
        {"product": "Mouse", "quantity": 2, "total": 1200},
        {"product": "Laptop", "quantity": 1, "total": 55000},
        {"product": "Keyboard", "quantity": 1, "total": 2500}
    ]

    print("\n========== SALES ANALYSIS ==========")

    if len(sales_history) == 0:
        print("No sales data available.")
        return

    total_sales = 0
    total_quantity = 0

    product_sales = {}

    for sale in sales_history:
        total_sales += sale["total"]
        total_quantity += sale["quantity"]

        product = sale["product"]

        if product in product_sales:
            product_sales[product] += sale["quantity"]
        else:
            product_sales[product] = sale["quantity"]

    # Find best-selling product
    best_product = max(product_sales, key=product_sales.get)

    print("Total Products Sold :", total_quantity)
    print("Total Sales Amount  : ₹", total_sales)
    print("Number of Sales     :", len(sales_history))
    print("Best Selling Product:", best_product)
    print("Units Sold          :", product_sales[best_product])

sales_analysis()

# 6. Low Stock Products
def low_stock_products():

    print("\n========== LOW STOCK PRODUCTS ==========")

    found = False

    for pid, product in products.items():

        if product["stock"] <= 5:

            print("----------------------------------")
            print("Product ID :", pid)
            print("Name       :", product["name"])
            print("Stock      :", product["stock"])

            found = True

    if not found:
        print("No low stock products.")        


# Main Program
while True:

    print("\n==========================================")
    print("       SMART STORE MANAGEMENT SYSTEM")
    print("==========================================")
    print("1. View All Product")
    print("2. Search Product")
    print("3. Purchase Product")
    print("4. View Sales History")
    print("5. Sales Analysis")
    print("6. Low Stock Product")
    print("7. Exit")
    print("==========================================")

    choice=int(input("Enter a choice:"))
    if choice==1:
        print("Module-1 View all product")
    elif choice==2:
        print("Module-2 Search Product")
    elif choice==3:
        print("Module-3 Purchase")
    elif choice==4:
        print("Module-4 View Sales History")
    elif choice==5:
        print("module-5 Sales Analysis")
    elif choice==6:
        print("Module-6 Low Stock Product")
    elif choice<8:
        print("Module-7 Exit")
    else:
        print("Thank you for purchasing product")
        break