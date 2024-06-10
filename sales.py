import streamlit as st
import pandas as pd
import folium

# Load dataset
@st.cache
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

data = load_data('train.csv')

# Add a title to the page
st.title('Superstore Sales Dashboard with Region Map')

# Sidebar for filters
st.sidebar.header("Filters")
segment_filter = st.sidebar.multiselect(
    "Select Segment",
    options=data['Segment'].unique(),
    default=data['Segment'].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=data['Region'].unique(),
    default=data['Region'].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=data['Category'].unique(),
    default=data['Category'].unique()
)

# Filter data based on selections
filtered_data = data[
    (data['Segment'].isin(segment_filter)) &
    (data['Region'].isin(region_filter)) &
    (data['Category'].isin(category_filter))
]

# Display filtered data
st.write(f"Data Dimension: {filtered_data.shape[0]} rows and {filtered_data.shape[1]} columns.")
st.dataframe(filtered_data)

# Visualization: Sales over time
st.subheader("Sales Over Time")
sales_over_time = filtered_data.groupby('Order Date')['Sales'].sum().reset_index()
st.line_chart(sales_over_time.set_index('Order Date'))

# Visualization: Sales by Category
st.subheader("Sales by Category")
sales_by_category = filtered_data.groupby('Category')['Sales'].sum().reset_index()
st.bar_chart(sales_by_category.set_index('Category'))

# Visualization: Sales by Region
st.subheader("Sales by Region")
sales_by_region = filtered_data.groupby('Region')['Sales'].sum().reset_index()
st.bar_chart(sales_by_region.set_index('Region'))

# Visualization: Sales by Segment
st.subheader("Sales by Segment")
sales_by_segment = filtered_data.groupby('Segment')['Sales'].sum().reset_index()
st.bar_chart(sales_by_segment.set_index('Segment'))

# Add markers for each region
for index, row in filtered_data.iterrows():
    folium.Marker([row['Segment'], row['Sales']], popup=row['Region']).add_to(m)

# Display the map
folium_static(m)
