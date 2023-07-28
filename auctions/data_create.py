# create_data.py
import os
import random
import string
import django
from django.utils.text import slugify

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commerce.settings")
# Set up Django environment
django.setup()

from auctions.models import User
from auctions.models import Listing, Category


def generate_random_string(length=6):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def generate_random_price():
    return round(random.uniform(10, 5000), 2)


def create_categories():
    for i in range(20):
        name = f"Category {i + 1}"
        slug = slugify(name)
        Category.objects.create(name=name)
    print("Categories created successfully.")


def create_users():
    for i in range(100):
        username = f"user{i + 1}"
        password = "admin"  # You can set any password here
        email = "test@test.com"
        user = User.objects.create_user(username, email, password)
        user.save()
    print("Users created successfully.")


def create_listings():
    categories = Category.objects.all()
    users = User.objects.all()

    for i in range(10000):
        title = f"Title{i + 1}"
        description = generate_random_string(100)
        starting_price = generate_random_price()
        current_price = starting_price
        image_url = f"https://www.shutterstock.com/image-vector/hot-sale-promotion-label-tag-illustration-1410327293"
        category = random.choice(categories)
        creator = random.choice(users)

        listing = Listing.objects.create(
            title=title,
            description=description,
            starting_price=starting_price,
            current_price=current_price,
            image_url=image_url,
            creator=creator,

        )
        listing.categories.add(category)




    print("Listings created successfully.")



if __name__ == "__main__":
    # create_categories()
    # create_users()
    create_listings()
