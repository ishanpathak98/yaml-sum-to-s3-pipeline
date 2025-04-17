import yaml
import boto3
import sys
import datetime

def load_yaml(file_path):
    """Load YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def calculate_sum(env_string):
    """Calculate the sum of numbers in a string like '1_2_3_4'."""
    return sum(int(i) for i in env_string.strip().split('_'))

def upload_to_s3(bucket_name, region, filename, content):
    """Upload result to S3."""
    s3 = boto3.client('s3', region_name=region)
    s3.put_object(Bucket=bucket_name, Key=filename, Body=content)
    print(f"✅ Result uploaded to S3: s3://{bucket_name}/{filename}")

def main():
    yaml_file = "env_config.yaml"
    bucket_name = "my-yaml-sum-bucket"  # Use the bucket name as per your setup
    region = "us-east-2"  # Use the region as per your setup

    # Load the YAML data
    yaml_data = load_yaml(yaml_file)

    # Get environment argument from command-line or default to 'All'
    env_arg = sys.argv[1] if len(sys.argv) > 1 else "All"

    result = {}
    if env_arg == "All":
        for env, val in yaml_data.items():
            result[env] = calculate_sum(val)
    elif env_arg in yaml_data:
        result[env_arg] = calculate_sum(yaml_data[env_arg])
    else:
        print(f"❌ Environment '{env_arg}' not found in YAML.")
        sys.exit(1)

    output = "\n".join([f"{k}: {v}" for k, v in result.items()])
    print("📦 Computed sums:\n" + output)

    # Create a filename with timestamp for uniqueness
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"env_sums_{env_arg}_{timestamp}.txt"

    # Upload result to S3
    upload_to_s3(bucket_name, region, filename, output)

if __name__ == "__main__":
    main()
