import pandas as pd
import os
from pathlib import Path
from database import Product, get_db

def load_atrobushing_data():
    """Load and process the AstroBushing spreadsheet into a DataFrame."""
    # Get the path to the Excel file
    base_dir = Path(__file__).parent
    excel_file = base_dir / 'AtroBushing Torque Rod Automation.xlsx'
    
    if not excel_file.exists():
        raise FileNotFoundError(f'Excel file not found at {excel_file}')
    
    # Read the Excel file
    df = pd.read_excel(
        excel_file,
        engine='openpyxl',
        usecols=range(1,7),  # Read columns A through F (0-5)
        sheet_name=0  # Read first sheet only
    )
    # Clean column names - remove whitespace and convert to lowercase
    df.columns = df.columns.str.strip().str.lower()
    
    # Remove any completely empty rows
    df = df.dropna(how='all')
    
    new_products = []
    
    # Iterate through each row in the DataFrame
    for idx, row in df.iterrows():
        for i in range(1, 6):
            # Skip if cell is empty, NaN, or just whitespace
            if pd.isna(row.iloc[i]) or str(row.iloc[i]).strip() == "":
                continue
            
            side_a, side_b = get_sides(i)
            # Create a new Product object
            if ", " in str(row.iloc[i]):
                for sku in str(row.iloc[i]).split(", "):
                    product = Product(
                        sku=sku,
                        c_to_c=str(row.iloc[0]),
                        side_a=side_a,
                        side_b=side_b,
                        vendor="AtroBushing"
                    )
                    new_products.append(product)
                    # print(f"Created product: {product.sku} - {product.side_a} - {product.side_b} - {product.c_to_c}")
            else:
                product = Product(
                    sku=str(row.iloc[i]),
                    c_to_c=str(row.iloc[0]),
                    side_a=side_a,
                    side_b=side_b,
                    vendor="AtroBushing"
                )
                new_products.append(product)
                # print(f"Created product: {product.sku} - {product.side_a} - {product.side_b} - {product.c_to_c}")
    
    return new_products

def get_sides(idx):
    match idx:
        case 1:
            return "Straddle", "Straddle"
        case 2:
            return "Straddle", "Taper"
        case 3:
            return "Taper", "Taper"
        case 4:
            return "Straddle", "Hollow"
        case 5:
            return "Hollow", "Hollow"
        case _:
            return None, None  # default case

def save_products_to_db(products):
    """Save the list of products to the database."""
    db = next(get_db())  # Get database session
    try:
        # Add all products to the session
        for product in products:
            db.add(product)
        # Commit the transaction
        db.commit()
        print(f"Successfully saved {len(products)} products to database")
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        raise e
    finally:
        # Always close the session
        db.close()

if __name__ == '__main__':
    try:
        # Load products from Excel
        products = load_atrobushing_data()
        print(f"Successfully created {len(products)} product objects")
        
        # Print details of first few products
        # for i, product in enumerate(products[:5]):
        #     print(f"\nProduct {i + 1}:")
        #     print(f"  SKU: {product.sku}")
        #     print(f"  Side A: {product.side_a}")
        #     print(f"  Side B: {product.side_b}")
        
        # Save to database
        save_products_to_db(products)
        
    except Exception as e:
        print(f"Error: {e}")