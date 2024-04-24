from minio import Minio

client = Minio(
    "127.0.0.1:9000",
    access_key="tester",
    secret_key="tester123",
    secure=False
)

minio_bucket = "my-first-bucket"

found = client.bucket_exists(minio_bucket)
if not found:
    client.make_bucket(minio_bucket)

destination_file = 'data.txt'
source_file = './data/data.txt' ## The file should exist in the project folder

client.fput_object(minio_bucket, destination_file, source_file,)