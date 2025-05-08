
# stock_process_stream.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType, TimestampType

# 1. Spark 세션 생성
spark = SparkSession.builder \
    .appName("StockStreamProcessor") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Kafka에서 메시지 읽기
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "stocks") \
    .load()

# 3. JSON 파싱 스키마 정의
schema = StructType() \
    .add("symbol", StringType()) \
    .add("timestamp", StringType()) \
    .add("open", FloatType()) \
    .add("high", FloatType()) \
    .add("low", FloatType()) \
    .add("close", FloatType()) \
    .add("volume", FloatType())

# 4. JSON 메시지 디코딩
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")


# 콘솔에 출력
query = df_parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
