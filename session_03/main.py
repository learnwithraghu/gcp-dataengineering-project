import json
import random
import datetime
from faker import Faker
from google.cloud import pubsub_v1
from flask import Flask, render_template, request, flash, redirect, url_for

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for message flashing

# Initialize Faker for realistic data generation
fake = Faker()

# Initialize Google Cloud Pub/Sub Publisher
publisher = pubsub_v1.PublisherClient()

# Function to generate a sequence of timestamps for the order events
def generate_timestamps(start_date, num_records):
    time_stamps = [start_date]
    current = start_date
    for _ in range(num_records - 1):
        current += datetime.timedelta(seconds=random.randint(30, 300))
        time_stamps.append(current)
    return time_stamps

# Function to generate and publish messages
def publish_messages(topic_path, num_messages):
    for _ in range(num_messages):
        order_id = random.randint(1000, 9999)
        price = round(random.uniform(10.0, 500.0), 2)
        timestamp = fake.date_time_this_year().isoformat()
        data = json.dumps({
            'order_id': order_id,
            'price': price,
            'timestamp': timestamp
        }).encode('utf-8')
        
        # Publish a message
        try:
            publisher.publish(topic_path, data)
        except Exception as e:
            return False, str(e)
    
    return True, "Messages successfully published."

# Flask route for the main page with form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_records = int(request.form.get('num_records'))
        topic_name = request.form.get('topic_name')
        topic_path = f'projects/your_project_id/topics/{topic_name}'  # Replace with your project ID

        # Call the publish_messages function
        success, message = publish_messages(topic_path, num_records)

        # Flash a message based on success or failure
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
