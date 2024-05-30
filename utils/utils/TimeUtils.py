import datetime


def time_to_str(time):
    if time.days > 0:
        return f"{time.days}天{time.seconds // 3600}小时{time.seconds % 3600 // 60}分钟{time.seconds % 60}秒"
    elif time.seconds > 0:
        return f"{time.seconds // 3600}小时{time.seconds % 3600 // 60}分钟{time.seconds % 60}秒"
    elif time.seconds > 0:
        return f"{time.seconds}秒"


def time_to_time_length(time: float):
    return time_to_str(datetime.timedelta(seconds=time))
