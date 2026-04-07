"""
seed_data.py - Add 100 sample menu items with images to your database

Run this AFTER running migrations (alembic upgrade head)
"""

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.models.restaurant import Restaurant
from app.models.menu_item import MenuItem, MenuCategory
from app.core.security import hash_password

db = SessionLocal()

print("=" * 70)
print("🔥 CoalSpark - Adding 100 Menu Items with Images")
print("=" * 70)

# 1. Create Admin if not exists
print("\n✅ Checking admin user...")
admin = db.query(User).filter(User.email == "admin@coalspark.in").first()
if not admin:
    admin = User(
        full_name="Admin User",
        email="admin@coalspark.in",
        hashed_password=hash_password("admin1234"),
        role=UserRole.admin,
        is_active=True
    )
    db.add(admin)
    db.commit()
    print("   Created admin user")
else:
    print("   Admin exists")

# 2. Create Restaurant if not exists
print("\n✅ Checking restaurant...")
restaurant = db.query(Restaurant).first()
if not restaurant:
    restaurant = Restaurant(
        name="CoalSpark Restaurant",
        tagline="Where Fire Meets Flavour",
        address="Gachibowli, Hyderabad",
        city="Hyderabad",
        phone="+91 9876543210",
        email="info@coalspark.in",
        rating=4.5,
        total_reviews=128,
        opening_time="11:00",
        closing_time="23:00",
        is_open="true"
    )
    db.add(restaurant)
    db.commit()
    print("   Created restaurant profile")
else:
    print("   Restaurant exists")

# 3. Add 100 Menu Items
print("🍽️  Adding 100 menu items with images...")

