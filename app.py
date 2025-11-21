from flask import Flask, request, jsonify
import pymysql
import boto3
from config import Config

app = Flask(__name__)

# Database connection
def get_db_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASS,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
)

# Routes
@app.route("/")
def index():
    return "Hello, Flask AWS App!"

@app.route("/items", methods=["GET"])
def get_items():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM items;")
        result = cursor.fetchall()
    conn.close()
    return jsonify(result)

@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    name = data.get("name")
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO items (name) VALUES (%s);", (name,))
        conn.commit()
    conn.close()
    return jsonify({"message": "Item created"}), 201

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    s3_client.upload_fileobj(file, Config.S3_BUCKET, file.filename)
    return jsonify({"message": f"{file.filename} uploaded to S3"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.FLASK_PORT)
