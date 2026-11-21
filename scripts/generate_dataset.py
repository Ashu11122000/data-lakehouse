"""
Generate sample structured customer data and unstructured customer metadata
for the Local Data Lakehouse assignment.
"""

import csv
import json
import random
from datetime import date, timedelta

from config.settings import (
    STRUCTURED_SOURCE_DIR,
    UNSTRUCTURED_SOURCE_DIR,
    SAMPLE_RECORD_COUNT,
    RANDOM_SEED,
)


# ---------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------

random.seed(RANDOM_SEED)


# ---------------------------------------------------------
# Sample Data
# ---------------------------------------------------------

FIRST_NAMES = [
    "Rahul", "Priya", "Amit", "Neha", "Rohan", "Ananya",
    "Vikram", "Sneha", "Arjun", "Kavya", "Aditya", "Meera",
    "Karan", "Ishita", "Sahil", "Pooja", "Nikhil", "Simran",
    "Varun", "Riya", "Manish", "Aarav", "Shreya", "Dev"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Patel", "Mehta",
    "Kumar", "Malhotra", "Kapoor", "Joshi", "Chopra", "Bansal",
    "Agarwal", "Reddy", "Das", "Mishra", "Sethi", "Khanna"
]

CITIES = [
    "Chandigarh", "Delhi", "Mumbai", "Pune", "Bengaluru",
    "Hyderabad", "Jaipur", "Chennai", "Kolkata", "Lucknow",
    "Ahmedabad", "Gurugram", "Noida", "Panchkula", "Indore"
]

COUNTRY = "India"

CUSTOMER_SEGMENTS = [
    "Basic",
    "Standard",
    "Premium",
    "VIP"
]

PRODUCT_CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home Appliances",
    "Books",
    "Sports",
    "Beauty",
    "Accessories",
    "Gaming"
]

SENTIMENTS = [
    "Positive",
    "Neutral",
    "Negative"
]


# ---------------------------------------------------------
# Text Metadata Templates
# ---------------------------------------------------------

FEEDBACK_TEMPLATES = {
    "Positive": [
        "The overall shopping experience was excellent and delivery was fast.",
        "I am very satisfied with the product quality and customer service.",
        "The products are good quality and the ordering process was smooth.",
        "I had a great experience and would recommend the store to others.",
        "The delivery experience was excellent and the product met expectations.",
    ],

    "Neutral": [
        "The product was delivered on time and works as expected.",
        "The shopping experience was satisfactory.",
        "The product is acceptable and meets my basic requirements.",
        "The service was average and there is room for improvement.",
        "The order was completed without any major issues.",
    ],

    "Negative": [
        "The delivery was delayed and the customer experience was disappointing.",
        "I experienced problems with the product and customer service.",
        "The product quality was below my expectations.",
        "The order process was confusing and needs improvement.",
        "I am dissatisfied with the delivery and overall experience.",
    ],
}


SUPPORT_NOTE_TEMPLATES = [
    "Customer contacted support regarding order tracking.",
    "Customer requested information about product availability.",
    "Customer asked about the return and refund process.",
    "Customer contacted support for assistance with account information.",
    "Customer requested help with product specifications.",
    "Support team provided assistance with a delivery issue.",
    "Customer asked about warranty and replacement options.",
    "Customer requested clarification regarding payment status.",
    "Customer contacted support regarding a promotional offer.",
    "No major support issues were reported during this period.",
]


MARKETING_NOTE_TEMPLATES = [
    "Customer may be interested in personalized product recommendations.",
    "Suitable for seasonal promotional campaigns.",
    "Customer responds to product category recommendations.",
    "Consider loyalty program engagement opportunities.",
    "Potential target for new product announcements.",
    "Customer may benefit from personalized discount offers.",
    "Potential candidate for cross-selling related products.",
    "Consider sending relevant product updates.",
]


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def generate_customer_id(index):
    """Generate a unique customer ID."""

    return f"CUST-{1000 + index}"


def generate_email(first_name, last_name, customer_id):
    """Generate a unique sample email address."""

    return (
        f"{first_name.lower()}."
        f"{last_name.lower()}."
        f"{customer_id.lower()}@example.com"
    )


def generate_signup_date():
    """Generate a signup date within the past five years."""

    start_date = date(2021, 1, 1)
    end_date = date(2026, 11, 1)

    days_between = (end_date - start_date).days

    random_days = random.randint(0, days_between)

    return start_date + timedelta(days=random_days)


def generate_customer_segment():
    """Generate a customer segment."""

    return random.choices(
        CUSTOMER_SEGMENTS,
        weights=[35, 35, 22, 8],
        k=1
    )[0]


