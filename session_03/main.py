import base64
import json
import io
from fastavro import reader
from google.cloud import storage

def read_avro_from_gcp(bucket_name):
    # Initialize the GCP storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Iterate over all blobs (files) in the bucket
    all_json_data = []
    for blob in bucket.list_blobs():
        # Download the blob into an in-memory file
        avro_file = io.BytesIO()
        blob.download_to_file(avro_file)
        avro_file.seek(0)

        # Read the Avro file
        avro_reader = reader(avro_file)
        for record in avro_reader:
            # Process each record to handle bytes and convert to JSON
            processed_record = process_record(record)
            all_json_data.append(processed_record)

    return json.dumps(all_json_data, indent=4)  # Serialize the entire data structure to JSON

def process_record(record):
    """ Process each record to handle bytes and convert to JSON """
    for key, value in record.items():
        if isinstance(value, bytes):
            # Decode bytes to string
            record[key] = value.decode('utf-8', errors='ignore')
        elif isinstance(value, dict):
            # Recursively process nested dictionaries
            record[key] = process_record(value)
    return record

# Replace 'your-bucket-name' with your bucket name
bucket_name = 'order-events-dataengineering'

# Get the data
json_data = read_avro_from_gcp(bucket_name)
print(json_data)
