import os
import logging
import traceback
import json
from datetime import datetime
import pytz
from app.core.environment import LOG_DIR


class JsonFormatter(logging.Formatter):
    """
    Jsonフォーマッタークラス
    """

    def format(self, record: logging.LogRecord):
        timestamp = datetime.now(pytz.timezone("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S %Z")
        log_record = {
            "timestamp": timestamp,
            "log_level": getattr(record, "levelname", ""),
            "request_id": getattr(record, "request_id", ""),
            "lavel": getattr(record, "msg", ""),
        }

        if record.name == "request":
            log_record.update(
                {
                    "detail": {
                        "protocol": getattr(record, "protocol", ""),
                        "host": getattr(record, "host", ""),
                        "url": getattr(record, "url", ""),
                        "method": getattr(record, "method", ""),
                    }
                }
            )
        elif record.name == "response":
            log_record.update(
                {
                    "detail": {
                        "status": getattr(record, "status", ""),
                    }
                }
            )
        elif record.name == "error":
            log_record.update(
                {
                    "detail": {
                        "content": getattr(record, "content", ""),
                        "stack_trace": getattr(record, "stack_trace", ""),
                    }
                }
            )

        return json.dumps(log_record, ensure_ascii=False)


class JsonFileHandler(logging.FileHandler):
    """
    Jsonファイルハンドラークラス
    """

    def __init__(self, filename):
        super().__init__(filename, encoding="utf-8")
        self.setFormatter(JsonFormatter())


# フォルダの作成
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# ログファイルパス
log_file_path: str = f"{LOG_DIR}/app.log"

# ログ設定
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"json": {"()": JsonFormatter}},
        "handlers": {
            "app_file_handler": {"level": "INFO", "class": JsonFileHandler, "filename": log_file_path},
        },
        "loggers": {
            "request": {"handlers": ["app_file_handler"], "level": "INFO", "propagate": False},
            "response": {"handlers": ["app_file_handler"], "level": "INFO", "propagate": False},
            "error": {"handlers": ["app_file_handler"], "level": "ERROR", "propagate": False},
        },
    }
)


def request_log(request_id: str, lavel: str, protocol: str, host: str, url: str, method: str):
    logger = logging.getLogger("request")
    logger.info(
        lavel,
        extra={
            "request_id": request_id,
            "protocol": protocol,
            "host": host,
            "url": url,
            "method": method,
        },
    )


def response_log(request_id: str, lavel: str, status: str):
    logger = logging.getLogger("response")
    logger.info(
        lavel,
        extra={
            "request_id": request_id,
            "status": status,
        },
    )


def error_log(request_id: str, lavel: str, content: str):
    logger = logging.getLogger("error")
    stack_trace = traceback.format_exc()
    logger.error(
        lavel,
        extra={
            "request_id": request_id,
            "content": content,
            "stack_trace": stack_trace,
        },
    )
