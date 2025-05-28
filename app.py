import pandas as pd
import numpy as np
import os
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, DateTime, Float
from dotenv import load_dotenv
import streamlit as st
import plotly.express as px


# Load environment variables from .env file
load_dotenv()

# Database connection
def get_db_connection():
    db_url = os.getenv("WAREHOUSE_URL")
    if not db_url:
        raise ValueError("WAREHOUSE_URL environment variable is not set.")
    engine = sqlalchemy.create_engine(db_url)
    return engine.connect()

# Load data
@st.cache_data
def load_data():
    cust_crm = pd.read_sql('SELECT * FROM cust_crm', con=get_db_connection())
    cust_erp = pd.read_sql('SELECT * FROM cust_erp', con=get_db_connection())
    prd_crm = pd.read_sql('SELECT * FROM prd_crm', con=get_db_connection())
    sales_crm = pd.read_sql('SELECT * FROM sales_crm', con=get_db_connection())
    loc_erp = pd.read_sql('SELECT * FROM loc_erp', con=get_db_connection())
    px_cat_erp = pd.read_sql('SELECT * FROM px_cat_erp', con=get_db_connection())
    sales_crm_prd = pd.read_sql('SELECT * FROM sales_crm_prd', con=get_db_connection())
    return cust_crm, cust_erp, prd_crm, sales_crm, loc_erp, px_cat_erp, sales_crm_prd

cust_crm, cust_erp, prd_crm, sales_crm, loc_erp, px_cat_erp, sales_crm_prd = load_data()

# Streamlit app
st.title("Business Data Dashboard")

# Sidebar navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a dataset to view:", 
                            ["Customer CRM", "Customer ERP", "Product CRM", "Sales CRM", "Location ERP", "Product Category ERP"])

# Display selected dataset
if options == "Customer CRM":
    st.header("Customer CRM Data")
    st.dataframe(cust_crm)
    st.subheader("Summary Statistics")
    st.write(cust_crm.describe())
elif options == "Customer ERP":
    st.header("Customer ERP Data")
    st.dataframe(cust_erp)
    st.subheader("Summary Statistics")
    st.write(cust_erp.describe())
elif options == "Product CRM":
    st.header("Product CRM Data")
    st.dataframe(prd_crm)
    st.subheader("Summary Statistics")
    st.write(prd_crm.describe())
elif options == "Sales CRM":
    st.header("Sales CRM Data")
    st.dataframe(sales_crm)
    st.subheader("Summary Statistics")
    st.write(sales_crm.describe())
elif options == "Location ERP":
    st.header("Location ERP Data")
    st.dataframe(loc_erp)
    st.subheader("Summary Statistics")
    st.write(loc_erp.describe())
elif options == "Product Category ERP":
    st.header("Product Category ERP Data")
    st.dataframe(px_cat_erp)
    st.subheader("Summary Statistics")
    st.write(px_cat_erp.describe())

# Visualization
st.sidebar.title("Visualization")
visualization = st.sidebar.radio("Select a visualization:", 
                                  ["Sales by Product", "Customer Distribution by Country", "Product Categories", "Number of Customers by Country"])

if visualization == "Sales by Product":
    st.header("Sales by Product")
    sales_summary = sales_crm_prd.groupby('prd_nm')['sls_sales'].sum().reset_index()
    print(sales_crm_prd.columns)
    fig = px.bar(sales_summary, x='prd_nm', y='sls_sales', title="Total Sales by Product")
    st.plotly_chart(fig)
elif visualization == "Customer Distribution by Country":
    st.header("Customer Distribution by Country")
    country_distribution = loc_erp['CNTRY'].value_counts().reset_index()
    country_distribution.columns = ['Country', 'Count']
    fig = px.pie(country_distribution, names='Country', values='Count', title="Customer Distribution by Country")
    st.plotly_chart(fig)
elif visualization == "Product Categories":
    st.header("Product Categories")
    category_distribution = px_cat_erp['CAT'].value_counts().reset_index()
    category_distribution.columns = ['Category', 'Count']
    fig = px.bar(category_distribution, x='Category', y='Count', title="Product Categories Distribution")
    st.plotly_chart(fig)
elif visualization == "Number of Customers by Country":
    st.header("Number of Customers by Country")
    customer_distribution = loc_erp['CNTRY'].value_counts().reset_index()
    customer_distribution.columns = ['Country', 'Count']
    fig = px.choropleth(customer_distribution, locations='Country', locationmode='country names',
                        color='Count', title="Number of Customers by Country",
                        color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig)
