import streamlit as st
import plotly.express as px
import pandas as pd

def display_delay_by_warehouse_chart(df: pd.DataFrame):
    """Renders a bar chart showing average shipping delay by warehouse."""
    if 'Warehouse' in df.columns and 'Shipping_Delay' in df.columns:
        st.subheader("Average Shipping Delay by Warehouse")
        avg_delay = df.groupby('Warehouse')['Shipping_Delay'].mean().reset_index()
        fig = px.bar(avg_delay, x='Warehouse', y='Shipping_Delay', 
                     title="Average Delay (Days)", text_auto=True, color='Warehouse')
        st.plotly_chart(fig, use_container_width=True)

def display_delayed_orders_table(df: pd.DataFrame, threshold: int = 3):
    """Highlights and displays orders delayed beyond a specific threshold."""
    if 'Shipping_Delay' in df.columns:
        st.subheader(f"Orders Delayed More Than {threshold} Days")
        delayed_df = df[df['Shipping_Delay'] > threshold]
        
        if delayed_df.empty:
            st.success(f"No orders delayed beyond {threshold} days!")
        else:
            # Highlighting high delays in red
            st.dataframe(delayed_df.style.map(
                lambda x: 'background-color: #ff0000' if isinstance(x, (int, float)) and x > threshold else '', 
                subset=['Shipping_Delay']
            ), use_container_width=True)