import pandas as pd

def load_and_process_data(file) -> pd.DataFrame:
    """
    Loads a CSV file and computes Order Processing Time and Shipping Delay.
    """
    try:
        df = pd.read_csv(file)
        
        # To ensure date columns are datetime objects
        date_cols = ['Order_Date', 'Ship_Date', 'Delivery_Date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Order processing time in days
        if 'Ship_Date' in df.columns and 'Order_Date' in df.columns:
            df['Order_Processing_Time'] = (df['Ship_Date'] - df['Order_Date']).dt.days
            
        # Shipping delay in days
        # Delay = Delivery_Date - Ship_Date. If Delivery_Date is missing, we use Ship_Date - Order_Date
        def calculate_delay(row):
            if pd.notnull(row.get('Delivery_Date')):
                return (row['Delivery_Date'] - row['Ship_Date']).days
            elif pd.notnull(row.get('Ship_Date')) and pd.notnull(row.get('Order_Date')):
                return (row['Ship_Date'] - row['Order_Date']).days
            return None

        if 'Ship_Date' in df.columns:
            df['Shipping_Delay'] = df.apply(calculate_delay, axis=1)
            
        return df
    except Exception as e:
        raise ValueError(f"Error processing data: {str(e)}")