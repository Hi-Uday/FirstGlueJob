import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME','S3_INPUT_PATH','S3_OUTPUT_PATH','COLUMN_TO_DROP'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# read csv data from s3 using PySpark DataFrame
input_path = args['S3_INPUT_PATH']
output_path = args['S3_OUTPUT_PATH']
column_to_drop = args['COLUMN_TO_DROP']

# load the csv data into a PySpark DataFrame
data_frame = spark.read.option("header","true").csv(input_path)

# drop the specified column 
data_frame = data_frame.drop(column_to_drop)

# write the DataFrame to s3 in parquet format
data_frame.write.mode("overwrite").parquet(output_path)

job.commit()