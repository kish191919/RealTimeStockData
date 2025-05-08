
# stock_spark_process_stream.py
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

# 5. PostgreSQL로 저장 (Trigger마다 실행)
def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/stockdb") \
        .option("dbtable", "stock_price") \
        .option("user", "stock") \
        .option("password", "stock123") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# 6. 트리거 실행
query = parsed_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

query.awaitTermination()
