from flask import Flask, request, jsonify
import boto3
from datetime import datetime
import os

app = Flask(__name__)

# ---- AWS CONFIG ----
BUCKET_NAME = "mini-siem-raw-logs-lakshman"
S3_PREFIX = "raw-logs/auth/"

s3 = boto3.client("s3", region_name="us-east-1")

# ---- Dummy User Validation ----
def validate_user(username, password):
    # Simple hardcoded logic for demo
    if username == "admin" and password == "admin123":
        return True
    return False


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    ip_address = request.remote_addr
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if validate_user(username, password):
        status = "LOGIN_SUCCESS"
    else:
        status = "LOGIN_FAILED"

    # Create log entry
    log_entry = f"{timestamp} | {status} | USER:{username} | IP:{ip_address}\n"

    try:
        file_name = f"{S3_PREFIX}login_logs_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=log_entry
        )

        return jsonify({"message": status}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)