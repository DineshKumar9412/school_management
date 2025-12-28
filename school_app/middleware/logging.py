## Logger 
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging
from logging_loki import LokiHandler
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)  # or WARNING in heavy traffic
handler = logging.StreamHandler()  # can be replaced with FileHandler
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_logger():

    handler = LokiHandler(
        url="http://loki:3100/loki/api/v1/push",
        tags={"app": "fastapi"},
        version="1",
    )

    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s %(path)s %(method)s'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger("fastapi")
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return logger

loki_logger = get_logger()
        
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        if request.url.path != "/metrics":
            logger.info(
                "%s %s | %s | %.3fs",
                request.method,
                request.url.path,
                response.status_code,
                process_time
            )
        
        return response