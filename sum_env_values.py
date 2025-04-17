import yaml
import boto3
import sys

# Get the environment name and bucket name from the arguments
if len(sys.argv) != 3:
    raise ValueError("❌ Missing required arguments. Usage: python sum_env_values.py <env_name> <s3_bucket_name>")

env_name = sys.argv[1]
s3_bucket = sys.argv[2]
yaml_file = 'env.yaml'  # Ensure the YAML file is in the same directory as this script

# Load the YAML file
with open(yaml_file, 'r') as file:
    data = yaml.safe_load(file)

# Debugging: print the loaded YAML content
print("Loaded YAML content:")
print(data)

# Ensure the 'env' key exists in the YAML
if 'env' not in data:
    raise ValueError(f"❌ The 'env' section is missing in {yaml_file}")

# Check if the requested environment exists under 'env'
if env_name not in data['env']:
    raise ValueError(f"❌ Environment '{env_name}' not found in {yaml_file}")

# Get the environment value
env_value = data['env'][env_name]
print(f"Environment '{env_name}' found with value: {env_value}")

# Upload the environment value to S3
s3 = boto3.client('s3')

filename = f'{env_name}_value.txt'
with open(filename, 'w') as file:
    file.write(f"Environment: {env_name}\nValue: {env_value}\n")

# Upload the file to the specified S3 bucket
try:
    print(f"Uploading '{filename}' to S3 bucket '{s3_bucket}'...")
    s3.upload_file(filename, s3_bucket, f'{env_name}/{filename}')
    print(f"✅ File uploaded successfully to S3 bucket '{s3_bucket}'")
except Exception as e:
    print(f"❌ Failed to upload file to S3: {str(e)}")
