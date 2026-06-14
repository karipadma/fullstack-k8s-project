from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_master_conn

app = Flask(__name__)
CORS(app)


@app.route("/api/employees", methods=["GET"])
def get_employees():

    try:
        conn = get_master_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees")
        data = cursor.fetchall()

        conn.close()

        return jsonify({
            "source": "db-master",
            "data": data
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/employees", methods=["POST"])
def add_employee():

    try:
        data = request.json

        conn = get_master_conn()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO employees (name, role) VALUES (%s, %s)",
            (data["name"], data["role"])
        )

        conn.commit()
        conn.close()

        return jsonify({
            "msg": "inserted"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/")
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
