from faker import Faker
from sqlalchemy.orm import Session
from random import randint, uniform, choice
from datetime import datetime
from src.models import CategoriesTable, SubCategoriesTable, ProductTable  # Replace with your actual models

# Initialize Faker instance
faker = Faker()

# Predefined categories and subcategories for realism
CATEGORY_SUBCATEGORY_MAP = {
    "Electronics": ["Smartphones", "Laptops", "Tablets", "Headphones", "Cameras"],
    "Clothing": ["Men's Wear", "Women's Wear", "Children's Wear", "Footwear", "Accessories"],
    "Home Appliances": ["Refrigerators", "Washing Machines", "Microwaves", "Air Conditioners", "Vacuum Cleaners"],
    "Books": ["Fiction", "Non-Fiction", "Science", "History", "Children's Books"],
    "Furniture": ["Living Room", "Bedroom", "Dining Room", "Office Furniture", "Outdoor Furniture"],
}

# Function to seed e-commerce data
def seed_ecommerce_data(session: Session, num_products=100):
    categories = []

    # Create Categories and Subcategories
    for category_name, subcategory_list in CATEGORY_SUBCATEGORY_MAP.items():
        category = CategoriesTable(
            name=category_name,
            desc=f"{category_name} category includes products like {', '.join(subcategory_list)}.",
            created_at=datetime.now()
        )
        session.add(category)
        session.flush()  # Flush to get category ID
        
        # Add subcategories
        for subcategory_name in subcategory_list:
            subcategory = SubCategoriesTable(
                name=subcategory_name,
                desc=f"{subcategory_name} subcategory under {category_name}.",
                category_id=category.id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(subcategory)
            session.flush()  # Flush to get subcategory ID
            categories.append((category, subcategory))

    # Add Products
    for _ in range(num_products):
        category, subcategory = choice(categories)  # Randomly select a category and subcategory
        product = ProductTable(
            name=f"{faker.unique.word().capitalize()} {subcategory.name}",
            category_id=category.id,
            subcategory_id=subcategory.id,
            desc=f"A high-quality {subcategory.name.lower()} product in the {category.name.lower()} category.",
            price=round(uniform(5.0, 2000.0), 2),  # Random price between $5 and $2000
            stock_quantity=randint(10, 500),  # Stock between 10 and 500
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(product)

    # Commit the session
    session.commit()

# Example usage
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Replace with your database URL
    DATABASE_URL = "postgresql+psycopg2://postgres:Admin123@localhost:5432/ecom_db"  # Example: SQLite database
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a session
    session = SessionLocal()

    try:
        # Seed data
        seed_ecommerce_data(session, num_products=200)
        print("E-commerce data seeded successfully!")
    finally:
        session.close()
