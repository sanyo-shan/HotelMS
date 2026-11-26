"""
Seed the database with fictional hotels located in Indian cities.

Place this file at:
    <your_app>/management/commands/seed_hotels.py
(make sure both `management/` and `commands/` contain an empty __init__.py)

Usage:
    python manage.py seed_hotels              # creates 100 hotels
    python manage.py seed_hotels --count 50   # creates 50 hotels
    python manage.py seed_hotels --clear      # deletes existing hotels first
"""

import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from ...models import Amenity, Hotel  # relative import: works from any app name


# (city, state, pincode prefix)
CITIES = [
    ("Mumbai", "Maharashtra", "400"),
    ("Pune", "Maharashtra", "411"),
    ("Nagpur", "Maharashtra", "440"),
    ("New Delhi", "Delhi", "110"),
    ("Bengaluru", "Karnataka", "560"),
    ("Mysuru", "Karnataka", "570"),
    ("Hyderabad", "Telangana", "500"),
    ("Chennai", "Tamil Nadu", "600"),
    ("Coimbatore", "Tamil Nadu", "641"),
    ("Madurai", "Tamil Nadu", "625"),
    ("Kolkata", "West Bengal", "700"),
    ("Darjeeling", "West Bengal", "734"),
    ("Jaipur", "Rajasthan", "302"),
    ("Udaipur", "Rajasthan", "313"),
    ("Jodhpur", "Rajasthan", "342"),
    ("Jaisalmer", "Rajasthan", "345"),
    ("Ahmedabad", "Gujarat", "380"),
    ("Vadodara", "Gujarat", "390"),
    ("Panaji", "Goa", "403"),
    ("Kochi", "Kerala", "682"),
    ("Thiruvananthapuram", "Kerala", "695"),
    ("Munnar", "Kerala", "685"),
    ("Lucknow", "Uttar Pradesh", "226"),
    ("Agra", "Uttar Pradesh", "282"),
    ("Varanasi", "Uttar Pradesh", "221"),
    ("Amritsar", "Punjab", "143"),
    ("Chandigarh", "Chandigarh", "160"),
    ("Shimla", "Himachal Pradesh", "171"),
    ("Manali", "Himachal Pradesh", "175"),
    ("Dehradun", "Uttarakhand", "248"),
    ("Rishikesh", "Uttarakhand", "249"),
    ("Bhopal", "Madhya Pradesh", "462"),
    ("Indore", "Madhya Pradesh", "452"),
    ("Bhubaneswar", "Odisha", "751"),
    ("Puri", "Odisha", "752"),
    ("Visakhapatnam", "Andhra Pradesh", "530"),
    ("Vijayawada", "Andhra Pradesh", "520"),
    ("Guwahati", "Assam", "781"),
    ("Gangtok", "Sikkim", "737"),
    ("Srinagar", "Jammu and Kashmir", "190"),
    ("Patna", "Bihar", "800"),
    ("Raipur", "Chhattisgarh", "492"),
    ("Ranchi", "Jharkhand", "834"),
    ("Puducherry", "Puducherry", "605"),
    ("Port Blair", "Andaman and Nicobar Islands", "744"),
]

NAME_PREFIXES = [
    "The Grand", "Royal", "Taj View", "Silver Oak", "Lotus", "Heritage",
    "Sapphire", "Emerald", "Golden Palm", "Blue Lagoon", "Sunrise", "Orchid",
    "Maharaja", "Banyan Tree", "Peacock", "Coral Bay", "Imperial", "Saffron",
    "Monsoon", "Kesari", "Neelam", "Chandni", "Mayur", "Shanti",
]

NAME_SUFFIXES = [
    "Residency", "Palace", "Inn", "Suites", "Retreat", "Resort",
    "Regency", "Plaza", "Grand", "Stay", "Heritage Hotel", "Boutique Hotel",
]

STREETS = [
    "MG Road", "Station Road", "Lake View Road", "Gandhi Nagar", "Nehru Street",
    "Civil Lines", "Park Street", "Mall Road", "Beach Road", "Ring Road",
    "Temple Street", "Market Road", "Rajpath Avenue", "Hill View Road",
]