menu_items_data = [

    # ── BBQ (15 items) ────────────────────────────────────────────────────────
    {
        "name": "Smoked BBQ Chicken",
        "description": "Tender chicken marinated in smoky spices, slow-grilled over coal",
        "price": 349.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 3,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=600&q=80"
    },
    {
        "name": "Grilled Paneer Tikka",
        "description": "Cottage cheese grilled in tandoor with spiced yogurt marinade",
        "price": 299.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 2,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=600&q=80"
    },
    {
        "name": "BBQ Lamb Chops",
        "description": "Juicy lamb chops marinated in herbs and grilled to perfection",
        "price": 549.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 3,
        "preparation_time": 30,
        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80"
    },
    {
        "name": "Seekh Kebab",
        "description": "Minced mutton kebabs on skewers with mint chutney",
        "price": 329.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=600&q=80"
    },
    {
        "name": "Grilled Fish Tikka",
        "description": "Fresh fish fillets marinated in ajwain and lemon, char-grilled",
        "price": 399.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1519984388953-d2406bc725e1?w=600&q=80"
    },
    {
        "name": "Mushroom Tikka",
        "description": "Whole button mushrooms marinated in spiced yogurt, grilled",
        "price": 249.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80"
    },
    {
        "name": "Tandoori Prawns",
        "description": "King prawns marinated in tandoori masala, flame-grilled",
        "price": 499.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 3,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80"
    },
    {
        "name": "Corn on the Cob",
        "description": "Sweet corn grilled with butter and chaat masala",
        "price": 129.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=600&q=80"
    },
    {
        "name": "BBQ Pulled Pork Sliders",
        "description": "Slow-smoked pulled pork with coleslaw in soft buns",
        "price": 379.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1553909489-cd47e0907980?w=600&q=80"
    },
    {
        "name": "Smoky Veggie Platter",
        "description": "Assorted grilled vegetables with dips",
        "price": 279.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80"
    },
    {
        "name": "Chicken Shish Tawook",
        "description": "Lebanese-style chicken cubes marinated in garlic and lemon",
        "price": 359.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1515516969-d4008cc6241a?w=600&q=80"
    },
    {
        "name": "Tandoori Raan",
        "description": "Whole leg of lamb slow-roasted in tandoor, serves 2-3",
        "price": 899.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 3,
        "preparation_time": 60,
        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80"
    },
    {
        "name": "Mixed Grill Platter",
        "description": "Chicken tikka, seekh kebab, and paneer tikka combo",
        "price": 699.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 3,
        "preparation_time": 30,
        "image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&q=80"
    },
    {
        "name": "Boti Kebab",
        "description": "Tender mutton pieces marinated overnight in raw papaya",
        "price": 419.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=600&q=80"
    },
    {
        "name": "Grilled Baby Back Ribs",
        "description": "Pork ribs glazed in our signature house BBQ sauce",
        "price": 599.0,
        "category": MenuCategory.bbq.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 40,
        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80"
    },

    # ── BIRYANI & MANDI (15 items) ─────────────────────────────────────────────
    {
        "name": "Chicken Biryani",
        "description": "Aromatic basmati rice with tender chicken and whole spices",
        "price": 329.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 3,
        "preparation_time": 30,
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80"
    },
    {
        "name": "Veg Biryani",
        "description": "Fragrant rice with seasonal vegetables and saffron",
        "price": 249.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1642821373181-696a54913e93?w=600&q=80"
    },
    {
        "name": "Mutton Biryani",
        "description": "Slow-cooked mutton in dum-style biryani with caramelised onions",
        "price": 429.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 4,
        "preparation_time": 45,
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80"
    },
    {
        "name": "Prawn Biryani",
        "description": "Succulent prawns layered with saffron-infused basmati",
        "price": 479.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 3,
        "preparation_time": 35,
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80"
    },
    {
        "name": "Egg Biryani",
        "description": "Boiled eggs in spiced biryani masala with basmati rice",
        "price": 279.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80"
    },
    {
        "name": "Hyderabadi Dum Biryani",
        "description": "Authentic Hyderabadi recipe sealed with dough, cooked on low flame",
        "price": 399.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 4,
        "preparation_time": 50,
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80"
    },
    {
        "name": "Chicken Mandi",
        "description": "Yemeni-style whole chicken slow-roasted over smoked wood",
        "price": 649.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 2,
        "preparation_time": 60,
        "image_url": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=600&q=80"
    },
    {
        "name": "Mutton Mandi",
        "description": "Slow-smoked leg of mutton on fragrant mandi rice",
        "price": 849.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 2,
        "preparation_time": 75,
        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80"
    },
    {
        "name": "Paneer Dum Biryani",
        "description": "Cottage cheese cubes layered with spiced rice, cooked in dum style",
        "price": 299.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 30,
        "image_url": "https://images.unsplash.com/photo-1642821373181-696a54913e93?w=600&q=80"
    },
    {
        "name": "Mushroom Biryani",
        "description": "Earthy mushrooms with whole spices and long-grain basmati",
        "price": 259.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=80"
    },
    {
        "name": "Fish Biryani",
        "description": "Spiced fish pieces layered with aromatic basmati and fried onions",
        "price": 449.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 35,
        "image_url": "https://images.unsplash.com/photo-1519984388953-d2406bc725e1?w=600&q=80"
    },
    {
        "name": "Kheema Biryani",
        "description": "Minced mutton cooked with spices layered over basmati",
        "price": 369.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 35,
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80"
    },
    {
        "name": "Chicken Kabsa",
        "description": "Saudi-style rice with chicken, dried fruits, and nuts",
        "price": 599.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 50,
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80"
    },
    {
        "name": "Kathal Biryani",
        "description": "Raw jackfruit biryani — a rich vegetarian delicacy",
        "price": 269.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 35,
        "image_url": "https://images.unsplash.com/photo-1642821373181-696a54913e93?w=600&q=80"
    },
    {
        "name": "Nawabi Chicken Biryani",
        "description": "Lucknowi-style mild biryani with rose water and kewra",
        "price": 389.0,
        "category": MenuCategory.biryani_mandi.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 40,
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&q=80"
    },

    # ── STARTERS (15 items) ───────────────────────────────────────────────────
    {
        "name": "Chicken Wings",
        "description": "Crispy fried wings tossed in spicy buffalo sauce",
        "price": 279.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 3,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1608039755401-742074f0548d?w=600&q=80"
    },
    {
        "name": "Garlic Bread",
        "description": "Toasted sourdough with garlic butter and parsley",
        "price": 149.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1573140401552-388e7e2f00b8?w=600&q=80"
    },
    {
        "name": "Crispy Calamari",
        "description": "Fried squid rings with aioli dipping sauce",
        "price": 349.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1559847844-5315695dadae?w=600&q=80"
    },
    {
        "name": "Veg Spring Rolls",
        "description": "Crispy rolls stuffed with cabbage, carrot, and glass noodles",
        "price": 199.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80"
    },
    {
        "name": "Chicken 65",
        "description": "Deep-fried spicy chicken pieces with curry leaves and chillies",
        "price": 259.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 4,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1608039755401-742074f0548d?w=600&q=80"
    },
    {
        "name": "Gobi Manchurian",
        "description": "Crispy cauliflower tossed in Indo-Chinese sauce",
        "price": 229.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80"
    },
    {
        "name": "Nachos with Salsa",
        "description": "Tortilla chips with fresh salsa, jalapeños, and sour cream",
        "price": 219.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1582169296194-e4d644c48063?w=600&q=80"
    },
    {
        "name": "Prawn Cocktail",
        "description": "Chilled tiger prawns with classic Marie Rose sauce",
        "price": 399.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80"
    },
    {
        "name": "Bruschetta",
        "description": "Toasted baguette with tomatoes, basil, and balsamic glaze",
        "price": 189.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?w=600&q=80"
    },
    {
        "name": "Chilli Chicken",
        "description": "Wok-tossed chicken with bell peppers in soy-chilli sauce",
        "price": 289.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 4,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1608039755401-742074f0548d?w=600&q=80"
    },
    {
        "name": "Aloo Tikki",
        "description": "Spiced potato patties with green chutney and tamarind",
        "price": 159.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=600&q=80"
    },
    {
        "name": "Hara Bhara Kebab",
        "description": "Spinach and pea patties with paneer stuffing",
        "price": 199.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80"
    },
    {
        "name": "Fish Fingers",
        "description": "Breaded fish strips with tartare sauce",
        "price": 299.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1519984388953-d2406bc725e1?w=600&q=80"
    },
    {
        "name": "Onion Rings",
        "description": "Beer-battered onion rings with ranch dip",
        "price": 169.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1573140401552-388e7e2f00b8?w=600&q=80"
    },
    {
        "name": "Dahi Ke Kebab",
        "description": "Hung curd kebabs with cashew stuffing, pan-fried",
        "price": 229.0,
        "category": MenuCategory.starters.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=600&q=80"
    },

    # ── MAIN COURSE (15 items) ────────────────────────────────────────────────
    {
        "name": "Butter Chicken",
        "description": "Creamy tomato-based curry with tender chicken pieces",
        "price": 369.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 2,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&q=80"
    },
    {
        "name": "Paneer Butter Masala",
        "description": "Rich creamy curry with soft paneer cubes",
        "price": 319.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 2,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&q=80"
    },
    {
        "name": "Mutton Rogan Josh",
        "description": "Kashmiri-style mutton curry with whole spices",
        "price": 469.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 4,
        "preparation_time": 40,
        "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&q=80"
    },
    {
        "name": "Dal Makhani",
        "description": "Black lentils slow-cooked overnight with butter and cream",
        "price": 249.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 1,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&q=80"
    },
    {
        "name": "Chicken Chettinad",
        "description": "Fiery South Indian curry with freshly ground spices",
        "price": 389.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 5,
        "preparation_time": 30,
        "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&q=80"
    },
    {
        "name": "Palak Paneer",
        "description": "Cottage cheese in a smooth spiced spinach gravy",
        "price": 279.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&q=80"
    },
    {
        "name": "Fish Curry",
        "description": "Coastal-style fish in coconut and tamarind gravy",
        "price": 399.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1519984388953-d2406bc725e1?w=600&q=80"
    },
    {
        "name": "Lamb Keema",
        "description": "Minced lamb cooked with peas and aromatic spices",
        "price": 349.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&q=80"
    },
    {
        "name": "Chana Masala",
        "description": "Hearty chickpea curry in tangy spiced tomato base",
        "price": 229.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&q=80"
    },
    {
        "name": "Prawn Masala",
        "description": "Juicy prawns in a rich, spiced masala gravy",
        "price": 459.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=600&q=80"
    },
    {
        "name": "Kadai Paneer",
        "description": "Paneer and bell peppers in a wok-cooked spicy tomato curry",
        "price": 299.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&q=80"
    },
    {
        "name": "Chicken Tikka Masala",
        "description": "Grilled chicken tikka pieces in creamy tomato curry",
        "price": 379.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": False,
        "is_featured": True,
        "spice_level": 2,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&q=80"
    },
    {
        "name": "Mixed Veg Curry",
        "description": "Seasonal vegetables in a light, spiced tomato gravy",
        "price": 219.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 20,
        "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80"
    },
    {
        "name": "Chicken Saag",
        "description": "Chicken cooked with mustard greens and spices",
        "price": 369.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": False,
        "is_featured": False,
        "spice_level": 3,
        "preparation_time": 30,
        "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&q=80"
    },
    {
        "name": "Malai Kofta",
        "description": "Cottage cheese dumplings in creamy cashew-tomato sauce",
        "price": 299.0,
        "category": MenuCategory.main_course.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 25,
        "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&q=80"
    },

    # ── BEVERAGES (15 items) ──────────────────────────────────────────────────
    {
        "name": "Fresh Lime Soda",
        "description": "Refreshing lime juice with soda water, sweet or salted",
        "price": 89.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&q=80"
    },
    {
        "name": "Mango Lassi",
        "description": "Traditional yogurt-based mango drink, chilled",
        "price": 129.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1546173159-315724a31696?w=600&q=80"
    },
    {
        "name": "Cold Coffee",
        "description": "Blended cold coffee with vanilla ice cream and milk",
        "price": 149.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80"
    },
    {
        "name": "Watermelon Juice",
        "description": "Fresh watermelon blended with a pinch of black salt",
        "price": 99.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1497534446932-c925b458314e?w=600&q=80"
    },
    {
        "name": "Mint Lemonade",
        "description": "Fresh lemon squeezed with mint leaves and soda",
        "price": 99.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&q=80"
    },
    {
        "name": "Rose Sharbat",
        "description": "Chilled rose syrup drink with basil seeds",
        "price": 89.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1546173159-315724a31696?w=600&q=80"
    },
    {
        "name": "Masala Chai",
        "description": "Spiced Indian tea with ginger, cardamom, and milk",
        "price": 69.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1561336313-0bd5e0b27ec8?w=600&q=80"
    },
    {
        "name": "Virgin Mojito",
        "description": "Lime, mint, sugar syrup, and soda over crushed ice",
        "price": 129.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&q=80"
    },
    {
        "name": "Strawberry Milkshake",
        "description": "Thick strawberry milkshake with whipped cream",
        "price": 159.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1558301211-0d8c8ddee6ec?w=600&q=80"
    },
    {
        "name": "Coconut Water",
        "description": "Fresh tender coconut served chilled",
        "price": 89.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1565194256564-43c28c6b08ac?w=600&q=80"
    },
    {
        "name": "Iced Americano",
        "description": "Double espresso shot over ice with cold water",
        "price": 149.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80"
    },
    {
        "name": "Jaljeera",
        "description": "Traditional cumin-based tangy Indian cooler",
        "price": 79.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 2,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&q=80"
    },
    {
        "name": "Pineapple Juice",
        "description": "Fresh pineapple blended and served chilled",
        "price": 109.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1497534446932-c925b458314e?w=600&q=80"
    },
    {
        "name": "Salted Lassi",
        "description": "Chilled yogurt drink with roasted cumin and black salt",
        "price": 99.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1546173159-315724a31696?w=600&q=80"
    },
    {
        "name": "Thandai",
        "description": "Chilled milk with almonds, saffron, and rose petals",
        "price": 139.0,
        "category": MenuCategory.beverages.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1546173159-315724a31696?w=600&q=80"
    },

    # ── DESSERTS (20 items) ───────────────────────────────────────────────────
    {
        "name": "Chocolate Brownie",
        "description": "Warm fudge brownie with vanilla ice cream and hot fudge",
        "price": 179.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476d?w=600&q=80"
    },
    {
        "name": "Gulab Jamun",
        "description": "Soft milk dumplings soaked in rose-cardamom syrup",
        "price": 99.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1593297759909-9015765eb784?w=600&q=80"
    },
    {
        "name": "Kulfi Falooda",
        "description": "Traditional saffron ice cream with rose falooda and basil seeds",
        "price": 159.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1560008581-09826d1de69e?w=600&q=80"
    },
    {
        "name": "Rasmalai",
        "description": "Spongy cottage cheese balls in chilled saffron milk",
        "price": 129.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1593297759909-9015765eb784?w=600&q=80"
    },
    {
        "name": "Cheesecake",
        "description": "New York-style baked cheesecake with berry compote",
        "price": 219.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=600&q=80"
    },
    {
        "name": "Gajar Halwa",
        "description": "Slow-cooked carrot pudding with khoya and almonds",
        "price": 139.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1593297759909-9015765eb784?w=600&q=80"
    },
    {
        "name": "Panna Cotta",
        "description": "Italian set cream dessert with strawberry coulis",
        "price": 199.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1560008581-09826d1de69e?w=600&q=80"
    },
    {
        "name": "Tiramisu",
        "description": "Classic Italian dessert with mascarpone and espresso",
        "price": 229.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80"
    },
    {
        "name": "Mango Sorbet",
        "description": "Dairy-free Alphonso mango sorbet, two scoops",
        "price": 149.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1497534446932-c925b458314e?w=600&q=80"
    },
    {
        "name": "Chocolate Lava Cake",
        "description": "Warm chocolate fondant with molten centre and ice cream",
        "price": 249.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 1,
        "preparation_time": 15,
        "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476d?w=600&q=80"
    },
    {
        "name": "Phirni",
        "description": "Chilled rice pudding with nuts, served in clay bowls",
        "price": 119.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1593297759909-9015765eb784?w=600&q=80"
    },
    {
        "name": "Waffles with Ice Cream",
        "description": "Belgian waffles with two scoops of vanilla and chocolate sauce",
        "price": 199.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1519915028121-7d3463d20b13?w=600&q=80"
    },
    {
        "name": "Baklava",
        "description": "Layers of filo pastry with pistachios and honey",
        "price": 179.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1478145046317-39f10e56b5e9?w=600&q=80"
    },
    {
        "name": "Kheer",
        "description": "Creamy rice pudding with cardamom, saffron, and dry fruits",
        "price": 109.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1593297759909-9015765eb784?w=600&q=80"
    },
    {
        "name": "Sticky Toffee Pudding",
        "description": "Date sponge in warm toffee sauce with clotted cream",
        "price": 239.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476d?w=600&q=80"
    },
    {
        "name": "Coconut Ladoo",
        "description": "Sweet coconut balls rolled in desiccated coconut",
        "price": 89.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1593297759909-9015765eb784?w=600&q=80"
    },
    {
        "name": "Churros with Chocolate",
        "description": "Spanish fried dough sticks with rich dark chocolate dip",
        "price": 189.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600&q=80"
    },
    {
        "name": "Rabri Jalebi",
        "description": "Crispy jalebis served with chilled thickened rabri",
        "price": 139.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": True,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1593297759909-9015765eb784?w=600&q=80"
    },
    {
        "name": "Fruit Trifle",
        "description": "Layers of sponge, custard, fresh fruits, and cream",
        "price": 169.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 5,
        "image_url": "https://images.unsplash.com/photo-1560008581-09826d1de69e?w=600&q=80"
    },
    {
        "name": "Shahi Tukda",
        "description": "Fried bread soaked in condensed milk and garnished with nuts",
        "price": 149.0,
        "category": MenuCategory.desserts.value,
        "is_vegetarian": True,
        "is_featured": False,
        "spice_level": 1,
        "preparation_time": 10,
        "image_url": "https://images.unsplash.com/photo-1593297759909-9015765eb784?w=600&q=80"
    },
]

