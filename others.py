
## MYSQL CONNECT

# import os
# import mysql.connector
# from mysql.connector import Error

# from dotenv import load_dotenv
# load_dotenv()

# db_config = {
#     "host": os.getenv("DB_HOST", ""),
#     "user": os.getenv("DB_USER", ""),
#     "password": os.getenv("DB_PASSWORD", ""),
#     "database": os.getenv("DB_NAME", ""),
# }

# connection = mysql.connector.connect(**db_config)
# cursor = connection.cursor(dictionary=True)
# name = "Alice"
# cursor.execute("SELECT * FROM employees WHERE name = %s", (name,))
# result = cursor.fetchone()
# print(result)



## REDIS CONNECT

# import redis
# import os
# from dotenv import load_dotenv
# load_dotenv()

# # redis_client = redis.Redis(host="65.0.68.115", port=6379, password="Redis@123", db=0)
# redis_client = redis.Redis(
#     host=os.getenv("REDIS_HOST", ""),
#     port=int(os.getenv("REDIS_PORT", 6379)),
#     password=os.getenv("REDIS_PASSWORD", ""),
#     decode_responses=True,
# )

# # Set a simple key-value pair
# redis_client.set("my_key", "Hello Redis")
# # Set a key with an expiration time (in seconds)
# redis_client.set("temp_key", "Temporary", ex=60)  # expires after 60 seconds
# # Get the value of a key
# value = redis_client.get("my_key")
# # Redis returns bytes, so decode it
# if value:
#     value = value.decode("utf-8")
# print(value)  # Output: Hello RedisSet a simple key-value pair
# redis_client.set("my_key", "Hello Redis")
# # Set a key with an expiration time (in seconds)
# redis_client.set("temp_key", "Temporary", ex=60)  # expires after 60 seconds


###  LOKI ERROR

# import logging
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# from logging_loki import LokiHandler
# from pythonjsonlogger import jsonlogger

# # -------------------------
# # Logger setup
# # -------------------------
# def get_logger():
#     #handler = LokiHandler(
#     #    url="http://localhost:3100/loki/api/v1/push",
#     #    tags={"app": "fastapi"},
#     #    version="1",
#     #)

#     handler = LokiHandler(
#         url="http://loki:3100/loki/api/v1/push",  # Use service name 'loki'
#         tags={"app": "fastapi"},
#         version="1",
#     )


#     formatter = jsonlogger.JsonFormatter(
#         '%(asctime)s %(levelname)s %(name)s %(message)s %(path)s %(method)s'
#     )
#     handler.setFormatter(formatter)

#     logger = logging.getLogger("fastapi")
#     logger.setLevel(logging.ERROR)
#     logger.addHandler(handler)
#     return logger

# logger = get_logger()

# # -------------------------
# # FastAPI app
# # -------------------------
# app = FastAPI()

# # Middleware to catch and log all unhandled exceptions
# @app.middleware("http")
# async def catch_exceptions_middleware(request: Request, call_next):
#     try:
#         return await call_next(request)
#     except Exception as e:
#         # Structured logging of unexpected errors
#         logger.error(
#             f"Unhandled exception: {e}",
#             extra={
#                 "path": request.url.path,
#                 "method": request.method
#             }
#         )
#         return JSONResponse(
#             status_code=500,
#             content={"detail": "Internal Server Error"}
#         )

# # -------------------------
# # Example route that triggers middleware logging
# # -------------------------
# @app.get("/new_error")
# def new_cause_error():
#     1 / 0  # This will trigger middleware logging automatically
#     return {"message": "This won't be reached"}

# # -------------------------
# # Example route with manual logger.error
# # -------------------------
# @app.get("/error")
# def manual_error():
#     gh = False
#     if not gh:
#         logger.error(
#             "Manual error: gh not provided",
#             extra={
#                 "path": "/error",
#                 "method": "GET"
#             }
#         )
#     return {"Success": f"Working fine {gh}"}


# # ---------------- Example Usage ----------------
# data = {"new": "value"}

# # Encrypt dictionary → Base64 string
# encrypted_b64 = encrypt_json(data, key, iv)
# print("Encrypted (send to client):", encrypted_b64)

# # Decrypt Base64 string → Python dictionary
# decrypted_data = decrypt_json(encrypted_b64, key, iv)
# print("Decrypted JSON:", decrypted_data)

###  Final middleware stack diagram. ###

# Incoming request
#       │
#       ▼
#    CORS middleware
#       │
#       ▼
#  DecryptionMiddleware (only selected paths)
#       │
#       ▼
#  LoggingMiddleware (logs request metadata)
#       │
#       ▼
#      Router / Endpoint
#       │
#       ▼
#  EncryptionMiddleware (only selected paths)
#       │
#       ▼
#  Response sent to client
#       │
#       ▼
#  Exception-catching middleware (catches unhandled errors)

## old working

# import os
# import json
# from decimal import Decimal
# from fastapi import FastAPI
# import mysql.connector
# from mysql.connector import Error
# import redis

# app = FastAPI()

# db_config = {
#     "host": os.getenv("DB_HOST", ""),
#     "user": os.getenv("DB_USER", ""),
#     "password": os.getenv("DB_PASSWORD", ""),
#     "database": os.getenv("DB_NAME", ""),
# }

# redis_client = redis.Redis(
#     host=os.getenv("REDIS_HOST", ""),
#     port=int(os.getenv("REDIS_PORT", 6379)),
#     password=os.getenv("REDIS_PASSWORD", ""),
#     decode_responses=True,
# )


# def convert_decimal(obj):
#     if isinstance(obj, Decimal):
#         return float(obj)
#     if isinstance(obj, dict):
#         return {k: convert_decimal(v) for k, v in obj.items()}
#     if isinstance(obj, list):
#         return [convert_decimal(i) for i in obj]
#     return obj

# @app.get("/employee/{name}")
# def get_employee(name: str):
#     # Try cache first
#     cached = redis_client.get(name)
#     if cached:
#         return {"employee": json.loads(cached), "source": "redis"}

#     connection = None
#     cursor = None

#     try:
#         connection = mysql.connector.connect(**db_config)
#         cursor = connection.cursor(dictionary=True)

#         cursor.execute("SELECT * FROM employees WHERE name = %s", (name,))
#         result = cursor.fetchone()

#         if result:
#             result = convert_decimal(result)

#             # Cache the result for 60 seconds
#             redis_client.setex(name, 60, json.dumps(result))

#             return {"employee": result, "source": "mysql"}

#         return {"message": f"No employee found with name '{name}'"}

#     except Error as e:
#         return {"error": str(e)}

#     finally:
#         if cursor:
#             cursor.close()
#         if connection and connection.is_connected():
#             connection.close()

# @app.get("/")
# def root():
#     return {"message": "FastAPI is running!"}



