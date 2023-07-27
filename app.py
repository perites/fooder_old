import logging
import datetime

from flask import Flask, render_template, request, redirect, url_for


from flask_login import LoginManager, UserMixin, login_user


from databases import Dish, Ingridient
from work_with_db import DayManager, DishManager
from decorators import error_catcher, login_required

from confg import date_format, confg_passwords

app = Flask(__name__)
app.config["SECRET_KEY"] = 'c42e8d7a0a1003456342385cb9e30b6b'

login_manager = LoginManager()
login_manager.init_app(app)


logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='fooder.log', filemode='w', level=logging.INFO)


@app.route("/<int:weekday>/")
@app.route("/")
@error_catcher
def home(weekday=None):

    md = DayManager(datetime.date.today())
    if weekday:
        week = md.make_week()
        if 0 < weekday < 8:
            md = DayManager(week[weekday - 1])
    return render_template("main.html", day=md.day)


@app.route("/day/<date>/")
@error_catcher
def for_specific_date(date, weekday=None):
    md = DayManager(datetime.datetime.strptime(date, date_format).date())
    week = md.make_week()

    return render_template("day_date.html", day=md.day, week=week)


@app.route("/menu/<date>/")
@error_catcher
def menu(date):
    md = DayManager(datetime.datetime.strptime(date, date_format).date())
    return render_template("menu.html", days=md.create_days_of_week())


@app.route("/dish/<dish_name>/")
@error_catcher
def dish(dish_name):
    dish = DishManager(dish_name)
    return render_template("dish.html", dish=dish)


@app.route("/dish/add/", methods=["GET", "POST"])
@login_required
@error_catcher
def dish_add():
    if request.method == "POST":
        dish_name = request.form["dish_name"]
        where_to_buy = request.form["where_to_buy"]
        try:
            Dish.get(Dish.name == dish_name)
        except Exception as e:
            print(e)
            Dish.create(name=dish_name, where_to_buy=where_to_buy)
        return redirect(f"/dish/edit/{dish_name}")

    return render_template("dish_add.html")


@app.route("/dish/edit/<dish_name>", methods=["GET", "POST"])
@login_required
# @error_catcher
def dish_edit(dish_name):

    if request.method == "POST":
        dish = DishManager(dish_name)
        ingr = request.args.get("ingr")
        if not ingr:
            ingr = request.form["add_ingr"]
            amount = request.form["amount"]
            dish.add_ingridient(ingr=ingr, amount=amount)
            return redirect(f"/dish/edit/{dish.dish_obj.name}")

        if request.args.get("delete"):
            dish.delete_ingr(ingr=ingr)
            return redirect(f"/dish/edit/{dish_name}")
        else:
            amount = request.form["amount"]
            dish.change_amount(amount=amount, ingr=ingr)
            return redirect(f"/dish/edit/{dish_name}")

    dish = DishManager(dish_name)
    return render_template("dish_edit.html", dish=dish, ingrds=Ingridient.select())


@app.route("/list/<date>/")
@error_catcher
def list_for_date(date):
    md = DayManager(datetime.datetime.strptime(date, date_format).date())
    ingr_list = [ingr for ingr in md.day.ingredients]
    return render_template("list.html", ingr_list=ingr_list, day=md.day)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def is_authenticated(self):
        return True


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form["password"]
        if password in confg_passwords:
            user_obj = User(password)
            login_user(user_obj)
            path = request.args.get("next_url")
            if not path:
                return redirect(url_for("home"))
            return redirect(path)

    return render_template("login.html")


@app.route("/menu/edit/<date>/", methods=["GET"])
@login_required
@error_catcher
def menu_edit_get(date):
    md = DayManager(datetime.datetime.strptime(date, date_format).date())
    return render_template("menu_edit.html", days=md.create_days_of_week(), dishes=Dish.select())


@app.route("/menu/edit/<date>", methods=["POST"])
@error_catcher
def menu_edit_post(date):
    form = request.args.get("form")
    md = DayManager(datetime.datetime.strptime(date, date_format).date())
    selected_dish = request.form[form]
    md.change_day(selected_dish=selected_dish, form=form)

    return redirect(f"/menu/edit/{date}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
