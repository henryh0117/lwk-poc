import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Product, Base

def update_vendors():
    # Target database connection
    target_url = 'postgresql://postgres:ulJYqWqrwrbgGYClrOzyWWgEszWhmNqB@centerbeam.proxy.rlwy.net:36815/railway'
    engine = create_engine(target_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:            
        # Verify the update
        count = session.query(Product).filter(Product.vendor == 'Automann').count()
        total = session.query(Product).count()
        print(f"\nUpdate Summary:")
        print(f"- Total products: {total}")
        print(f"- Products with vendor 'Automann': {count}")
        
    except Exception as e:
        print(f"Error during update: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    update_vendors()
