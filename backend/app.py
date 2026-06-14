from flask import Flask, request, jsonify
from db import get_master_conn, get_replica_conn
import redis, json
from config import Config

app = Flask(__name__)

# existing code ...

@app.route("/api/employees", methods=["POST"])
def add_employee():
    data = request.json

    conn = get_master_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, role) VALUES (%s,%s)",
        (data["name"], data["role"])
    )
    conn.commit()
    conn.close()

    cache.delete(CACHE_KEY)

    return jsonify({"msg": "inserted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)": "inserted"})
