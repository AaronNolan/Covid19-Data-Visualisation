import pandas as pd
from drop import drop_columns

def read_and_clean(name):
    # Read CSV
    df = pd.read_csv("./csv/" + name + ".csv")

    # Drop
    df = df.drop(labels=drop_columns(name), axis=1) # Unwanted columns
    df.drop_duplicates() # Duplicate rows
    df.dropna() # Null rows

    # Filter
    df = df[df['location_key'].str.contains("_", regex=False)==False] # Out sub regions
    if "date" in df.columns:
        df.date = pd.to_datetime(df.date, format="%Y-%m-%d") # .strftime('%Y-%m-%d') # Set date as datetime data type
        df = df[(df.date >= '2020-10-15') & (df.date <= '2022-12-31')] #.dt.strftime('%Y-%m-%d') # Only 2021 dates

    # Sort
    df.sort_values("location_key") # By location

    return df
