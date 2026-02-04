import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('car_prices.csv')
    df['saledate'] = pd.to_datetime(df['saledate'], errors='coerce')
    df['year'] = df['year'].astype(int, errors='ignore')
    df['sellingprice'] = pd.to_numeric(df['sellingprice'], errors='coerce')
    df['mmr'] = pd.to_numeric(df['mmr'], errors='coerce')
    df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce')
    df['condition'] = pd.to_numeric(df['condition'], errors='coerce')
    return df

df = load_data()

st.title('Car Prices Dashboard')

# Sidebar filters
st.sidebar.header('Filters')
makes = st.sidebar.multiselect('Select Makes', options=df['make'].unique(), default=df['make'].unique()[:5])
years = st.sidebar.slider('Select Year Range', int(df['year'].min()), int(df['year'].max()), (int(df['year'].min()), int(df['year'].max())))
bodies = st.sidebar.multiselect('Select Body Types', options=df['body'].unique(), default=df['body'].unique()[:3])

# Filter data
filtered_df = df[
    (df['make'].isin(makes)) &
    (df['year'] >= years[0]) &
    (df['year'] <= years[1]) &
    (df['body'].isin(bodies))
]

st.write(f"Showing {len(filtered_df)} cars")

# Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader('Selling Price Distribution')
    fig, ax = plt.subplots()
    ax.hist(filtered_df['sellingprice'].dropna(), bins=50, edgecolor='black')
    ax.set_xlabel('Selling Price')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

with col2:
    st.subheader('Average Selling Price by Make')
    avg_price = filtered_df.groupby('make')['sellingprice'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots()
    avg_price.plot(kind='bar', ax=ax)
    ax.set_ylabel('Average Selling Price')
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.subheader('Odometer vs Selling Price')
fig, ax = plt.subplots()
ax.scatter(filtered_df['odometer'], filtered_df['sellingprice'], alpha=0.5)
ax.set_xlabel('Odometer')
ax.set_ylabel('Selling Price')
st.pyplot(fig)

st.subheader('Data Overview')
st.dataframe(filtered_df.head(100))
