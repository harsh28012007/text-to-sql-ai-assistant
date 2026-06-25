import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv("amazon.csv")

# Clean column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Convert price column if needed
if "discounted_price" in df.columns:
    df["discounted_price"] = (
        df["discounted_price"]
        .astype(str)
        .str.replace("₹", "")
        .str.replace(",", "")
        .astype(float)
    )

# Create database
engine = create_engine("sqlite:///./amazon.db")

# Save table
df.to_sql("amazon", engine, if_exists="replace", index=False)

print("Database created successfully")