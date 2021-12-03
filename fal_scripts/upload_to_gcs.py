import os
from google.cloud import storage

bucket_name = "fal_example_dbt_artifacts_bucket"
destination_blob_name = "manifest.json"
source_file_name = os.path.join(context.config.target_path, "manifest.json")

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file_name)
