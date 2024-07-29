import boto3
import sys
import pandas as pd
from io import StringIO
from pyspark.context import SparkContext

# from awsglue.transforms import *
from awsglue.context import GlueContext
from awsglue.job import Job

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Initialize a session using the IAM role attached to the Glue job
session = boto3.Session()

# Use the S3 client
glue_client = boto3.client("glue")
s3_client   = boto3.client('s3')
secrets_client = boto3.client("secretsmanager")

# Specify the S3 bucket and file key
bucket_name = 'redshift-dl-test-data-landing-316328384763-us-east-1' 
file_key = 'ache_raw_data_test.csv'

# Get the file object
csv_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')

# Use StringIO to make the string look like a file object
csv_file = StringIO(csv_string)

# Read it into a pandas DataFrame
df = pd.read_csv(csv_file)

print(df.head())

job.commit()
