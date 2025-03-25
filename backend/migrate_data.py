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
        
        # Get existing SKUs from target database
        existing_skus = {p.sku for p in target_session.query(Product.sku).all()}
        print(f"Found {len(existing_skus)} existing products in target database")
        
        # Track statistics
        new_count = 0
        skip_count = 0
        
        # Copy each product to target database if it doesn't exist
        for product in source_products:
            if product.sku in existing_skus:
                skip_count += 1
                continue
                
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
                notes=product.notes,
                vendor=product.vendor
            )
            target_session.add(new_product)
            # print(f"Added product: {new_product.sku} - {new_product.side_a} - {new_product.side_b} - {new_product.c_to_c}")
            new_count += 1
            
            # Commit in batches of 100 to avoid memory issues
            if new_count % 100 == 0:
                target_session.commit()
                # print(f"Committed {new_count} new products so far...")
        
        # Final commit for any remaining products
        if new_count % 100 != 0:
            target_session.commit()
        
        print("\nMigration Summary:")
        print(f"- Skipped {skip_count} existing products")
        print(f"- Added {new_count} new products")
        print(f"- Total products in target database: {target_session.query(Product).count()}")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        target_session.rollback()
    finally:
        source_session.close()
        target_session.close()

if __name__ == "__main__":
    target_url = 'postgresql://postgres:ulJYqWqrwrbgGYClrOzyWWgEszWhmNqB@centerbeam.proxy.rlwy.net:36815/railway' 
    target_session = setup_connection(target_url)
    print(f"Total products in target database: {target_session.query(Product).count()}")
    # migrate_data()
