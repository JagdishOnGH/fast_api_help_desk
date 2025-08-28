from app.models.category import Category
from app.models.subcategory import Subcategory
from app.database import SessionLocal

def seed_categories():
    db = SessionLocal()
    try:
        data = [
            {
                "name": "Technical Issue",
                "description": "Issues related to connectivity or speed",
                "subcategories": ["Slow Internet", "No Internet", "Fiber Breakage"]
            },
            {
                "name": "General Inquiry",
                "description": "General questions and support",
                "subcategories": []
            },
            {
                "name": "Package Inquiry",
                "description": "Queries about internet packages",
                "subcategories": []
            },
            {
                "name": "Recharge Inquiry",
                "description": "Issues with recharge or payment",
                "subcategories": []
            },
            {
                "name": "Router Replacement",
                "description": "Requests for router replacement",
                "subcategories": []
            },
        ]

        for entry in data:
            category = db.query(Category).filter(Category.name == entry["name"]).first()
            if not category:
                category = Category(name=entry["name"], description=entry["description"])
                db.add(category)
                db.commit()
                db.refresh(category)

            # Add subcategories
            for sub in entry["subcategories"]:
                exists = db.query(Subcategory).filter(
                    Subcategory.name == sub,
                    Subcategory.category_id == category.id
                ).first()
                if not exists:
                    db.add(Subcategory(name=sub, category_id=category.id))

        db.commit()
    finally:
        db.close()


