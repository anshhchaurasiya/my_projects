# import streamlit as st
# import time
# import numpy as np
# import pandas as pd
# import pickle

# st.set_page_config(page_title="demo", page_icon="📈")

# # Load Data and Pipeline
# with open("df.pkl", "rb") as file:
#     df = pickle.load(file)
# with open("pipeline.pkl", "rb") as file:
#     pipeline = pickle.load(file)

# # UI Inputs
# st.header("Enter your inputs")
# property_type = st.selectbox("Property Type", ["flat", "house"])
# sector = st.selectbox('Sector', sorted(df["sector"].unique().tolist()))
# bedrooms = float(st.selectbox('Number of Bedroom', sorted(df["bedRoom"].unique().tolist())))
# bathroom = float(st.selectbox('Number of Bathrooms', sorted(df["bathroom"].unique().tolist())))
# balcony = st.selectbox('Balconies', sorted(df["balcony"].unique().tolist()))
# property_age = st.selectbox('Property Age', sorted(df["agePossession"].unique().tolist()))
# built_up_area = float(st.number_input('Built Up Area'))
# servant_room = float(st.selectbox("Servant Room", [0.0, 1.0]))
# store_room = float(st.selectbox("Store Room", [0.0, 1.0]))
# furnishing_type = st.selectbox("Furnishing Type", sorted(df["furnishing_type"].unique().tolist()))
# luxury_category = st.selectbox("Luxury Category", sorted(df['luxury_category'].unique().tolist()))
# floor_category = st.selectbox("Floor Category", sorted(df["floor_category"].unique().tolist()))

# if st.button("Predict"):
#     data = [[property_type, sector, bedrooms, bathroom, balcony, property_age,
#              built_up_area, servant_room, store_room, furnishing_type,
#              luxury_category, floor_category]]

#     columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
#                'agePossession', 'built_up_area', 'servant room', 'store room',
#                'furnishing_type', 'luxury_category', 'floor_category']

#     one_df = pd.DataFrame(data, columns=columns)

#     base_price = np.expm1(pipeline.predict(one_df))[0]
#     low = round(base_price - 0.22, 2)
#     high = round(base_price + 0.22, 2)

#     # st.success(f"🏠 **Estimated Price Range:** ₹ **{low} Cr** — ₹ **{high} Cr**")
#     st.markdown(
#     f"""
#     <div style='
#         background-color:#111827;
#         padding:20px;
#         border-radius:12px;
#         color:white;
#         font-family:monospace;
#         box-shadow:0 4px 12px rgba(0,0,0,0.5);
#     '>
#         <h3 style='margin-bottom:10px;'>📈 Property Price Forecast</h3>
#         <div style='
#             font-size:24px;
#             display:flex;
#             justify-content:space-between;
#             align-items:center;
#         '>
#             <span style='color:#10b981;'>🔻 ₹ {low:,.2f} Cr</span>
#             <span style='color:#facc15;'>—</span>
#             <span style='color:#ef4444;'>🔺 ₹ {high:,.2f} Cr</span>
#         </div>
#         <p style='font-size:13px;margin-top:10px;color:#9ca3af;'>Based on current market trends and inputs provided</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

import streamlit as st
import numpy as np
import pandas as pd
import pickle
import plotly.graph_objects as go

st.set_page_config(page_title="Smart Property Price Estimator", page_icon="🏠", layout="wide")

# Load data and model
with open("df.pkl", "rb") as file:
    df = pickle.load(file)

with open("pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)

# Sidebar Inputs
st.sidebar.header("🔧 Property Configuration")
property_type = st.sidebar.selectbox("🏘️ Property Type", ["flat", "house"])
sector = st.sidebar.selectbox('📍 Sector', sorted(df["sector"].unique()))
bedrooms = float(st.sidebar.selectbox('🛏️ Bedrooms', sorted(df["bedRoom"].unique())))
bathroom = float(st.sidebar.selectbox('🚿 Bathrooms', sorted(df["bathroom"].unique())))
balcony = st.sidebar.selectbox('🌤️ Balconies', sorted(df["balcony"].unique()))
property_age = st.sidebar.selectbox('🏗️ Property Age', sorted(df["agePossession"].unique()))
built_up_area = float(st.sidebar.number_input('📐 Built-Up Area (sq. ft)', min_value=100.0))
servant_room = float(st.sidebar.selectbox("👤 Servant Room", [0.0, 1.0]))
store_room = float(st.sidebar.selectbox("📦 Store Room", [0.0, 1.0]))
furnishing_type = st.sidebar.selectbox("🛋️ Furnishing", sorted(df["furnishing_type"].unique()))
luxury_category = st.sidebar.selectbox("💎 Luxury Category", sorted(df['luxury_category'].unique()))
floor_category = st.sidebar.selectbox("🏢 Floor Category", sorted(df["floor_category"].unique()))

# Main Display
st.title("🏡 Smart Property Price Estimator")
st.markdown("Get an AI-powered forecast for your dream property in seconds.")

# Predict Button
if st.button("🔮 Predict Price"):

    # Prepare Input
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age,
             built_up_area, servant_room, store_room, furnishing_type,
             luxury_category, floor_category]]

    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    input_df = pd.DataFrame(data, columns=columns)

    # Predict
    base_price = np.expm1(pipeline.predict(input_df))[0]
    low = round(base_price - 0.22, 2)
    high = round(base_price + 0.22, 2)

    # Display Gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=base_price,
        delta={'reference': base_price - 0.5, 'increasing': {'color': "red"}},
        title={'text': "Estimated Property Price (Cr)", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, base_price + 2]},
            'bar': {'color': "#10b981"},
            'steps': [
                {'range': [0, base_price], 'color': '#d1fae5'},
                {'range': [base_price, base_price + 2], 'color': '#fef9c3'}
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Price range box
    st.markdown(
        f"""
        <div style='
            background-color:#1f2937;
            padding:20px;
            border-radius:12px;
            color:white;
            font-family:monospace;
            text-align:center;
            margin-top:20px;
        '>
            <h3>📊 Estimated Price Range</h3>
            <p style='font-size:22px;'>
                <span style='color:#10b981;'>₹ {low} Cr</span>
                <strong style='color:#facc15;'> — </strong>
                <span style='color:#ef4444;'>₹ {high} Cr</span>
            </p>
            <p style='font-size:13px;color:#9ca3af;'>Based on property trends & AI model insights</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    

   

