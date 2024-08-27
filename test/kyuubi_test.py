import jaydebeapi

# Set JDBC driver path and connection URL
driver = "org.apache.kyuubi.jdbc.KyuubiHiveDriver"
url = "jdbc:kyuubi://127.0.0.1:10009/default"
jdbc_driver_path = ["/home/ubuntu/spark/kyuubi-hive-jdbc-shaded-1.9.0.jar", "/home/ubuntu/spark/slf4j-api-2.0.13.jar"]

# Connect to the database using JayDeBeApi
conn = jaydebeapi.connect(driver, url, ["jupyter", ""], jdbc_driver_path)

# Create a cursor object
cursor = conn.cursor()

# Execute the SQL query
cursor.execute("SELECT * FROM test_table LIMIT 10")

# Retrieve query results
result_set = cursor.fetchall()

# Process the results
for row in result_set:
    print(row)

# Close the cursor and the connection
cursor.close()
conn.close()