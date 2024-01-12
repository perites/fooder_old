import logging
import datetime

from flask import Flask, render_template, request, redirect, url_for, jsonify


from databases import Dish, Ingridient
from work_with_db import DayManager, DishManager, IngrManager
from decorators import error_catcher, login_required, login_manager, login_user, User
import functions

from confg import date_format, confg_passwords


app = Flask(__name__)
app.config["SECRET_KEY"] = 'c42e8d7a0a1003456342385cb9e30b6b'

login_manager.init_app(app)


logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='fooder.log', filemode='w', level=logging.INFO)


@app.route("/<int:weekday>/")
@app.route("/")
@error_catcher
def home(weekday=None):

    md = functions.home(weekday)

    return render_template("main.html", day=md.day)


@app.route("/api/")
@error_catcher
def home_api():

    md = functions.home()
    # md.day.to_json_for_api()

    return jsonify(md.day.to_json_for_api())


@app.route("/day/<date>/")
@error_catcher
def for_specific_date(date):

    md = DayManager(datetime.datetime.strptime(date, date_format).date())

    return render_template("day_date.html", day=md.day, week=md.make_week())


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
        try:
            Dish.get(Dish.name == dish_name)
        except Dish.DoesNotExist:
            Dish.create(name=dish_name)
        return redirect(f"/dish/edit/{dish_name}")

    return render_template("dish_add.html")


@app.route("/dish/edit/<dish_name>", methods=["GET", "POST"])
@login_required
@error_catcher
def dish_edit(dish_name):

    if request.method == "POST":
        dish = DishManager(dish_name)
        ingr = request.args.get("ingr")
        if not ingr:
            if request.args.get("change_name"):
                new_name = request.form["new_name"]
                dish.change_name(new_name)
                return redirect(f"/dish/edit/{dish.dish_obj.name}")

            elif request.args.get("delete"):
                dish.delete_dish()
                return redirect(url_for("home"))

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
# @error_catcher
def list_for_date(date):
    md = DayManager(datetime.datetime.strptime(date, date_format).date())
    ingr_list = [ingr for ingr in md.day.ingredients]
    return render_template("list.html", ingr_list=ingr_list, day=md.day)


@app.route("/ingredients/edit/", methods=["GET", "POST"])
@login_required
@error_catcher
def edit_ingredients():
    if request.method == "POST":
        ingr = request.args.get("ingr")
        if not ingr:
            name = request.form["name"]
            where_to_buy = request.form["where_to_buy"]
            Ingridient.create(name=name, where_to_buy=where_to_buy)
            return redirect("/ingredients/edit/")

        ingr = IngrManager(ingr)
        if request.args.get("delete"):
            ingr.delete_ingr()
            return redirect("/ingredients/edit/")

        elif request.args.get("new_name"):
            new_name = request.form["new_name"]
            ingr.change_name(new_name)
            return redirect("/ingredients/edit/")

        elif request.args.get("where_to_buy"):
            where_to_buy = request.form["where_to_buy"]
            ingr.change_where_to_buy(where_to_buy)
            return redirect("/ingredients/edit/")

    return render_template("ingrs_edit.html", ingrs=Ingridient.select().order_by(Ingridient.name))


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
