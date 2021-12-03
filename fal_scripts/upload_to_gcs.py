import os
from google.cloud import storage

bucket_name = "fal_example_dbt_artifacts_bucket"
manifest_destination_blob_name = "manifest.json"
run_results_destination_blob_name = "run_results.json"

manifest_source_file_name = os.path.join(context.config.target_path, "manifest.json")
run_results_source_file_name = os.path.join(context.config.target_path, "run_results.json")

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
manifest_blob = bucket.blob(manifest_destination_blob_name)
run_results_blob = bucket.blob(run_results_destination_blob_name)

manifest_blob.upload_from_filename(manifest_source_file_name)
run_results_blob.upload_from_filename(run_results_source_file_name)
