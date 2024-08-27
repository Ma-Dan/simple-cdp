from pyspark.sql import SparkSession

if __name__ == "__main__":
    # 创建Spark会话
    spark1 = SparkSession.builder \
        .appName("Spark Test") \
        .enableHiveSupport() \
        .getOrCreate()

    spark1.sql("use cdp")

    # 创建Hive表
    spark1.sql("insert overwrite table tag_customer_young select id, (CASE WHEN birthday > unix_timestamp(date('1985-01-01')) THEN 'Y' ELSE 'N' END) as young from customer;")

    # 停止Spark会话
    spark1.stop()