"""
check_enum_values.py - Verify MenuCategory ENUM values in database
"""

from sqlalchemy import text
from app.db.session import SessionLocal

db = SessionLocal()

print("=" * 70)
print("🔍 Checking MenuCategory ENUM Values in Database")
print("=" * 70)

try:
    # Query to get enum values
    result = db.execute(text("""
        SELECT unnest(enum_range(NULL::menucategory))
    """))
    
    enum_values = [row[0] for row in result]
    
    print("\n✅ Valid ENUM values:")
    for i, value in enumerate(enum_values, 1):
        print(f"   {i}. '{value}'")
    
    print("\n💡 Usage:")
    print("   Use EXACTLY these values (case-sensitive!)")
    print("   Example: category='BBQ' (not 'bbq')")
    
except Exception as e:
    print(f"\n❌ Error checking enum values: {e}")
    print("\n⚠️  This might be SQLite (no ENUM support)")
    print("   For development, consider using string categories directly")

finally:
    db.close()

print("\n" + "=" * 70)
