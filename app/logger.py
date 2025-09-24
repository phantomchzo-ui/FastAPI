import logging
from datetime import datetime, timezone
from pythonjsonlogger import jsonlogger

from app.config import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            log_record["timestamp"] = datetime.now(timezone.utc).isoformat()

        log_record["level"] = record.levelname.upper()


logger = logging.getLogger()
logHandler = logging.StreamHandler()
logHandler.setFormatter(CustomJsonFormatter())
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)


