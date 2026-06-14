from flask import Flask, request, jsonify
from db import get_master_conn, get_replica_conn
import redis, json
from config import Config

app = Flask(__name__)

cache = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True
)

CACHE_KEY = "employees"

@app.route("/api/employees", methods=["GET"])
def get_employees():

    cached = cache.get(CACHE_KEY)
    if cached:
        return jsonify({"source": "redis", "data": json.loads(cached)})

    conn = get_replica_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    conn.close()

    cache.set(CACHE_KEY, json.dumps(data), ex=60)

    return jsonify({"source": "db-replica", "data": data})


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