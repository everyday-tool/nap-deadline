import datetime

def compute_time_left():
    deadlines = [
        (3, 0),
        (8, 30),
        (14, 0),
        (18, 20),
        (22, 40),
    ]
    t = datetime.datetime.now()

    if t.hour > 23:
        deadline = deadlines[0]
        hour, minute = deadline
        hour_left = hour + 24 - t.hour
        minute_left = minute - t.minute
    else:
        min_hour_left = 24
        min_minute_left = 60
        for hour, minute in deadlines:
            hour_left = hour - t.hour
            minute_left = minute - t.minute
            if hour_left < min_hour_left and hour_left > 0 or (hour_left == 0 and minute_left >= 0):
                min_hour_left = hour_left
                min_minute_left = minute_left
        hour_left = min_hour_left
        minute_left = min_minute_left

    if minute_left < 0:
        hour_left -= 1
        minute_left = 60 + minute_left

    return hour_left, minute_left


