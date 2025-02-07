import time


class TimeUtiliti:

    @staticmethod
    def get_timestamp() -> str:
        return str(int(time.time() * 1000))