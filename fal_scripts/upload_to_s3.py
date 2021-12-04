import os
import boto3

s3_client = boto3.client('s3')

bucket_name = "fal-example-dbt-artifacts-bucket"
manifest_source_file_name = os.path.join(context.config.target_path, "manifest.json")
run_results_source_file_name = os.path.join(context.config.target_path, "run_results.json")
manifest_destination_blob_name = "manifest.json"
run_results_destination_blob_name = "run_results.json"


s3_client.upload_file(manifest_source_file_name, bucket_name, manifest_destination_blob_name)
s3_client.upload_file(run_results_source_file_name, bucket_name, run_results_destination_blob_name)