AMENITIES = {
    "Free Wi-Fi": "High-speed wireless internet throughout the property.",
    "Swimming Pool": "Outdoor pool open from 7 AM to 9 PM.",
    "Spa": "Full-service spa with Ayurvedic treatments.",
    "Fitness Centre": "24-hour gym with modern equipment.",
    "Restaurant": "On-site multi-cuisine restaurant.",
    "Room Service": "In-room dining available around the clock.",
    "Free Parking": "Complimentary on-site parking.",
    "Airport Shuttle": "Pick-up and drop to the nearest airport.",
    "Air Conditioning": "Climate control in all rooms.",
    "Bar": "Lounge bar serving drinks and snacks.",
    "Conference Hall": "Meeting and event space for up to 200 guests.",
    "Laundry Service": "Same-day laundry and dry cleaning.",
    "Breakfast Included": "Complimentary buffet breakfast.",
    "Pet Friendly": "Pets allowed on request.",
    "Kids Play Area": "Supervised play zone for children.",
    "24-Hour Front Desk": "Reception staffed day and night.",
}

# Price ranges (INR per night) by star tier, so price and rating stay consistent
TIERS = [
    # (min_rating, max_rating, min_price, max_price, amenity_count_range)
    (3.0, 3.6, 1200, 3500, (3, 6)),
    (3.6, 4.3, 3500, 9000, (5, 10)),
    (4.3, 5.0, 9000, 45000, (9, 16)),
]


class Command(BaseCommand):
    help = "Create fictional hotels in Indian cities for development/testing."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=100, help="Number of hotels to create")
        parser.add_argument("--clear", action="store_true", help="Delete existing hotels first")
        parser.add_argument("--seed", type=int, default=42, help="Random seed for repeatable data")

    def handle(self, *args, **options):
        count = options["count"]
        random.seed(options["seed"])

        max_unique = len(NAME_PREFIXES) * len(NAME_SUFFIXES) * len(CITIES)
        if count > max_unique:
            self.stderr.write(f"Can create at most {max_unique} unique hotels.")
            return

        with transaction.atomic():
            if options["clear"]:
                deleted, _ = Hotel.objects.all().delete()
                self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing records."))

            amenities = self.create_amenities()
            hotels = self.create_hotels(count, amenities)

        self.stdout.write(self.style.SUCCESS(f"Created {len(hotels)} hotels and {len(amenities)} amenities."))

    def create_amenities(self):
        amenities = []
        for name, description in AMENITIES.items():
            amenity, _ = Amenity.objects.get_or_create(
                name=name, defaults={"description": description}
            )
            amenities.append(amenity)
        return amenities

    def create_hotels(self, count, amenities):
        used_names = set(Hotel.objects.values_list("name", flat=True))
        created = []

        while len(created) < count:
            city, state, pin_prefix = random.choice(CITIES)
            name = f"{random.choice(NAME_PREFIXES)} {random.choice(NAME_SUFFIXES)} {city}"
            if name in used_names:
                continue
            used_names.add(name)

            min_r, max_r, min_p, max_p, (min_a, max_a) = random.choice(TIERS)
            slug = slugify(name)

            hotel = Hotel.objects.create(
                name=name,
                price=Decimal(random.randrange(min_p, max_p, 50)).quantize(Decimal("0.01")),
                rating=Decimal(str(round(random.uniform(min_r, max_r), 2))),
                address=f"{random.randint(1, 250)}, {random.choice(STREETS)}, {city}",
                city=city,
                state=state,
                country="India",
                zip_code=f"{pin_prefix}{random.randint(1, 99):03d}",
                # Fictional numbers in valid Indian mobile format
                phone_number=f"+91 {random.choice('6789')}{random.randint(100000000, 999999999)}",
                # example.com domains are reserved, so these never reach a real business
                email=f"reservations@{slug}.example.com",
                website=f"https://{slug}.example.com" if random.random() > 0.2 else None,
            )
            hotel.amenities.set(random.sample(amenities, random.randint(min_a, max_a)))
            created.append(hotel)

        return created