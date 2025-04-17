import sys
import yaml
import json
import boto3
import os
from datetime import datetime

# Get environment name (dev/test/prod) and bucket from environment variables or passed arguments
env_name = sys.argv[1] if len(sys.argv) > 1 else 'dev'
s3_bucket = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('S3_BUCKET')

if not s3_bucket:
    raise ValueError("❌ S3 bucket name not provided or found in environment variables")

# Load the YAML file
yaml_file = 'env.yaml'
with open(yaml_file, 'r') as file:
    all_data = yaml.safe_load(file)

# Ensure the environment exists in the YAML
if env_name not in all_data:
    raise ValueError(f"❌ Environment '{env_name}' not found in {yaml_file}")

# Extract values
env_data = all_data[env_name]
total = sum(env_data.values())

# Prepare result
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
result = {
    'timestamp': timestamp,
    'environment': env_name,
    'values': env_data,
    'sum': total
}

# Save to a local JSON file
filename = f'result-{env_name}-{timestamp}.json'
with open(filename, 'w') as f:
    json.dump(result, f, indent=2)

# Upload to S3
s3 = boto3.client('s3')
s3.upload_file(filename, s3_bucket, f'{env_name}/{filename}')
print(f'✅ Uploaded to s3://{s3_bucket}/{env_name}/{filename}')
