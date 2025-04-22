import random
from faker import Faker
from datetime import datetime, timezone
from mongoengine import connect, DoesNotExist
from nosql_products.models_nosql import Category, Product
from nosql_users.models_nosql import BrowsingHistory, Wishlist
from nosql_notifications.models_nosql import UserNotification, AdminLog, ErrorLog

fake = Faker()

# MongoDB connection setup
connect('telangana_handicrafts_db', host='localhost', port=27017)  # Adjust based on your MongoDB settings

def seed_categories():
    categories = ['Art', 'Clothing', 'Accessories', 'Home Decor', 'Jewelry']
    for category in categories:
        # Check if the category already exists before saving
        if not Category.objects(name=category):
            Category(name=category).save()
    print("Categories seeded")
    print(Category.objects.all())  # Verify categories are saved

def seed_products():
    categories = Category.objects.all()  # Fetch categories first
    if not categories:
        print("No categories found. Exiting product seeding.")
        return  # Skip seeding products if there are no categories

    for _ in range(10):  # Seed 10 products
        category = random.choice(categories)  # Ensure category is chosen from the list of valid categories
        product = Product(
            name=fake.word(),
            description=fake.text(),
            price=random.randint(100, 1000),
            stock=random.randint(1, 100),  # Stock quantity
            category=category,  # Ensure valid category is assigned
            images=[fake.image_url() for _ in range(3)],
            tags=[fake.word() for _ in range(3)],
            available=True
        )
        product.save()
    print("Products seeded")

def seed_browsing_history():
    users = ['user1', 'user2', 'user3', 'user4', 'user5']  # List of user IDs from SQL
    products = Product.objects.all()
    for _ in range(20):  # Seed 20 browsing history entries
        user_id = random.choice(users)
        product = random.choice(products)
        if isinstance(user_id, str):  # Ensure user_id is a string
            BrowsingHistory(
                user_id=user_id,
                product=product,
                viewed_at=datetime.now(timezone.utc)
            ).save()
    print("Browsing history seeded")

def seed_wishlist():
    Wishlist.objects.delete()  # Clear all wishlists first
    products = list(Product.objects.all())
    for user in range(1, 11):
        product_ids = random.sample(products, random.randint(1, 5))
        wishlist = Wishlist(user_id=str(user), product_ids=product_ids)
        wishlist.save()
    print("Wishlists seeded")

def seed_user_notifications():
    users = ['user1', 'user2', 'user3', 'user4', 'user5']  # List of user IDs
    for user_id in users:
        notification = UserNotification(
            user_id=user_id,
            title=fake.sentence(),
            message=fake.text(),
            read=random.choice([True, False])
        )
        notification.save()
    print("User notifications seeded")

def seed_admin_logs():
    admins = ['admin1', 'admin2']  # List of admin IDs
    actions = ['Product added', 'Product removed', 'Category updated', 'User reported']
    for admin_id in admins:
        log = AdminLog(
            admin_id=admin_id,
            action=random.choice(actions),
            details=fake.text()
        )
        log.save()
    print("Admin logs seeded")

def seed_error_logs():
    error_types = ['DatabaseError', 'ValidationError', 'TimeoutError', 'ConnectionError']
    for _ in range(10):  # Seed 10 error logs
        error_log = ErrorLog(
            error_type=random.choice(error_types),
            message=fake.text()
        )
        error_log.save()
    print("Error logs seeded")

def main():
    print("Starting seed data process...")
    seed_categories()  # Seed categories first
    seed_products()  # Seed products
    seed_browsing_history()  # Seed browsing history
    seed_wishlist()  # Seed wishlists
    seed_user_notifications()  # Seed user notifications
    seed_admin_logs()  # Seed admin logs
    seed_error_logs()  # Seed error logs
    print("Seed data process completed.")

if __name__ == "__main__":
    main()

# Cleanup invalid products
print("Cleaning up products with invalid categories...")
for product in Product.objects:
    try:
        if product.category:
            _ = product.category  # Tries to dereference the reference field
    except DoesNotExist:
        print(f"Deleting product with invalid category: {product.name}")
        product.delete()
print("Cleanup done.")
