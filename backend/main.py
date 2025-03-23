import os
import logging
import time
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db, Product
from sqlalchemy import text
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Duration: {duration:.3f}s Status: {response.status_code}"
    )
    return response

# Configure CORS
# Get CORS origins from environment variable
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, 'https://nextjs-frontend-production-c9b5.up.railway.app'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from typing import Optional

class ProductSearch(BaseModel):
    sku: Optional[str] = None
    type1: Optional[str] = None
    type2: Optional[str] = None
    c_to_c: Optional[str] = None
    side_a: Optional[str] = None
    side_b: Optional[str] = None
    side_a_bushing: Optional[str] = None
    side_b_bushing: Optional[str] = None
    side_a_angle: Optional[str] = None
    side_b_angle: Optional[str] = None
    shaft_dia: Optional[str] = None
    notes: Optional[str] = None

@app.get("/")
def read_root():
    try:
        # Test database connection
        db = next(get_db())
        db.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return {"message": "Welcome to the Product Search API", "status": "healthy"}
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Database connection error. Please try again later."
        )

@app.post("/api/products/search")
def search_products(search_query: ProductSearch, db: Session = Depends(get_db)):
    logger.info(f"Received search query: {search_query.dict(exclude_none=True)}")
    try:
        # Using parameterized query to prevent SQL injection
        # Build the WHERE clause dynamically based on non-null fields
        conditions = []
        params = {}

        if search_query.sku:
            conditions.append("sku ILIKE :sku")
            params['sku'] = f'%{search_query.sku}%'
        if search_query.type1:
            conditions.append("type1 ILIKE :type1")
            params['type1'] = f'%{search_query.type1}%'
        if search_query.type2:
            conditions.append("type2 ILIKE :type2")
            params['type2'] = f'%{search_query.type2}%'
        if search_query.c_to_c:
            conditions.append("c_to_c ILIKE :c_to_c")
            params['c_to_c'] = f'%{search_query.c_to_c}%'
        if search_query.side_a:
            conditions.append("side_a ILIKE :side_a")
            params['side_a'] = f'%{search_query.side_a}%'
        if search_query.side_b:
            conditions.append("side_b ILIKE :side_b")
            params['side_b'] = f'%{search_query.side_b}%'
        if search_query.side_a_bushing:
            conditions.append("side_a_bushing ILIKE :side_a_bushing")
            params['side_a_bushing'] = f'%{search_query.side_a_bushing}%'
        if search_query.side_b_bushing:
            conditions.append("side_b_bushing ILIKE :side_b_bushing")
            params['side_b_bushing'] = f'%{search_query.side_b_bushing}%'
        if search_query.side_a_angle:
            conditions.append("side_a_angle ILIKE :side_a_angle")
            params['side_a_angle'] = f'%{search_query.side_a_angle}%'
        if search_query.side_b_angle:
            conditions.append("side_b_angle ILIKE :side_b_angle")
            params['side_b_angle'] = f'%{search_query.side_b_angle}%'
        if search_query.shaft_dia:
            conditions.append("shaft_dia ILIKE :shaft_dia")
            params['shaft_dia'] = f'%{search_query.shaft_dia}%'
        if search_query.notes:
            conditions.append("notes ILIKE :notes")
            params['notes'] = f'%{search_query.notes}%'

        # If no search criteria provided, return empty list
        if not conditions:
            return []

        # Combine all conditions with AND
        where_clause = " AND ".join(conditions)
        
        query = text(f"""
            SELECT * FROM torque_rods 
            WHERE {where_clause}
        """)

        logger.debug(f"Executing query: {query}")
        logger.debug(f"Query parameters: {params}")
        
        try:
            result = db.execute(query, params)
            products = [dict(row._mapping) for row in result]
            logger.info(f"Found {len(products)} matching products")
            return {"products": products}
        except SQLAlchemyError as e:
            logger.error(f"Database error during product search: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Database error occurred while searching products"
            )
    except Exception as e:
        logger.error(f"Error processing search request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your request"
        )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
