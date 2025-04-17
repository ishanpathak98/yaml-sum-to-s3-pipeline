import yaml
import boto3
import os

def calculate_sums(data):
    results = {}
    for env, val in data['environments'].items():
        nums = map(int, val.split("_"))
        results[env] = sum(nums)
    return results

def write_to_file(results, file_name="result.txt"):
    with open(file_name, "w") as f:
        for k, v in results.items():
            f.write(f"{k} sum: {v}\n")

def upload_to_s3(file_name, bucket_name, object_name):
    s3 = boto3.client("s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION")
    )
    s3.upload_file(file_name, bucket_name, object_name)

if __name__ == "__main__":
    with open("env.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)

    results = calculate_sums(yaml_data)
    write_to_file(results)
    upload_to_s3("result.txt", os.getenv("S3_BUCKET_NAME"), "result.txt")
