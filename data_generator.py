import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_suppliers(n=50):
    supplier_names = [
        "Kalyan Jewellers", "Tanishq", "Malabar Gold", "Joyalukkas", "Senco Gold",
        "PC Jeweller", "TBZ", "Shankar Gems", "Kalaimagam", "Anandam Jewellers",
        "Alankar Jewellers", "Darshan Gems", "Balaji Diamonds", "Bansal Jewellers",
        "Beri Diamond", "Bhajan Jewels", "Survansh Jewellers", "Verma Jeweller",
        "Nishu Meerut", "Aditya Jewellers", "New Standard", "M.R. Manik",
        "Deepali Jewellers", "Shree Krishna", "Ganesh Gems"
    ]
    cities = ["Mumbai", "Delhi", "Kolkata", "Chennai", "Jaipur", "Surat", "Ahmedabad", "Lucknow", "Kanpur", "Meerut"]
    states = ["Maharashtra", "Delhi", "West Bengal", "Tamil Nadu", "Rajasthan", "Gujarat", "Uttar Pradesh"]
    metals = ["Gold", "Silver", "Platinum", "Diamond", "Mixed"]
    
    data = []
    for i in range(n):
        data.append({
            "supplier_id": f"SUP{i+1:04d}",
            "supplier_name": random.choice(supplier_names) if i < len(supplier_names) else f"Supplier_{i+1}",
            "contact_person": f"Contact Person {i+1}",
            "phone": f"+91{random.randint(6000000000, 9999999999)}",
            "email": f"supplier{i+1}@jewellery.com",
            "city": random.choice(cities),
            "state": random.choice(states),
            "metal_type": random.choice(metals),
            "rating": round(random.uniform(3.0, 5.0), 1),
            "years_in_business": random.randint(1, 30),
            "on_time_delivery_rate": round(random.uniform(85, 100), 1),
            "quality_score": round(random.uniform(3.5, 5.0), 1),
            "total_orders": random.randint(50, 500),
            "account_balance": round(random.uniform(100000, 5000000), 2),
            "status": random.choice(["Active", "Active", "Active", "Inactive"]),
            "created_date": (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime("%Y-%m-%d")
        })
    return pd.DataFrame(data)

def generate_inventory(n=500):
    product_categories = ["Rings", "Necklaces", "Bangles", "Earrings", "Chains", "Pendants", "Bracelets", "Mangalsutra"]
    metal_types = ["Gold 24K", "Gold 22K", "Gold 18K", "Silver", "Platinum"]
    designs = ["Traditional", "Contemporary", "Fusion", "Minimalist", "Ethnic"]
    base_price_per_gram = {"Gold 24K": 7500, "Gold 22K": 6875, "Gold 18K": 5625, "Silver": 85, "Platinum": 3500}
    
    data = []
    for i in range(n):
        weight = round(random.uniform(2, 100), 2)
        metal = random.choice(metal_types)
        price_per_gram = base_price_per_gram.get(metal, 5000)
        making_charge = random.uniform(5, 15)
        wastage = random.uniform(3, 10)
        stone_cost = round(random.uniform(0, 50000), 2) if random.random() > 0.3 else 0
        
        data.append({
            "product_id": f"PRD{i+1:05d}",
            "product_name": f"{random.choice(designs)} {random.choice(product_categories)}",
            "category": random.choice(product_categories),
            "metal_type": metal,
            "weight_grams": weight,
            "price_per_gram": price_per_gram,
            "making_charge_percent": round(making_charge, 1),
            "wastage_percent": round(wastage, 1),
            "stone_type": random.choice(["Diamond", "Ruby", "Emerald", "Sapphire", "None", "Pearl"]),
            "stone_weight_carat": round(random.uniform(0, 2), 2) if random.random() > 0.3 else 0,
            "stone_cost": stone_cost,
            "total_cost": round(weight * price_per_gram * (1 + wastage/100) + weight * price_per_gram * making_charge/100 + stone_cost, 2),
            "selling_price": round(random.uniform(1.1, 1.4)) * round(weight * price_per_gram * (1 + wastage/100) + weight * price_per_gram * making_charge/100 + stone_cost, 2),
            "stock_quantity": random.randint(0, 50),
            "min_stock_level": random.randint(5, 15),
            "warehouse_location": f"Shelf-{random.choice(['A', 'B', 'C', 'D'])}-{random.randint(1, 20)}",
            "supplier_id": f"SUP{random.randint(1, 50):04d}",
            "status": random.choice(["Available", "Available", "Available", "Out of Stock", "Discontinued"]),
            "created_date": (datetime.now() - timedelta(days=random.randint(30, 500))).strftime("%Y-%m-%d")
        })
    return pd.DataFrame(data)

def generate_buyers(n=200):
    buyer_types = ["Retail", "Wholesale", "Corporate", "Individual"]
    cities = ["Mumbai", "Delhi", "Kolkata", "Chennai", "Jaipur", "Surat", "Ahmedabad", "Lucknow", "Kanpur", "Meerut", "Varanasi", "Agra"]
    
    data = []
    for i in range(n):
        data.append({
            "buyer_id": f"BYR{i+1:05d}",
            "buyer_name": f"Buyer_{i+1}" if random.random() > 0.3 else f"Customer {i+1}",
            "buyer_type": random.choice(buyer_types),
            "contact_person": f"Contact {i+1}",
            "phone": f"+91{random.randint(6000000000, 9999999999)}",
            "email": f"buyer{i+1}@email.com",
            "address": f"{random.randint(1, 999)}, Street {random.randint(1, 100)}",
            "city": random.choice(cities),
            "state": random.choice(["Maharashtra", "Delhi", "West Bengal", "Tamil Nadu", "Rajasthan", "Gujarat", "Uttar Pradesh"]),
            "gstin": f"{random.randint(0, 9)}{random.choice(['A','B','C'])}{random.randint(1000, 9999)}{random.randint(0, 9)}{chr(65+random.randint(0,25))}{random.randint(0,9)}{random.randint(0,9)}{random.choice(['A','B','C'])}{random.randint(100, 999)}",
            "credit_limit": round(random.uniform(50000, 5000000), 2),
            "outstanding_amount": round(random.uniform(0, 500000), 2),
            "payment_terms": random.choice(["Immediate", "15 Days", "30 Days", "45 Days", "60 Days"]),
            "loyalty_points": random.randint(0, 10000),
            "total_purchases": random.randint(1, 100),
            "last_purchase_date": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d"),
            "status": random.choice(["Active", "Active", "Active", "Inactive"]),
            "created_date": (datetime.now() - timedelta(days=random.randint(30, 800))).strftime("%Y-%m-%d")
        })
    return pd.DataFrame(data)

def generate_sales(inventory_df, buyers_df, n=1000):
    categories = ["Rings", "Necklaces", "Bangles", "Earrings", "Chains", "Pendants", "Bracelets", "Mangalsutra"]
    payment_methods = ["Cash", "UPI", "Bank Transfer", "Credit Card", "Debit Card", "EMI"]
    cities = ["Mumbai", "Delhi", "Kolkata", "Chennai", "Jaipur", "Surat", "Ahmedabad", "Lucknow", "Kanpur", "Meerut"]
    
    data = []
    for i in range(n):
        base_date = datetime.now() - timedelta(days=random.randint(1, 365))
        season = get_season(base_date.month)
        price_multiplier = 1.2 if season in ["Wedding", "Festival"] else 1.0
        quantity = random.randint(1, 5)
        unit_price = random.uniform(5000, 500000) * price_multiplier
        discount = random.uniform(0, 10) if random.random() > 0.7 else 0
        gst_rate = 0.03 if random.random() > 0.5 else 0.05
        
        data.append({
            "transaction_id": f"TXN{i+1:06d}",
            "transaction_date": (base_date - timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S"),
            "invoice_number": f"INV{base_date.strftime('%Y%m')}{i+1:05d}",
            "buyer_id": f"BYR{random.randint(1, min(len(buyers_df), 200)):05d}",
            "product_category": random.choice(categories),
            "product_id": f"PRD{random.randint(1, min(len(inventory_df), 500)):05d}",
            "metal_type": random.choice(["Gold 24K", "Gold 22K", "Gold 18K", "Silver", "Platinum"]),
            "quantity": quantity,
            "unit_price": round(unit_price, 2),
            "total_amount": round(unit_price * quantity * (1 - discount/100), 2),
            "discount_percent": round(discount, 1),
            "gst_percent": gst_rate * 100,
            "gst_amount": round(unit_price * quantity * (1 - discount/100) * gst_rate, 2),
            "final_amount": round(unit_price * quantity * (1 - discount/100) * (1 + gst_rate), 2),
            "payment_method": random.choice(payment_methods),
            "payment_status": random.choice(["Paid", "Paid", "Paid", "Pending", "Partial"]),
            "city": random.choice(cities),
            "season": season,
            "sales_person": f"SalesPerson_{random.randint(1, 10)}",
            "branch": random.choice(["Main Branch", "Branch A", "Branch B", "Branch C"]),
            "created_date": base_date.strftime("%Y-%m-%d")
        })
    return pd.DataFrame(data)

def get_season(month):
    if month in [10, 11, 12, 1, 2, 3]:
        return "Wedding"
    elif month in [9, 3, 4]:
        return "Festival"
    elif month in [6, 7, 8]:
        return "Off-Season"
    else:
        return "Regular"

def generate_all_data():
    print("Generating suppliers...")
    suppliers = generate_suppliers(50)
    print("Generating inventory...")
    inventory = generate_inventory(500)
    print("Generating buyers...")
    buyers = generate_buyers(200)
    print("Generating sales transactions...")
    sales = generate_sales(inventory, buyers, 1000)
    return suppliers, inventory, buyers, sales

def save_data(suppliers, inventory, buyers, sales, folder="data"):
    import os
    os.makedirs(folder, exist_ok=True)
    suppliers.to_csv(f"{folder}/suppliers.csv", index=False)
    inventory.to_csv(f"{folder}/inventory.csv", index=False)
    buyers.to_csv(f"{folder}/buyers.csv", index=False)
    sales.to_csv(f"{folder}/sales.csv", index=False)
    print(f"Data saved to {folder}/ folder")
    print(f"- Suppliers: {len(suppliers)} records")
    print(f"- Inventory: {len(inventory)} records")
    print(f"- Buyers: {len(buyers)} records")
    print(f"- Sales: {len(sales)} records")

if __name__ == "__main__":
    suppliers, inventory, buyers, sales = generate_all_data()
    save_data(suppliers, inventory, buyers, sales, "data")
    print("\nSample data generated successfully!")