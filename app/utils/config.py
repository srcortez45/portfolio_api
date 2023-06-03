from app.utils.settings import cnf
from notifiers.logging import NotificationHandler
from loguru import logger
import notifiers
import datetime

class NotificationManager(object):
    def __init__(self,app):
        self.args = {
        "chat_id":cnf.NOTIFICATION_CONFIG.channel,
        "token":cnf.NOTIFICATION_CONFIG.token
        }
        app.state._state["mode"] = cnf.LOG_LEVEL
        self._log_level = cnf.LOG_LEVEL
        self._notification_handler = notifiers.get_notifier("telegram")
        self.new_message(f"The application is running in {app.state._state}")
        handler = NotificationHandler("telegram", defaults=self.args)
        logger.add(handler, level=cnf.LOG_LEVEL)
        self._observers = []


    @property
    def log_level(self):
        return self._log_level


    @log_level.setter
    def log_level(self, value):
        self._log_level = value
        for callback in self._observers:
            logger.debug(f"changing log level {self._log_level}")
            self.new_message(f"changing log level {self._log_level}")
            callback(self._log_level)


    def bind_to(self, callback):
        logger.debug("bound")
        self._observers.append(callback)


    def new_message(self, message:str):
        get_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = self._notification_handler.notify(message=f"{get_time} | {self.log_level} | {message}", **self.args)
        logger.debug(result.status)


class NotificationState(object):
    def __init__(self, notifier_manager:NotificationManager):
        self.notifier_manager = notifier_manager
        self.notifier_manager.bind_to(self.update_log_level)

    def update_log_level(self, level):
        self.log_level = level
    
