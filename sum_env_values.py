import yaml
import boto3
import sys

# Check command-line arguments
if len(sys.argv) != 3:
    raise ValueError("❌ Usage: python sum_env_values.py <env_name> <s3_bucket_name>")

env_name = sys.argv[1]
s3_bucket = sys.argv[2]
yaml_file = 'env.yaml'

# Load the YAML file
with open(yaml_file, 'r') as file:
    data = yaml.safe_load(file)

# Validate structure
if 'env' not in data:
    raise ValueError(f"❌ Missing 'env' section in {yaml_file}")

if env_name not in data['env']:
    raise ValueError(f"❌ Environment '{env_name}' not found in {yaml_file}")

# Extract and process the value
env_value = data['env'][env_name]
try:
    number_list = list(map(int, env_value.split('_')))
    total_sum = sum(number_list)
except Exception as e:
    raise ValueError(f"❌ Failed to calculate sum: {str(e)}")

# Create output file
filename = f'{env_name}_sum.txt'
with open(filename, 'w') as file:
    file.write(f"Sum for environment '{env_name}': {total_sum}\n")

# Upload to S3
s3 = boto3.client('s3')
try:
    print(f"Uploading '{filename}' to S3 bucket '{s3_bucket}'...")
    s3.upload_file(filename, s3_bucket, f'{env_name}/{filename}')
    print(f"✅ Uploaded successfully to 's3://{s3_bucket}/{env_name}/{filename}'")
except Exception as e:
    print(f"❌ Failed to upload to S3: {str(e)}")
