import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Jewellery Business Management System",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .warning-box {
        background-color: #78350f;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        padding: 10px 20px;
        border-radius: 5px 5px 0 0;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        from data_generator import generate_all_data, save_data
        suppliers, inventory, buyers, sales = generate_all_data()
        save_data(suppliers, inventory, buyers, sales, data_dir)
    
    try:
        suppliers = pd.read_csv(f"{data_dir}/suppliers.csv")
        inventory = pd.read_csv(f"{data_dir}/inventory.csv")
        buyers = pd.read_csv(f"{data_dir}/buyers.csv")
        sales = pd.read_csv(f"{data_dir}/sales.csv")
        if 'transaction_date' in sales.columns:
            sales['transaction_date'] = pd.to_datetime(sales['transaction_date'])
        if 'created_date' in sales.columns:
            sales['created_date'] = pd.to_datetime(sales['created_date'])
        return suppliers, inventory, buyers, sales
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

def format_currency(value):
    return f"₹{value:,.2f}"

def get_kpi_metrics(sales, inventory, suppliers, buyers):
    total_revenue = sales['final_amount'].sum() if 'final_amount' in sales.columns else 0
    total_orders = len(sales)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    if 'transaction_date' in sales.columns:
        current_month = sales[sales['transaction_date'] >= (datetime.now() - timedelta(days=30))]
        monthly_revenue = current_month['final_amount'].sum()
    else:
        monthly_revenue = total_revenue * 0.1
    low_stock_items = len(inventory[inventory['stock_quantity'] <= inventory['min_stock_level']]) if len(inventory) > 0 else 0
    active_suppliers = len(suppliers[suppliers['status'] == 'Active']) if len(suppliers) > 0 else 0
    active_buyers = len(buyers[buyers['status'] == 'Active']) if len(buyers) > 0 else 0
    return {
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'low_stock_items': low_stock_items,
        'active_suppliers': active_suppliers,
        'active_buyers': active_buyers
    }

def plot_revenue_trend(sales):
    if 'transaction_date' not in sales.columns or len(sales) == 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
        return fig
    sales['month'] = sales['transaction_date'].dt.to_period('M')
    monthly_sales = sales.groupby('month')['final_amount'].sum().reset_index()
    monthly_sales['month'] = monthly_sales['month'].astype(str)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_sales['month'], y=monthly_sales['final_amount'],
        mode='lines+markers', name='Revenue', line=dict(color='#FFD700', width=3),
        marker=dict(size=10, color='#FFD700')))
    fig.update_layout(title='Monthly Revenue Trend', xaxis_title='Month',
        yaxis_title='Revenue (₹)', template='plotly_dark', height=400)
    return fig

