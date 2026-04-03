# 💎 Jewellery Business Data Management and Analytics System

A comprehensive data management and analytics platform for jewellery wholesale businesses. Track inventory, analyze sales trends, monitor supplier performance, and make data-driven decisions.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.24+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

### 📊 Dashboard
- Real-time KPIs and business metrics
- Interactive visualizations
- Revenue trend analysis
- Category performance overview

### 📦 Inventory Management
- Product catalog with 500+ items
- Stock level monitoring
- Low-stock alerts
- Filter by category, metal type, status

### 👥 Supplier Management
- Supplier database with 50+ suppliers
- Performance ratings
- On-time delivery tracking
- Quality score monitoring

### 🛒 Buyer Management
- Customer database with 200+ buyers
- Buyer type segmentation
- Credit limit tracking
- Loyalty points management

### 💰 Sales Analytics
- Transaction history (1000+ records)
- Seasonal trend analysis
- Payment status tracking
- Revenue breakdown by category

### 📈 Advanced Analytics
- Monthly revenue trends
- Category performance comparison
- Inventory turnover analysis
- Supplier performance evaluation

### 📤 Data Management
- Import CSV/Excel files
- Data validation and cleaning
- Export reports as CSV
- Automatic data generation

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/username/jewellery-business-system.git
cd jewellery-business-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Open in Browser
Navigate to: `http://localhost:8501`

---

## 📁 Project Structure

```
jewellery-business-system/
├── app.py                 # Main Streamlit application
├── data_generator.py      # Sample data generator
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
│
└── data/                 # Data directory (auto-generated)
    ├── suppliers.csv     # Supplier data (50 records)
    ├── inventory.csv     # Inventory data (500 records)
    ├── buyers.csv        # Buyer data (200 records)
    └── sales.csv         # Sales data (1000 records)
```

---

## 🗃️ Data Schema

### Suppliers
| Column | Type | Description |
|--------|------|-------------|
| supplier_id | string | Unique ID (SUP0001) |
| supplier_name | string | Company name |
| rating | float | Rating (3.0-5.0) |
| on_time_delivery_rate | float | Delivery % |
| status | string | Active/Inactive |

### Inventory
| Column | Type | Description |
|--------|------|-------------|
| product_id | string | Unique ID (PRD00001) |
| product_name | string | Product name |
| category | string | Rings/Necklaces/etc |
| metal_type | string | Gold 24K/22K/Silver/etc |
| weight_grams | float | Weight |
| selling_price | float | Selling price |
| stock_quantity | int | Stock level |
| status | string | Availability |

### Buyers
| Column | Type | Description |
|--------|------|-------------|
| buyer_id | string | Unique ID (BYR00001) |
| buyer_name | string | Customer name |
| buyer_type | string | Retail/Wholesale/Corporate |
| credit_limit | float | Credit limit |
| loyalty_points | int | Points |

### Sales
| Column | Type | Description |
|--------|------|-------------|
| transaction_id | string | Unique ID |
| transaction_date | datetime | Date/Time |
| product_category | string | Category |
| quantity | int | Items sold |
| final_amount | float | Total |
| payment_status | string | Paid/Pending |
| season | string | Wedding/Festival/etc |

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository and deploy

### Docker
```bash
docker build -t jewellery-system .
docker run -p 8501:8501 jewellery-system
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

## 👤 Author

**Anshuman | Ambey Diamonds**
**Version:** 1.0.0 | **April 2026**

---

<div align="center">

**Made with ❤️ for the Jewellery Industry**

</div>