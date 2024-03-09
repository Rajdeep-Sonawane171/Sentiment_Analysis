# First Initialize The SparkSession
from pyspark.sql import SparkSession

# Then import the required module
from pyspark.sql.types import StructType, StructField, StringType,IntegerType

# Start The SparkSession And create The Application
spark=SparkSession.builder.appName("CustomerReviewSentimentAnalysis").getOrCreate()

# Set The Schema For The Json Data
schema = StructType([
    StructField("ItemID", IntegerType()),
    StructField("Sentiment", IntegerType()),
    StructField("SentimentSource", StringType()),
    StructField("SentimentText", StringType())
])

# Create The CustomerRevivedf And Upload The Json Data From The S3 Bucket
CustomerRevivedf = spark.read.schema(schema).option("mode", "PERMISSIVE").json("s3://myprojectemr/myinputfolder/tweets.json")

# Print The Schema Of CustomerRevivedf
CustomerRevivedf.printSchema()

# Show the CustomerRevivedf DataFrame
CustomerRevivedf.show()

# Write The CustomerRevivedf Into Parquet Format In HDFS File
CustomerRevivedf.write.mode("overwrite").parquet("hdfs://ip-10-0-11-178/outputdata/")

# At last Stop The Spark Job
spark.stop()