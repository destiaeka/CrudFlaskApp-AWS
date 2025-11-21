from flask import Flask, request, render_template, redirect
import pymysql
import boto3
import os

app = Flask(__name__)

# RDS Connection
db = pymysql.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"]
)

# S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    aws_session_token=os.environ.get("AWS_SESSION_TOKEN")
)
BUCKET = os.environ["S3_BUCKET"]

@app.route("/")
def index():
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email, file_url FROM users")
    rows = cursor.fetchall()
    return render_template("index.html", data=rows)

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    email = request.form["email"]
    file = request.files.get("file")

    file_url = None
    if file:
        filename = f"uploads/{name}_{file.filename}"
        s3.upload_fileobj(file, BUCKET, filename)
        file_url = f"https://{BUCKET}.s3.amazonaws.com/{filename}"

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, file_url) VALUES (%s, %s, %s)",
        (name, email, file_url)
    )
    db.commit()

    return redirect("/")

@app.route("/delete/<id>")
def delete(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    db.commit()
    return redirect("/")

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
