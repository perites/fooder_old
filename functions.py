from work_with_db import DayManager
import datetime


def home(weekday=None):
    md = DayManager(datetime.date.today())
    if weekday:
        week = md.make_week()
        if 0 < weekday < 8:
            md = DayManager(week[weekday - 1])

    return md
