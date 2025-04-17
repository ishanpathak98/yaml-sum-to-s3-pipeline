#!/usr/bin/env python3
import os
import yaml
import boto3
import json
from datetime import datetime

def load_config():
    """Load configuration from YAML file"""
    if os.path.exists('config.yaml'):
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    return {}

def process_data(config):
    """Process data according to config"""
    # Example data processing
    numbers = config.get('numbers', [1, 2, 3, 4, 5])
    total_sum = sum(numbers)
    
    result = {
        'sum': total_sum,
        'count': len(numbers),
        'average': total_sum / len(numbers) if numbers else 0,
        'environment': os.environ.get('ENVIRONMENT', 'dev'),
        'timestamp': datetime.now().isoformat()
    }
    
    return result

def save_to_s3(data, bucket_name=None, prefix=None):
    """Save data to S3 bucket"""
    # Use environment variable or parameter
    bucket = bucket_name or os.environ.get('S3_BUCKET')
    env = os.environ.get('ENVIRONMENT', 'dev')
    
    if not bucket:
        print("No S3 bucket specified. Saving locally instead.")
        os.makedirs('output', exist_ok=True)
        with open('output/result.json', 'w') as f:
            json.dump(data, f, indent=2)
        return
    
    # Create S3 client
    s3 = boto3.client('s3')
    
    # Convert data to JSON
    json_data = json.dumps(data, indent=2)
    
    # Define S3 key with environment prefix
    key = f"{env}/result-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    if prefix:
        key = f"{prefix}/{key}"
    
    # Upload to S3
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json_data,
        ContentType='application/json'
    )
    
    print(f"Data uploaded to s3://{bucket}/{key}")

def main():
    # Load configuration
    config = load_config()
    
    # Process data
    result = process_data(config)
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Save locally
    with open('output/result.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    # Save to S3 if bucket is specified
    bucket_name = os.environ.get('S3_BUCKET')
    if bucket_name:
        save_to_s3(result, bucket_name)

if __name__ == "__main__":
    main()
