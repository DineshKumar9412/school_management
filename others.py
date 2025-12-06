
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
