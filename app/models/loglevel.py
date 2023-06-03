from enum import Enum


class LogLevel(Enum):
    trace = "TRACE"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"
    success = "SUCCESS"
    critical = "CRITICAL"
    @classmethod
    def set_log_level(cls, level):
        if level.upper() in cls._value2member_map_:
            return cls._member_map_.get(level).value
        else:
            return cls._member_map_.get("info").value