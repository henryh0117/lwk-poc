import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Product, Base
from dotenv import load_dotenv

load_dotenv()

def setup_connection(url):
    # Ensure URL uses postgresql:// instead of postgres://
    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    return Session()

def migrate_data():
    # Source (local) database connection
    source_url = 'postgresql://postgres:password@localhost:5432/lwk_scraping'
    source_session = setup_connection(source_url)
    
    # Target (remote) database connection
    target_url = ''
    target_session = setup_connection(target_url)
    
    try:
        # Get all products from source database
        source_products = source_session.query(Product).all()
        print(f"Found {len(source_products)} products in source database")
        
        # Create table in target database if it doesn't exist
        engine = create_engine(target_url)
        Base.metadata.create_all(engine)
        
        # Copy each product to target database
        for product in source_products:
            # Create new product object for target database
            new_product = Product(
                sku=product.sku,
                type1=product.type1,
                type2=product.type2,
                c_to_c=product.c_to_c,
                side_a=product.side_a,
                side_b=product.side_b,
                side_a_bushing=product.side_a_bushing,
                side_b_bushing=product.side_b_bushing,
                side_a_angle=product.side_a_angle,
                side_b_angle=product.side_b_angle,
                shaft_dia=product.shaft_dia,
                notes=product.notes
            )
            target_session.add(new_product)
            
        # Commit changes to target database
        target_session.commit()
        print("Data migration completed successfully!")
        
        # Verify the number of records in target database
        count = target_session.query(Product).count()
        print(f"Total records in target database: {count}")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        target_session.rollback()
    finally:
        source_session.close()
        target_session.close()

if __name__ == "__main__":
    migrate_data()
