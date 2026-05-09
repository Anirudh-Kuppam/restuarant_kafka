from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import os
os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["spark.hadoop.io.native.lib.available"] = "false"

spark = SparkSession.builder \
    .appName("KafkaAnalysis") \
    .master("local[*]") \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
    .config("spark.sql.streaming.checkpointLocation", "file:///C:/tmp/checkpoint") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

spark.conf.set(
    "spark.hadoop.fs.file.impl",
    "org.apache.hadoop.fs.LocalFileSystem"
)

schema = StructType() \
    .add("item", StringType()) \
    .add("price", IntegerType()) \
    .add("quantity", IntegerType())

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "orders") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

result = json_df.withColumn("revenue", col("price") * col("quantity")) \
    .groupBy("item") \
    .agg(sum("revenue").alias("total_revenue"))

query = result.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .option("checkpointLocation", "file:///C:/tmp/checkpoint") \
    .start()

query.awaitTermination()