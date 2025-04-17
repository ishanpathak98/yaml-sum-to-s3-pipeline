import yaml
import boto3
import os
from datetime import datetime

# Get environment name (dev/test/prod) and bucket from environment variables
env_name = os.environ.get('ENV_NAME', 'dev')
s3_bucket = os.environ.get('S3_BUCKET')

# Load the YAML file
yaml_file = 'env.yaml'
with open(yaml_file, 'r') as file:
    all_data = yaml.safe_load(file)

# Ensure the environment exists in the YAML
if env_name not in all_data['env']:
    raise ValueError(f"❌ Environment '{env_name}' not found in {yaml_file}")

# Extract values
env_data = all_data['env'][env_name]
# Split the string into individual numbers, convert to integers and sum them
values = list(map(int, env_data.split('_')))
total = sum(values)

# Prepare result
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
result = f"Timestamp: {timestamp}\n" \
         f"Environment: {env_name}\n" \
         f"Values: {env_data}\n" \
         f"Sum: {total}\n"

# Save to a local .txt file
filename = f'result-{env_name}-{timestamp}.txt'
with open(filename, 'w') as f:
    f.write(result)

# Upload to S3
s3 = boto3.client('s3')
s3.upload_file(filename, s3_bucket, f'{env_name}/{filename}')
print(f'✅ Uploaded to s3://{s3_bucket}/{env_name}/{filename}')
