import streamlit as st
import pandas as pd
from data_processor import load_and_process_data
from visualization import display_delay_by_warehouse_chart, display_delayed_orders_table
from ai_agent import ask_supply_chain_agent

# Configuring Streamlit page
st.set_page_config(page_title="Supply Chain AI Copilot", layout="wide")

st.title("Mini Supply Chain AI Copilot")
st.markdown("Upload your shipment data and ask questions in natural language.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuration")
    
    # Model Selection Dropdown
    model_choice = st.selectbox(
        "Select AI Engine", 
        ["Gemini", "OpenAI", "Claude"],
        index=0 # Setting default model to Gemini
    )
    
    # Dynamic API Key Input based on user selection
    if model_choice == "Gemini":
        api_key = st.text_input("Gemini API Key", type="password")
        st.markdown("[Get key from Google AI Studio](https://aistudio.google.com/app/apikey)")
    elif model_choice == "OpenAI":
        api_key = st.text_input("OpenAI API Key", type="password")
        st.markdown("[Get key from OpenAI Platform](https://platform.openai.com/api-keys)")
    elif model_choice == "Claude":
        api_key = st.text_input("Anthropic API Key", type="password")
        st.markdown("[Get key from Anthropic Console](https://console.anthropic.com/)")
    
    st.divider()
    
    st.header("Data Upload")
    uploaded_file = st.file_uploader("Upload Shipment CSV", type=["csv"])

# --- MAIN APP ---
if uploaded_file is not None:
    # Process and store data in session state to prevent reloading
    if 'df' not in st.session_state or st.session_state.get('last_uploaded') != uploaded_file.name:
        try:
            st.session_state.df = load_and_process_data(uploaded_file)
            st.session_state.last_uploaded = uploaded_file.name
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.stop()

    df = st.session_state.df

    # Display Raw Data & Bonus Features
    with st.expander("View Processed Data & Dashboard", expanded=False):
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            display_delay_by_warehouse_chart(df) #Rendering a bar chart showing average shipping delay by warehouse.
        with col2:
            display_delayed_orders_table(df, threshold=3) #Highlighting and displaying orders delayed beyond a specific threshold (3).

    # AI Chat Interface
    st.divider()
    st.subheader(f"Ask the {model_choice} Copilot")
    st.markdown("Try asking: *'Which warehouse has the highest shipping delay?'* or *'What is the average delay?'*")
    
    user_question = st.text_input("Enter your question:")
    
    if st.button("Ask AI", type="primary"):
        if not api_key:
            st.warning(f"Please enter your {model_choice} API key in the sidebar.")
        elif not user_question:
            st.warning("Please enter a question.")
        else:
            with st.spinner(f"Analyzing data with {model_choice}..."):
                # Passing the model_choice alongside the api_key
                answer = ask_supply_chain_agent(df, user_question, api_key, model_choice)
                st.info(answer)

else:
    st.info("Please upload a CSV file in the sidebar to begin.")