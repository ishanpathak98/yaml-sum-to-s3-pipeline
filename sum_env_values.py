import yaml
import boto3
import sys
import datetime

# Load the YAML file
def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"❌ Error loading YAML file: {e}")
        sys.exit(1)

# Calculate the sum of underscore-separated values
def calculate_sum(env_string):
    try:
        return sum(int(i) for i in env_string.strip().split('_'))
    except Exception as e:
        print(f"❌ Error parsing environment string: {e}")
        sys.exit(1)

# Upload result to S3
def upload_to_s3(bucket_name, region, filename, content):
    try:
        s3 = boto3.client('s3', region_name=region)
        s3.put_object(Bucket=bucket_name, Key=filename, Body=content)
        print(f"✅ Result uploaded to S3: s3://{bucket_name}/{filename}")
    except Exception as e:
        print(f"❌ Failed to upload to S3: {e}")
        sys.exit(1)

# Main function
def main():
    yaml_file = "env_config.yaml"  # Ensure this file is present in same directory
    bucket_name = "my-yaml-sum-bucket"
    region = "us-east-2"

    # Load YAML data
    yaml_data = load_yaml(yaml_file)
    result = {}

    # Compute sum for each environment
    for env, value in yaml_data.items():
        result[env] = calculate_sum(value)

    # Create output string
    output = "\n".join([f"{k}: {v}" for k, v in result.items()])
    print("📦 Computed sums:\n" + output)

    # Generate unique filename using timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"env_sums_{timestamp}.txt"

    # Upload to S3
    upload_to_s3(bucket_name=bucket_name, region=region, filename=filename, content=output)

if __name__ == "__main__":
    main()
