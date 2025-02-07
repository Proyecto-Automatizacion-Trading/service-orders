import time

from datetime import datetime


class TimeUtility:

    @staticmethod
    def get_timestamp() -> str:
        return str(int(time.time() * 1000))

    @staticmethod
    def get_timestamp_datetime() -> str:
        return str(int(datetime.now().timestamp() * 1000))