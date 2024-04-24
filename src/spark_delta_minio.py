from minio import Minio
from pyspark.sql import SparkSession
from delta import *

builder = SparkSession.builder.appName("minio_app") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder, extra_packages=["org.apache.hadoop:hadoop-aws:3.3.4"]).getOrCreate()

# add confs
sc = spark.sparkContext
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "abdelbarre")
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "abdelbarre")
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://localhost:9000")
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")


client = Minio(
    "127.0.0.1:9000",
    access_key="tester",
    secret_key="tester123",
    secure=False
)

minio_bucket = "delta-demo"

found = client.bucket_exists(minio_bucket)
if not found:
    client.make_bucket(minio_bucket)

data_csv = './data/data.csv'
data_df = spark.read.format('csv').option('header', 'true').option('inferSchema', 'true').load(data_csv)

data_df \
    .write \
    .format("delta") \
    .partitionBy("school") \
    .mode("overwrite") \
    .save(f"s3a://{minio_bucket}/data-delta")