def generate_customer_metrics(segment):
    """Generate order count and spending based on customer segment."""

    if segment == "Basic":
        total_orders = random.randint(1, 5)
        total_spend = random.uniform(1000, 15000)

    elif segment == "Standard":
        total_orders = random.randint(4, 15)
        total_spend = random.uniform(15000, 50000)

    elif segment == "Premium":
        total_orders = random.randint(10, 30)
        total_spend = random.uniform(50000, 150000)

    else:  # VIP
        total_orders = random.randint(20, 60)
        total_spend = random.uniform(150000, 500000)

    return total_orders, round(total_spend, 2)


def generate_preferences():
    """Generate free-form customer preferences."""

    categories = random.sample(
        PRODUCT_CATEGORIES,
        k=random.randint(1, 3)
    )

    return (
        "Interested in "
        + ", ".join(categories)
        + "."
    )


def generate_feedback(sentiment):
    """Generate customer feedback matching the sentiment."""

    return random.choice(FEEDBACK_TEMPLATES[sentiment])


# ---------------------------------------------------------
# Structured Dataset Generation
# ---------------------------------------------------------

def generate_structured_customers():
    """Generate structured customer records."""

    customers = []

    for index in range(1, SAMPLE_RECORD_COUNT + 1):

        customer_id = generate_customer_id(index)

        first_name = random.choice(FIRST_NAMES)

        last_name = random.choice(LAST_NAMES)

        age = random.randint(18, 75)

        city = random.choice(CITIES)

        segment = generate_customer_segment()

        total_orders, total_spend = generate_customer_metrics(segment)

        signup_date = generate_signup_date()

        is_active = random.choice([True, True, True, False])

        customer = {
            "customer_id": customer_id,
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "email": generate_email(
                first_name,
                last_name,
                customer_id
            ),
            "city": city,
            "country": COUNTRY,
            "customer_segment": segment,
            "signup_date": signup_date.isoformat(),
            "total_orders": total_orders,
            "total_spend": total_spend,
            "is_active": is_active,
        }

        customers.append(customer)

    return customers


# ---------------------------------------------------------
# Unstructured Metadata Generation
# ---------------------------------------------------------

def generate_customer_metadata(customers):
    """Generate free-form metadata for each customer."""

    metadata_records = []

    for customer in customers:

        sentiment = random.choice(SENTIMENTS)

        metadata = {
            "customer_id": customer["customer_id"],
            "feedback": generate_feedback(sentiment),
            "support_notes": random.choice(
                SUPPORT_NOTE_TEMPLATES
            ),
            "preferences": generate_preferences(),
            "marketing_notes": random.choice(
                MARKETING_NOTE_TEMPLATES
            ),
            "sentiment": sentiment,
        }

        metadata_records.append(metadata)

    return metadata_records


# ---------------------------------------------------------
# Save Structured Dataset
# ---------------------------------------------------------

def save_customers_csv(customers):
    """Save structured customer records to CSV."""

    output_file = STRUCTURED_SOURCE_DIR / "customers.csv"

    fieldnames = list(customers[0].keys())

    with open(
        output_file,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(customers)

    print(f"Structured dataset saved: {output_file}")


# ---------------------------------------------------------
# Save Unstructured Metadata Dataset
# ---------------------------------------------------------

def save_metadata_json(metadata_records):
    """Save customer metadata records to JSON."""

    output_file = UNSTRUCTURED_SOURCE_DIR / "customer_metadata.json"

    with open(
        output_file,
        mode="w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata_records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Metadata dataset saved: {output_file}")


# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------

def main():

    # Ensure source directories exist
    STRUCTURED_SOURCE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    UNSTRUCTURED_SOURCE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 60)
    print("LOCAL DATA LAKEHOUSE - DATASET GENERATION")
    print("=" * 60)

    print("\nGenerating structured customer dataset...")

    customers = generate_structured_customers()

    print("Generating unstructured metadata dataset...")

    metadata_records = generate_customer_metadata(customers)

    print("\nSaving datasets...")

    save_customers_csv(customers)

    save_metadata_json(metadata_records)

    print("\n" + "=" * 60)
    print("DATASET GENERATION COMPLETED")
    print("=" * 60)

    print(f"Structured records generated: {len(customers)}")

    print(f"Metadata records generated: {len(metadata_records)}")

    print("\nSample customer:")

    print(json.dumps(
        customers[0],
        indent=4
    ))

    print("\nSample metadata:")

    print(json.dumps(
        metadata_records[0],
        indent=4
    ))


if __name__ == "__main__":
    main()