def plot_category_distribution(sales):
    if 'product_category' not in sales.columns or len(sales) == 0:
        return None
    category_sales = sales.groupby('product_category')['final_amount'].sum().reset_index()
    fig = px.pie(category_sales, values='final_amount', names='product_category',
        title='Sales by Product Category', hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(template='plotly_dark', height=400)
    return fig

def plot_inventory_status(inventory):
    if len(inventory) == 0:
        return None
    status_counts = inventory['status'].value_counts()
    fig = go.Figure(data=[go.Bar(x=status_counts.index, y=status_counts.values,
        marker_color=['#22c55e' if x == 'Available' else '#ef4444' if x == 'Out of Stock' else '#f59e0b' for x in status_counts.index])])
    fig.update_layout(title='Inventory Status Distribution', xaxis_title='Status',
        yaxis_title='Count', template='plotly_dark', height=400)
    return fig

def plot_supplier_performance(suppliers):
    if len(suppliers) == 0:
        return None
    fig = px.bar(suppliers.head(15), x='supplier_name', y='rating',
        color='on_time_delivery_rate', title='Top Suppliers by Rating',
        labels={'rating': 'Rating', 'supplier_name': 'Supplier'},
        color_continuous_scale='RdYlGn')
    fig.update_layout(template='plotly_dark', height=400, xaxis_tickangle=-45)
    return fig

def plot_payment_status(sales):
    if 'payment_status' not in sales.columns or len(sales) == 0:
        return None
    status_counts = sales['payment_status'].value_counts()
    fig = go.Figure(data=[go.Bar(x=status_counts.index, y=status_counts.values,
        marker_color=['#22c55e' if x == 'Paid' else '#f59e0b' if x == 'Pending' else '#ef4444' for x in status_counts.index])])
    fig.update_layout(title='Payment Status Distribution', xaxis_title='Status',
        yaxis_title='Count', template='plotly_dark', height=400)
    return fig

def plot_sales_by_season(sales):
    if 'season' not in sales.columns or len(sales) == 0:
        return None
    season_sales = sales.groupby('season')['final_amount'].sum().reset_index()
    fig = px.bar(season_sales, x='season', y='final_amount', title='Sales by Season',
        color='final_amount', color_continuous_scale='Blues')
    fig.update_layout(template='plotly_dark', height=400)
    return fig

def plot_metal_type_analysis(inventory):
    if 'metal_type' not in inventory.columns or len(inventory) == 0:
        return None
    metal_analysis = inventory.groupby('metal_type').agg({
        'product_id': 'count', 'total_cost': 'mean', 'selling_price': 'mean', 'stock_quantity': 'sum'
    }).reset_index()
    metal_analysis.columns = ['Metal Type', 'Products', 'Avg Cost', 'Avg Price', 'Total Stock']
    fig = make_subplots(rows=1, cols=2, subplot_titles=['Stock by Metal Type', 'Average Price by Metal Type'],
        specs=[[{"type": "bar"}, {"type": "bar"}]])
    fig.add_trace(go.Bar(x=metal_analysis['Metal Type'], y=metal_analysis['Total Stock'], name='Stock'), row=1, col=1)
    fig.add_trace(go.Bar(x=metal_analysis['Metal Type'], y=metal_analysis['Avg Price'], name='Avg Price'), row=1, col=2)
    fig.update_layout(template='plotly_dark', height=400, showlegend=False)
    return fig

def plot_buyer_analysis(buyers):
    if len(buyers) == 0:
        return None
    buyer_types = buyers['buyer_type'].value_counts().reset_index()
    buyer_types.columns = ['buyer_type', 'count']
    fig = px.pie(buyer_types, values='count', names='buyer_type',
        title='Buyer Type Distribution', hole=0.4)
    fig.update_layout(template='plotly_dark', height=400)
    return fig

def main():
    st.markdown('<h1 class="main-header"> Jewellery Business Data Management & Analytics System</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #94a3b8;">Vartika Sharma</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("Navigation")
        st.markdown("---")
        if st.button(" Dashboard", use_container_width=True):
            st.session_state['current_page'] = 'dashboard'
        if st.button(" Inventory", use_container_width=True):
            st.session_state['current_page'] = 'inventory'
        if st.button(" Suppliers", use_container_width=True):
            st.session_state['current_page'] = 'suppliers'
        if st.button(" Buyers", use_container_width=True):
            st.session_state['current_page'] = 'buyers'
        if st.button(" Sales", use_container_width=True):
            st.session_state['current_page'] = 'sales'
        if st.button(" Analytics", use_container_width=True):
            st.session_state['current_page'] = 'analytics'
        if st.button(" Data Upload", use_container_width=True):
            st.session_state['current_page'] = 'upload'
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.info("System Status: Online")
        if st.button(" Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    suppliers, inventory, buyers, sales = load_data()
    if suppliers is None:
        st.error("Failed to load data. Please check data files.")
        return
    
    metrics = get_kpi_metrics(sales, inventory, suppliers, buyers)
    current_page = st.session_state.get('current_page', 'dashboard')
    
    if current_page == 'dashboard' or current_page is None:
        st.header(" Dashboard Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Total Revenue", format_currency(metrics['total_revenue']))
        with col2: st.metric("Monthly Revenue", format_currency(metrics['monthly_revenue']))
        with col3: st.metric("Total Orders", f"{metrics['total_orders']:,}")
        with col4: st.metric("Avg Order Value", format_currency(metrics['avg_order_value']))
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Total Products", f"{len(inventory):,}")
        with col2: st.metric("Low Stock Items", metrics['low_stock_items'])
        with col3: st.metric("Active Suppliers", metrics['active_suppliers'])
        with col4: st.metric("Active Buyers", metrics['active_buyers'])
        st.markdown("---")
        tab1, tab2, tab3 = st.tabs(["Revenue & Sales", "Inventory Overview", "Supplier & Buyer Analysis"])
        with tab1:
            col1, col2 = st.columns(2)
            with col1: st.plotly_chart(plot_revenue_trend(sales), use_container_width=True)
            with col2: st.plotly_chart(plot_category_distribution(sales), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1: st.plotly_chart(plot_sales_by_season(sales), use_container_width=True)
            with col2: st.plotly_chart(plot_payment_status(sales), use_container_width=True)
        with tab2:
            col1, col2 = st.columns(2)
            with col1: st.plotly_chart(plot_inventory_status(inventory), use_container_width=True)
            with col2: st.plotly_chart(plot_metal_type_analysis(inventory), use_container_width=True)
            st.subheader("Low Stock Alerts")
            low_stock = inventory[inventory['stock_quantity'] <= inventory['min_stock_level']]
            if len(low_stock) > 0:
                st.markdown(f'<div class="warning-box"> {len(low_stock)} items are below minimum stock level!</div>', unsafe_allow_html=True)
                st.dataframe(low_stock[['product_id', 'product_name', 'category', 'stock_quantity', 'min_stock_level']], use_container_width=True)
            else:
                st.success("All items are above minimum stock level!")
        with tab3:
            col1, col2 = st.columns(2)
            with col1: st.plotly_chart(plot_supplier_performance(suppliers), use_container_width=True)
            with col2: st.plotly_chart(plot_buyer_analysis(buyers), use_container_width=True)
    
    elif current_page == 'inventory':
        st.header(" Inventory Management")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Total Products", f"{len(inventory):,}")
        with col2: st.metric("Available", f"{len(inventory[inventory['status'] == 'Available']):,}")
        with col3: st.metric("Out of Stock", f"{len(inventory[inventory['status'] == 'Out of Stock']):,}")
        st.subheader("Filter Inventory")
        col1, col2, col3 = st.columns(3)
        with col1: category_filter = st.multiselect("Category", inventory['category'].unique() if 'category' in inventory.columns else [])
        with col2: metal_filter = st.multiselect("Metal Type", inventory['metal_type'].unique() if 'metal_type' in inventory.columns else [])
        with col3: status_filter = st.multiselect("Status", inventory['status'].unique() if 'status' in inventory.columns else [])
        filtered_inv = inventory.copy()
        if category_filter: filtered_inv = filtered_inv[filtered_inv['category'].isin(category_filter)]
        if metal_filter: filtered_inv = filtered_inv[filtered_inv['metal_type'].isin(metal_filter)]
        if status_filter: filtered_inv = filtered_inv[filtered_inv['status'].isin(status_filter)]
        st.dataframe(filtered_inv, use_container_width=True)
        st.download_button(" Download Inventory Data", filtered_inv.to_csv(index=False), "inventory_data.csv", "text/csv")
    
    elif current_page == 'suppliers':
        st.header(" Supplier Management")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Total Suppliers", f"{len(suppliers):,}")
        with col2: st.metric("Active Suppliers", f"{len(suppliers[suppliers['status'] == 'Active']):,}")
        with col3: st.metric("Avg Rating", f"{suppliers['rating'].mean():.2f}")
        st.plotly_chart(plot_supplier_performance(suppliers), use_container_width=True)
        st.subheader("All Suppliers")
        st.dataframe(suppliers, use_container_width=True)
        st.download_button(" Download Suppliers Data", suppliers.to_csv(index=False), "suppliers_data.csv", "text/csv")
    
    elif current_page == 'buyers':
        st.header(" Buyer Management")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Total Buyers", f"{len(buyers):,}")
        with col2: st.metric("Active Buyers", f"{len(buyers[buyers['status'] == 'Active']):,}")
        with col3: st.metric("Total Credit Limit", format_currency(buyers['credit_limit'].sum()))
        st.plotly_chart(plot_buyer_analysis(buyers), use_container_width=True)
        st.subheader("All Buyers")
        st.dataframe(buyers, use_container_width=True)
        st.download_button(" Download Buyers Data", buyers.to_csv(index=False), "buyers_data.csv", "text/csv")
    
    elif current_page == 'sales':
        st.header(" Sales Analytics")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Total Revenue", format_currency(metrics['total_revenue']))
        with col2: st.metric("Total Transactions", f"{metrics['total_orders']:,}")
        with col3: st.metric("Avg Order Value", format_currency(metrics['avg_order_value']))
        with col4: st.metric("Paid Orders", f"{len(sales[sales['payment_status'] == 'Paid']) if 'payment_status' in sales.columns else 0:,}")
        tab1, tab2, tab3 = st.tabs(["Sales Overview", "By Category", "By Season"])
        with tab1:
            st.plotly_chart(plot_revenue_trend(sales), use_container_width=True)
            st.plotly_chart(plot_payment_status(sales), use_container_width=True)
        with tab2:
            st.plotly_chart(plot_category_distribution(sales), use_container_width=True)
            category_details = sales.groupby('product_category').agg({'final_amount': ['sum', 'mean', 'count']}).reset_index()
            category_details.columns = ['Category', 'Total Sales', 'Avg Order', 'Orders']
            st.dataframe(category_details, use_container_width=True)
        with tab3:
            st.plotly_chart(plot_sales_by_season(sales), use_container_width=True)
        st.subheader("Recent Transactions")
        st.dataframe(sales.tail(20), use_container_width=True)
        st.download_button(" Download Sales Data", sales.to_csv(index=False), "sales_data.csv", "text/csv")
    
    elif current_page == 'analytics':
        st.header(" Advanced Analytics")
        tab1, tab2, tab3, tab4 = st.tabs(["Trend Analysis", "Category Performance", "Supplier Analysis", "Inventory Turnover"])
        with tab1:
            if 'transaction_date' in sales.columns:
                sales['month_year'] = sales['transaction_date'].dt.to_period('M')
                trend_data = sales.groupby('month_year').agg({'final_amount': ['sum', 'mean', 'count']}).reset_index()
                trend_data.columns = ['Month', 'Total Revenue', 'Avg Order', 'Orders']
                trend_data['Month'] = trend_data['Month'].astype(str)
                fig = make_subplots(rows=2, cols=1, subplot_titles=['Monthly Revenue', 'Orders Count'],
                    specs=[[{"type": "scatter"}], [{"type": "bar"}]])
                fig.add_trace(go.Scatter(x=trend_data['Month'], y=trend_data['Total Revenue'],
                    mode='lines+markers', name='Revenue'), row=1, col=1)
                fig.add_trace(go.Bar(x=trend_data['Month'], y=trend_data['Orders'], name='Orders'), row=2, col=1)
                fig.update_layout(template='plotly_dark', height=600, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        with tab2:
            category_perf = sales.groupby('product_category').agg({'final_amount': ['sum', 'mean', 'count'], 'quantity': 'sum'}).reset_index()
            category_perf.columns = ['Category', 'Revenue', 'Avg Order', 'Orders', 'Units Sold']
            category_perf = category_perf.sort_values('Revenue', ascending=False)
            fig = px.bar(category_perf, x='Category', y='Revenue', color='Orders', title='Category Performance by Revenue')
            fig.update_layout(template='plotly_dark', height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(category_perf, use_container_width=True)
        with tab3:
            supplier_perf = suppliers.groupby('metal_type').agg({'rating': 'mean', 'on_time_delivery_rate': 'mean', 'total_orders': 'sum'}).reset_index()
            fig = make_subplots(rows=1, cols=2, subplot_titles=['Average Rating by Metal', 'Orders by Supplier Type'])
            fig.add_trace(go.Bar(x=supplier_perf['metal_type'], y=supplier_perf['rating'], name='Rating'), row=1, col=1)
            fig.add_trace(go.Bar(x=supplier_perf['metal_type'], y=supplier_perf['total_orders'], name='Orders'), row=1, col=2)
            fig.update_layout(template='plotly_dark', height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with tab4:
            inventory_analysis = inventory.groupby('category').agg({'stock_quantity': 'sum', 'total_cost': 'mean', 'selling_price': 'mean'}).reset_index()
            inventory_analysis['Turnover Ratio'] = (inventory_analysis['selling_price'] / inventory_analysis['total_cost']).round(2)
            fig = px.bar(inventory_analysis, x='category', y='Turnover Ratio', title='Inventory Turnover by Category',
                color='Turnover Ratio', color_continuous_scale='RdYlGn')
            fig.update_layout(template='plotly_dark', height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(inventory_analysis, use_container_width=True)
    
    elif current_page == 'upload':
        st.header(" Data Upload & Management")
        tab1, tab2 = st.tabs(["Upload Data", "Data Statistics"])
        with tab1:
            uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=['csv', 'xlsx'])
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                    st.success(f"File uploaded successfully! {len(df)} rows loaded.")
                    st.dataframe(df.head(10), use_container_width=True)
                    data_type = st.selectbox("Select data type", ["suppliers", "inventory", "buyers", "sales"])
                    if st.button("Save to Database"):
                        df.to_csv(f"data/{data_type}.csv", index=False)
                        st.success(f"Data saved to data/{data_type}.csv")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Suppliers")
                st.write(f"Total Records: {len(suppliers)}")
                st.write(f"Active: {len(suppliers[suppliers['status'] == 'Active'])}")
            with col2:
                st.write("### Inventory")
                st.write(f"Total Products: {len(inventory)}")
                st.write(f"Available: {len(inventory[inventory['status'] == 'Available'])}")
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Buyers")
                st.write(f"Total Buyers: {len(buyers)}")
            with col2:
                st.write("### Sales")
                st.write(f"Total Transactions: {len(sales)}")
                st.write(f"Total Revenue: {format_currency(sales['final_amount'].sum())}")

if __name__ == "__main__":
    main()
