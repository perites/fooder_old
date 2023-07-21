import logging
import datetime

from flask import Flask, render_template, request, redirect

from databases import Dish
from work_with_db import ManageTables
from decorators import error_catcher


app = Flask(__name__)


logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='fooder.log', filemode='w', level=logging.INFO)


@app.route("/<int:weekday>/")
@app.route("/")
@error_catcher
def home(weekday=None):
    date = datetime.date.today()
    if weekday:
        week = ManageTables().make_week(date)
        if 0 < weekday < 8:
            date = week[weekday - 1]

    day = ManageTables().menu_for_day(date)
    return render_template("main.html", day=day)


@app.route("/menu/<date>/")
@error_catcher
def menu(date):
    date_format = "%Y-%m-%d"
    date = datetime.datetime.strptime(date, date_format).date()
    days = ManageTables().days_of_week(date)
    return render_template("menu.html", days=days)


@app.route("/dish/<dish_name>/")
@error_catcher
def dish(dish_name):
    ingr = ManageTables().get_ingredients(dish_name)
    return render_template("dish.html", ingr=ingr)


@app.route("/list/<date>/")
@error_catcher
def list(date):
    date_format = "%Y-%m-%d"
    date = datetime.datetime.strptime(date, date_format).date()
    day = ManageTables().menu_for_day(date)
    ingr_list = [ingr for ingr in day.ingredients]
    return render_template("list.html", ingr_list=ingr_list, day=day)


@app.route("/menu/edit/<date>/", methods=["GET"])
@error_catcher
def menu_edit_get(date):
    date_format = "%Y-%m-%d"
    date = datetime.datetime.strptime(date, date_format).date()

    days = ManageTables().days_of_week(date)
    dishes = Dish.select()

    return render_template("menu_edit.html", days=days, dishes=dishes)


@app.route("/menu/edit/<date>", methods=["POST"])
@error_catcher
def menu_edit_post(date):

    date_format = "%Y-%m-%d"
    date_obj = datetime.datetime.strptime(date, date_format).date()

    forms = ['dish_lunch', 'dish_dinner', 'dish_lunch_delete', 'dish_dinner_delete']

    for form in forms:
        try:
            selected_dish = request.form[form]
            ManageTables().change_day(date_obj, selected_dish=selected_dish, form=form)
        except Exception:
            pass

    return redirect("/menu/edit/" + date)


if __name__ == '__main__':
    app.run(debug=True)
