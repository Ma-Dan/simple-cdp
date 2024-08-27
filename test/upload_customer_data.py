import jaydebeapi

# Set JDBC driver path and connection URL
driver = "org.apache.kyuubi.jdbc.KyuubiHiveDriver"
url = "jdbc:kyuubi://127.0.0.1:10009/cdp_demo"
jdbc_driver_path = ["/home/ubuntu/spark/kyuubi-hive-jdbc-shaded-1.9.0.jar", "/home/ubuntu/spark/slf4j-api-2.0.13.jar"]

import pandas as pd

df = pd.read_csv('./customer.csv')

# Connect to the database using JayDeBeApi
conn = jaydebeapi.connect(driver, url, ["jupyter", ""], jdbc_driver_path)

cursor = conn.cursor()
for row in df.iterrows():
    sql = "INSERT INTO customer VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(row[1][0], row[1][1], row[1][2], row[1][3], row[1][4], row[1][5], row[1][6])
    print(sql)
    cursor.execute(sql)

cursor.close()
conn.close()