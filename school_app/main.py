import os
import json
from decimal import Decimal
from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error
import redis

app = FastAPI()

db_config = {
    "host": os.getenv("DB_HOST", ""),
    "user": os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", ""),
}

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", ""),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", ""),
    decode_responses=True,
)


def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    return obj

@app.get("/employee/{name}")
def get_employee(name: str):
    # Try cache first
    cached = redis_client.get(name)
    if cached:
        return {"employee": json.loads(cached), "source": "redis"}

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM employees WHERE name = %s", (name,))
        result = cursor.fetchone()

        if result:
            result = convert_decimal(result)

            # Cache the result for 60 seconds
            redis_client.setex(name, 60, json.dumps(result))

            return {"employee": result, "source": "mysql"}

        return {"message": f"No employee found with name '{name}'"}

    except Error as e:
        return {"error": str(e)}

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}




