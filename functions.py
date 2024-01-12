from work_with_db import DayManager
import datetime


def home(weekday=None):
    md = DayManager(datetime.date.today())
    if weekday and 0 < weekday < 8:
        week = md.make_week()
        md = DayManager(week[weekday - 1])

    return md
