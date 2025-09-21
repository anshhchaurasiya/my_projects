import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt  # ✅ Correct import

# Streamlit config
st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

# Title
st.title("Analytics")

# Load pickled feature text
feature_text = pickle.load(open("feature_text.pkl", "rb"))

# Load data
new_df = pd.read_csv("data_viz1.csv")

# Grouping the data
group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean().reset_index()

# Creating scatter mapbox plot
fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    size="built_up_area",
    color="price_per_sqft",
    mapbox_style="open-street-map",
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    width=1200,
    height=700,
)

# Show the scatter map
st.plotly_chart(fig, use_container_width=True)

# WordCloud visualization
st.subheader("Feature Word Cloud")

plt.rcParams["font.family"] = "Arial"
st.subheader("Features Word")
wordcloud = WordCloud(
    width=800,
    height=800,
    background_color='white',
    stopwords=set(['s']),  # Add more stopwords if needed
    min_font_size=10
).generate(feature_text)

# Show the wordcloud using Streamlit
fig_wc, ax = plt.subplots(figsize=(8, 8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig_wc)

st.subheader("Average Price per Sector")
st.subheader("🟢 Sector-wise Average Price Bubble Chart")

fig_bubble = px.scatter(
    group_df,
    x='sector',
    y='price',
    size='built_up_area',
    color='price_per_sqft',
    hover_name='sector',
    size_max=60,
    color_continuous_scale='Viridis',
    labels={'price': 'Average Price in Crore', 'sector': 'Sector'},
    title='Sector vs Average Price (Bubble = Area, Color = Price/Sqft)'
)

fig_bubble.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig_bubble, use_container_width=True)

# Property type selection
property_type = st.selectbox("Select Property Type", ['flat', 'house'])

# Filter and plot based on selection
if property_type == "house":
    filtered_df = new_df[new_df['property_type'] == 'house']
else:
    filtered_df = new_df[new_df['property_type'] == 'flat']

# Scatter plot
fig1 = px.scatter(
    filtered_df,
    x="built_up_area",
    y="price",
    color="bedRoom",
    title=f"Area vs Price for {property_type.capitalize()}s"
)

st.plotly_chart(fig1, use_container_width=True)
