import logging
import datetime

from flask import Flask, render_template, request, redirect

from databases import Dish
from work_with_db import ManageDay, ManageDish
from decorators import error_catcher


app = Flask(__name__)


logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='fooder.log', filemode='w', level=logging.INFO)


@app.route("/<int:weekday>/")
@app.route("/")
@error_catcher
def home(weekday=None):
    md = ManageDay(datetime.date.today())
    if weekday:
        week = md.make_week()
        if 0 < weekday < 8:
            md = ManageDay(week[weekday - 1])

    return render_template("main.html", day=md.day)


@app.route("/menu/<date>/")
@error_catcher
def menu(date):
    date_format = "%Y-%m-%d"
    md = ManageDay(datetime.datetime.strptime(date, date_format).date())
    return render_template("menu.html", days=md.days_of_week())


@app.route("/dish/<dish_name>/")
@error_catcher
def dish(dish_name):
    dish = ManageDish(dish_name)
    return render_template("dish.html", ingr=dish.get_ingredients())


@app.route("/list/<date>/")
@error_catcher
def list(date):
    date_format = "%Y-%m-%d"
    md = ManageDay(datetime.datetime.strptime(date, date_format).date())
    ingr_list = [ingr for ingr in md.day.ingredients]
    return render_template("list.html", ingr_list=ingr_list, day=md.day)


@app.route("/menu/edit/<date>/", methods=["GET"])
@error_catcher
def menu_edit_get(date):
    date_format = "%Y-%m-%d"
    md = ManageDay(datetime.datetime.strptime(date, date_format).date())
    return render_template("menu_edit.html", days=md.days_of_week(), dishes=Dish.select())


@app.route("/menu/edit/<date>", methods=["POST"])
@error_catcher
def menu_edit_post(date):
    date_format = "%Y-%m-%d"
    md = ManageDay(datetime.datetime.strptime(date, date_format).date())
    forms = ['dish_lunch', 'dish_dinner', 'dish_lunch_delete', 'dish_dinner_delete']

    for form in forms:
        try:
            selected_dish = request.form[form]
            md.change_day(selected_dish=selected_dish, form=form)
        except Exception:
            pass

    return redirect("/menu/edit/" + date)


if __name__ == '__main__':
    app.run(debug=True)
