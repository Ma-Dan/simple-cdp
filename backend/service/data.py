from flask import Blueprint, Flask, make_response, render_template, request
from flask_cors import cross_origin
import json
import requests

import jaydebeapi
from hdfs import InsecureClient

# Set JDBC driver path and connection URL
driver = "org.apache.kyuubi.jdbc.KyuubiHiveDriver"
url = "jdbc:kyuubi://127.0.0.1:10009/cdp_demo"
jdbc_driver_path = ["/home/ubuntu/spark/kyuubi-hive-jdbc-shaded-1.9.0.jar", "/home/ubuntu/spark/slf4j-api-2.0.13.jar"]

# 认证服务
from utils.bcrypt import hash_pwd, compare_pwd
from utils.http import parse_request, _http_response, success, param_err, auth_err, server_err
from components.authenticate import auth, generate_token, verify_token

data_api = Blueprint('data_api', __name__)

@data_api.route('/api/query', methods=['POST'])
@cross_origin(supports_credentials=True)
@auth.login_required
def query():
    print(request.json)
    database = request.json["database"]
    sql = request.json["sql"]

    url = "jdbc:kyuubi://127.0.0.1:10009/{}".format(database)

    # Connect to the database using JayDeBeApi
    conn = jaydebeapi.connect(driver, url, ["jupyter", ""], jdbc_driver_path)

    # Create a cursor object
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute(sql)

    # Retrieve query results
    result_set = cursor.fetchall()

    # Process the results
    rows = []
    for row in result_set:
        rows.append(row)

    # Close the cursor and the connection
    cursor.close()

    conn.close()

    return json.dumps({
          'status': True,
          'message': '查询成功',
          'result': {
            'rows': rows,
          }
        }, ensure_ascii=False).encode('utf8')

@data_api.route('/api/get_job', methods=['GET'])
@cross_origin(supports_credentials=True)
@auth.login_required
def get_job():
    job_name = request.args.get("job_name")

    client = InsecureClient("http://localhost:9870", "jupyter")
    hdfs_path = "/user/jupyter/spark_job_files/{}.py".format(job_name)
    content = ""
    with client.read(hdfs_path) as f:
        content = f.data.decode('utf-8')

    return json.dumps({
          'status': True,
          'message': '读取成功',
          'result': {
            'hdfs_path': hdfs_path,
            'content': content
          }
        }, ensure_ascii=False).encode('utf8')

@data_api.route('/api/upload_job', methods=['POST'])
@cross_origin(supports_credentials=True)
@auth.login_required
def upload_job():
    print(request.json)
    job_name = request.json["job_name"]
    job_script = request.json['job_script']

    client = InsecureClient("http://localhost:9870", "jupyter")
    hdfs_path = "/user/jupyter/spark_job_files/{}.py".format(job_name)
    client.write(hdfs_path=hdfs_path, overwrite=True, data=job_script.encode('utf-8'))

    return json.dumps({
          'status': True,
          'message': '上传成功',
          'result': {
            'hdfs_path': hdfs_path,
          }
        }, ensure_ascii=False).encode('utf8')

@data_api.route('/api/submit_job', methods=['POST'])
@cross_origin(supports_credentials=True)
@auth.login_required
def submit_job():
    job_name = request.json["job_name"]

    hdfs_resource = "hdfs://master/user/jupyter/spark_job_files/{}.py".format(job_name)

    job_data = {
        "batchType": "Spark",
        "resource": hdfs_resource,
        "name": job_name,
        "conf": {
            "hive.server2.proxy.user": "jupyter",
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        },
        "className": "org.apache.spark.deploy.PythonRunner"
    }
    headers = {
        'Content-Type': 'application/json'
    }

    resp = requests.request("POST", "http://localhost:10099/api/v1/batches", headers=headers, data=json.dumps(job_data), verify=False)
    result = json.loads(resp.text)

    return json.dumps({
          'status': True,
          'message': '提交成功',
          'result': result,
        }, ensure_ascii=False).encode('utf8')

@data_api.route('/api/get_job_status', methods=['POST'])
@cross_origin(supports_credentials=True)
@auth.login_required
def get_job_status():
    print(request.json)
    job_id = request.json["job_id"]

    headers = {
        'Content-Type': 'application/json'
    }

    resp = requests.request("GET", "http://localhost:10099/api/v1/batches/{}".format(job_id), headers=headers, verify=False)
    result = json.loads(resp.text)

    return json.dumps({
          'status': True,
          'message': '读取成功',
          'result': result,
        }, ensure_ascii=False).encode('utf8')