count = 0
for item_data in menu_items_data:
    existing = db.query(MenuItem).filter(MenuItem.name == item_data["name"]).first()
    if not existing:
        menu_item = MenuItem(
            restaurant_id=restaurant.id,
            **item_data
        )
        db.add(menu_item)
        count += 1
        print(f"   ✓ Added: {item_data['name']} - ₹{item_data['price']}")

try:
    db.commit()
    print("\n" + "=" * 70)
    print(f"✅ SUCCESS! Added {count} new menu items!")
    print(f"   Total items defined: {len(menu_items_data)}")
    print("=" * 70)
    print("\n🎯 Next Steps:")
    print("1. Keep backend running: uvicorn main:app --reload")
    print("2. Keep frontend running: npm run dev")
    print("3. Refresh browser: http://localhost:5173")
    print("4. Go to Menu page to see all 100 items!")
    print("\n📊 Category Breakdown:")
    print("   BBQ             → 15 items")
    print("   Biryani & Mandi → 15 items")
    print("   Starters        → 15 items")
    print("   Main Course     → 15 items")
    print("   Beverages       → 15 items")
    print("   Desserts        → 20 items")
    print(f"   TOTAL           → {len(menu_items_data)} items")
    print("=" * 70)
except Exception as e:
    db.rollback()
    print("\n❌ ERROR: Failed to save seed data to database!")
    print(f"   Error details: {e}")
    print("\n⚠️  Check that categories match your PostgreSQL ENUM values.")
finally:
    db.close()