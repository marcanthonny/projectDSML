import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="DoorDash Delivery: Efficient Enough?", layout="wide")

# Apply custom styles (black background, white text)
st.markdown("""
    <style>
    body {
        background-color: black;
        color: white;
    }
    .name-nim-box {
        border: 2px solid #007BFF;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    h1 {
        color: #007BFF;
    }
    </style>
""", unsafe_allow_html=True)

# Add title
st.title("DoorDash Delivery: Efficient Enough?")
st.write(""" 
         Dasbor ini menganalisis indikator kinerja utama dari kumpulan data DoorDash, 
         dengan fokus pada volume pesanan, metode pembayaran, pendapatan, waktu pengiriman, diskon, 
         pengembalian dana, dan perilaku pelanggan. Analisis ini bertujuan untuk memberikan wawasan 
         tentang seberapa efisien sistem pengiriman DoorDash, serta tren perilaku pelanggan dan kinerja keuangan. 
""")

# Personal Information box with shadow and blue outline
st.markdown(f"""
    <div class='name-nim-box'>
        <h3>Group: 5th Group</h3>
        <h4>Class: LC41</h4>
        <p>Marc Anthony Samuel<br>Bayu Askha<br>Samuel Yuda Lampe</p>
    </div>
""", unsafe_allow_html=True)

# Load dataset
url = 'https://raw.githubusercontent.com/marcanthonny/projectDSML/refs/heads/main/food_orders_new_delhi%20(1).csv'
df = pd.read_csv(url)

# Data cleaning and exploration
st.header("Data Exploration and Cleaning")

# Show basic info
st.subheader("Dataset Overview")
st.write(df.head())

# Show dataset info
buffer = pd.DataFrame({'Column': df.columns, 'Data Type': df.dtypes, 'Null Values': df.isnull().sum()})
st.write(buffer)

# Fill missing values for 'Discounts and Offers' with 'No Offer'
df['Discounts and Offers'] = df['Discounts and Offers'].fillna('No Offer')

st.markdown("<hr/>", unsafe_allow_html=True)

# Sidebar to select which part of the dashboard to show
option = st.sidebar.selectbox(
    "Pilih Bagian Dashboard:",
    ["Order Volume", "Payment Method Distribution", "Total Revenue", "Delivery Duration", "Discounts and Offers", "Correlation Analysis", "Top 10 Customers"]
)

# Sidebar changes the selected section to display
if option == "Order Volume":
    st.subheader("Order Volume Over Time")
    
    # Order volume over time
    df['Order Date and Time'] = pd.to_datetime(df['Order Date and Time'])
    df['Order Date'] = df['Order Date and Time'].dt.date
    orders_per_day = df.groupby('Order Date')['Order ID'].count()

    # Columns for chart and insights
    col1, col2 = st.columns([2, 1])
    
    # Chart on the left
    with col1:
        fig1 = px.line(orders_per_day, x=orders_per_day.index, y=orders_per_day.values, 
                       labels={'x': 'Order Date', 'y': 'Number of Orders'},
                       title="Order Volume Over Time")
        fig1.update_traces(hovertemplate="Date: %{x}<br>Orders: %{y}")
        st.plotly_chart(fig1, use_container_width=True)

    # Key insights on the right
    with col2:
        st.write("### Key Insights")
        st.write("1. Certain dates show a high number of orders.")
        st.write("2. Monitor peak ordering times for planning resources.")
        
elif option == "Payment Method Distribution":
    st.subheader("Payment Method Distribution")
    
    payment_method_counts = df['Payment Method'].value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar chart for payment method distribution
        fig2 = px.bar(payment_method_counts, x=payment_method_counts.index, y=payment_method_counts.values,
                      labels={'x': 'Payment Method', 'y': 'Number of Orders'},
                      title="Distribution of Payment Methods")
        fig2.update_traces(hovertemplate="Payment Method: %{x}<br>Orders: %{y}")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.write("### Key Insights")
        st.write("1. Observe the dominant payment method.")
        st.write("2. Compare the proportion of digital payments.")

