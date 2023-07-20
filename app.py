import logging

from flask import Flask, render_template

from databases import *
from work_with_db import *
from decorators import error_catcher


app = Flask(__name__)


logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='fooder.log', filemode='w', level=logging.INFO)


@app.route("/<int:weekday>/")
@app.route("/")
@error_catcher
def home(weekday=None):
    date = datetime.date.today()
    week = make_week(date)
    if weekday:
        if 0 < weekday < 8:
            date = week[weekday - 1]

    day = menu_for_day(date)
    return render_template("main.html", day=day)


@app.route("/menu/<date>/")
@error_catcher
def menu(date):
    date_format = "%Y-%m-%d"
    date = datetime.datetime.strptime(date, date_format).date()
    days = days_of_week(date)
    return render_template("menu.html", days=days)


@app.route("/dish/<dish_name>/")
@error_catcher
def dish(dish_name):
    ingr = get_ingredients(dish_name)
    return render_template("dish.html", ingr=ingr)


if __name__ == '__main__':
    app.run(debug=True)
