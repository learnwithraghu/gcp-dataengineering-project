import json
import random
import datetime
from faker import Faker
from google.cloud import pubsub_v1

# Initialize Faker for realistic data generation
fake = Faker()

# Initialize Google Cloud Pub/Sub Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/kodekloud-gcp-training/topics/order_events'  # Replace with your project and topic

# Function to generate a sequence of timestamps for the order events
def generate_timestamps(start_date):
    time_stamps = [start_date]
    current_time = start_date
    for _ in range(4):  # For the other 4 events
        time_added = datetime.timedelta(hours=random.randint(1, 5))
        current_time += time_added
        time_stamps.append(current_time)
    return time_stamps

# Function to generate a random order value in USD
def random_order_value():
    return round(random.uniform(10.0, 500.0), 2)

# Function to generate random product categories
def random_product_categories(num_categories=7):
    possible_categories = ["Food", "Cosmetics", "Electronics", "Clothing", "Home Appliances", "Books", "Toys"]
    return random.sample(possible_categories, num_categories)

# Function to generate random phone models
def random_phone_model():
    phone_models = ["iPhone 12", "Samsung Galaxy S21", "Google Pixel 5", "OnePlus 9", "Huawei P30"]
    return random.choice(phone_models)

# Function to generate random coordinates in New York
def random_coordinates():
    lat = random.uniform(40.477399, 40.917577)
    long = random.uniform(-74.259090, -73.700272)
    return {"latitude": lat, "longitude": long}

# Function to publish message to Pub/Sub
def publish_to_pubsub(message):
    data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, data)
    return future.result()

# Generate and publish data for 10 orders
for _ in range(10):
    start_date = fake.date_time_between(start_date="-2y", end_date="now")
    timestamps = generate_timestamps(start_date)
    event_statuses = ["Order placed", "Order prepared", "Order dispatched", "Order delivered", "Order rated"]

    events = [{"status": status, "timestamp": timestamp.strftime("%d/%m/%Y %H:%M:%S")} for status, timestamp in zip(event_statuses, timestamps)]

    order_data = {
        "date": start_date.strftime("%d/%m/%Y"),
        "order_number": fake.unique.bothify(text='Order-####'),
        "events": events,
        "order_value": random_order_value(),
        "product_category": random_product_categories(),
        "dispatcher_id": fake.unique.numerify(text='Dispatcher-###'),
        "phone_user": random_phone_model(),
        "location": random_coordinates()
    }

    # Publish each order to Pub/Sub
    publish_to_pubsub(order_data)

print('Order data generated and published to Pub/Sub.')