elif option == "Total Revenue":
    st.subheader("Total Revenue Over Time")
    
    # Ensure proper date parsing and extraction
    df['Order Date and Time'] = pd.to_datetime(df['Order Date and Time'], errors='coerce')
    df['Order Date'] = df['Order Date and Time'].dt.date

    # Ensure numerical conversion for revenue-related columns
    df['Order Value'] = pd.to_numeric(df['Order Value'], errors='coerce')
    df['Delivery Fee'] = pd.to_numeric(df['Delivery Fee'], errors='coerce')
    df['Commission Fee'] = pd.to_numeric(df['Commission Fee'], errors='coerce')
    df['Payment Processing Fee'] = pd.to_numeric(df['Payment Processing Fee'], errors='coerce')

    # Calculate total revenue
    df['Total Revenue'] = df['Order Value'] + df['Delivery Fee'] + df['Commission Fee'] + df['Payment Processing Fee']

    # Group by 'Order Date' and calculate total revenue per day
    daily_revenue = df.groupby('Order Date')['Total Revenue'].sum()

    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Line chart for revenue over time
        fig3 = px.line(daily_revenue, x=daily_revenue.index, y=daily_revenue.values, 
                       labels={'x': 'Order Date', 'y': 'Total Revenue'},
                       title="Revenue Over Time")
        fig3.update_traces(hovertemplate="Date: %{x}<br>Revenue: %{y}")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.write("### Key Insights")
        st.write("1. Peaks in revenue might align with peak order times.")
        st.write("2. Investigate dips in revenue for potential operational issues.")


elif option == "Delivery Duration":
    st.subheader("Delivery Duration Distribution")
    
    # Ensure proper date parsing for both 'Order Date and Time' and 'Delivery Date and Time'
    df['Order Date and Time'] = pd.to_datetime(df['Order Date and Time'], errors='coerce')
    df['Delivery Date and Time'] = pd.to_datetime(df['Delivery Date and Time'], errors='coerce')

    # Calculate delivery duration in minutes
    df['Delivery Duration'] = (df['Delivery Date and Time'] - df['Order Date and Time']).dt.total_seconds() / 60.0

    # Create layout with two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Histogram for delivery duration
        fig4 = px.histogram(df, x='Delivery Duration', nbins=20, 
                            title="Distribution of Delivery Duration (Minutes)")
        fig4.update_traces(hovertemplate="Duration: %{x} min<br>Orders: %{y}")
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        st.write("### Key Insights")
        st.write("1. Shorter delivery times might correlate with higher customer satisfaction.")
        st.write("2. Longer delivery durations could indicate operational bottlenecks.")


elif option == "Discounts and Offers":
    st.subheader("Discounts and Offers Usage")
    
    discount_counts = df['Discounts and Offers'].value_counts()

    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar chart for discounts and offers
        fig5 = px.bar(discount_counts, x=discount_counts.index, y=discount_counts.values,
                      labels={'x': 'Discounts and Offers', 'y': 'Number of Orders'},
                      title="Usage of Discounts and Offers")
        fig5.update_traces(hovertemplate="Discount: %{x}<br>Orders: %{y}")
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        st.write("### Key Insights")
        st.write("1. Certain offers may drive more orders.")
        st.write("2. Track offers with no impact on orders.")

elif option == "Correlation Analysis":
    st.subheader("Correlation Analysis (Revenue and Fees)")
    
    df['Order Value'] = pd.to_numeric(df['Order Value'], errors='coerce')
    df['Delivery Fee'] = pd.to_numeric(df['Delivery Fee'], errors='coerce')
    df['Commission Fee'] = pd.to_numeric(df['Commission Fee'], errors='coerce')
    df['Payment Processing Fee'] = pd.to_numeric(df['Payment Processing Fee'], errors='coerce')

    # Calculate correlation matrix
    corr_matrix = df[['Order Value', 'Delivery Fee', 'Commission Fee', 'Payment Processing Fee']].corr()

    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Heatmap for correlation analysis
        fig6 = px.imshow(corr_matrix, labels=dict(x="Variables", y="Variables", color="Correlation"),
                         title="Correlation Heatmap")
        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        st.write("### Key Insights")
        st.write("1. Strong correlations suggest shared factors affecting fees.")
        st.write("2. Use this data to adjust pricing strategies.")

elif option == "Top 10 Customers":
    st.subheader("Top 10 Customers by Total Order Value")

    top_customers = df.groupby('Customer ID')['Order Value'].sum().sort_values(ascending=False).head(10)

    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar chart for top 10 customers
        fig7 = px.bar(top_customers, x=top_customers.index, y=top_customers.values,
                      labels={'x': 'Customer ID', 'y': 'Total Order Value'},
                      title="Top 10 Customers by Order Value")
        fig7.update_traces(hovertemplate="Customer ID: %{x}<br>Order Value: %{y}")
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        st.write("### Key Insights")
        st.write("1. Identify key customers contributing the most to revenue.")
        st.write("2. Consider targeting these customers for loyalty programs.")
