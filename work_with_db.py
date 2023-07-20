import datetime
import json
from databases import *
import random


# def see_all():
#     # ingrs = Ingridient.select()
#     # # if not ingrs:
#     # #     print(ingrs)
#     # for ingr in ingrs:
#     #     print(ingr.name, "--- ingr")

#     dishes = Dish.select()
#     for dish in dishes:
#         print("\n", dish.name, "--- dish")
#         print("recept:")
#         recept = dish.ingredients
#         for ingr in recept:
#             print(ingr.ingredient.name, ingr.hot_much_ingr)


# see_all()
# dishes = ["mashed potato", "chicken", "salat", "kotlet"]
# lunch = ["salat", "kotlet"]
# dinner = ["mashed potato", "chicken"]


# def create_tetttt():
#     for n in range(-3, 12):
#         menu_for_day_l = [random.choice(dishes), random.choice(dishes)]
#         menu_for_day_d = [random.choice(dishes), random.choice(dishes)]
#         DayMenu.create(date=datetime.date.today() + datetime.timedelta(days=n), lunch=json.dumps(menu_for_day_l), dinner=json.dumps(menu_for_day_d))


# menu_for_day_l = random.choice(dishes)
# menu_for_day_d = random.choice(dishes)
# DayMenu.create(date=datetime.date.today() + datetime.timedelta(days=-2), lunch=json.dumps(menu_for_day_l), dinner=json.dumps(menu_for_day_d))


# create_tetttt()


# def recept_for_weeks():
#     week = []
#     for x in DayMenu.select():
#         if x.date not in week:
#             print("\nnew week")
#             week = make_week(x.date)

#         print("\nweekday : ", x.date.isocalendar().weekday, "\nmenu lunch:", x.lunch, "\nmenu dinner :", x.dinner)


# recept_for_weeks()

class Day():
    def __init__(self, date, lunch, dinner):
        self.date = date
        self.week_number = date.isocalendar().week
        self.weekday = self.weekday_name(date.isocalendar().weekday)
        self.lunch = json.loads(lunch)
        self.dinner = json.loads(dinner)

    def weekday_name(self, weekday_number):
        weekday_name = {
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday",
            7: "Sunday"}

        return weekday_name[weekday_number]


def make_week(date):
    week = []
    week_number = date.isocalendar().week

    for n in range(-7, 8):
        new_date = date + datetime.timedelta(days=n)
        if new_date.isocalendar().week == week_number:
            week.append(new_date)

    week.sort()
    return week


def days_of_week(date):
    week = make_week(date)
    return [menu_for_day(day_date) for day_date in week]


def menu_for_day(date):
    day = DayMenu.get(DayMenu.date == date)
    return Day(day.date, day.lunch, day.dinner)


def get_ingredients(dish_name):
    dish = Dish.get(Dish.name == dish_name)
    return dish.ingredients

# date = "2023-07-20"
# date_format = "%Y-%m-%d"
# date = datetime.datetime.strptime(date, date_format).date()
# days_of_week(date)
# date = "2023-07-20"
# date_format = "%Y-%m-%d"
# date = datetime.datetime.strptime(date, date_format)
# print(date, "---date")
# print(datetime.date.today())
# print(date == datetime.date.today())
# print(type(date.date()), type(datetime.date.today()))
# a = menu_for_day(datetime.date.today())
# print(a.lunch)


# recept_for_week(datetime.date.today())
# print("\n", x.date)
# print(x.lunch, "--- lunch")
# print(x.dinner, "--- dinner")
#     # print(x.lunch)
#     # print(type(json.dumps(["salat", "kotlet"])))
#     a = ["salat", "kotlet"]
#     b = json.dumps(a)
#     print(b)
#     print(json.loads(b))
# print(x.date, json.loads(x.lunch)[1], json.loads(x.dinner)[0])
# dishes = Dish.select().where(Dish.name == json.loads(x.lunch)[1])
# for dish in dishes:
#     print("\n", dish.name, "--- dish")
#     print("recept:")
#     recept = dish.ingredients
#     for ingr in recept:
#         print(ingr.ingredient.name, ingr.hot_much_ingr)
# db.create_tables([Ingridient, Dish, IngrToDish, DayMenu])
# # Ingridient.create(name="onoin", where_to_buy="Kredens")
# # Ingridient.drop_table()
# import date


# def resrart():
#     DayMenu.drop_table()
#     db.create_tables([Ingridient, Dish, IngrToDish, DayMenu])


# resrart()
# # Dish.create(name="kotlet")
# # IngrToDish.create(ingredient=Ingridient.get(Ingridient.name == "onoin"), hot_much_ingr="0.5 kg", dish=Dish.get(Dish.name == "kotlet"))
# see_all()

# WeekMenu.create(start_day=date.date())
# # def create_menu_for_day():

# if week_day_original == 1:

# print(week_day_original)

# for n in range(-7, 8):
#     print(n)

# next_day = datetime.timedelta(days=0)

# specific_date = datetime.date(2023, 7, 24)
# a = specific_date + datetime.timedelta(days=0)
# print(a)
#

# datetime.timedelta(days=1)
# iso_year, iso_week, iso_weekday = specific_date.isocalendar()
# print(specific_date.isocalendar().weekday)
# iso_year2, iso_week2, iso_weekday2 = ().isocalendar()
# while iso_week == iso2_week:

# specific_date2 = datetime.date(2023, 7, 30)

# print(specific_date < datetime.date(2023, 7, 31) < specific_date2)
# iso_year, iso_week, iso_weekday = specific_date2.isocalendar()

# print(f"ISO Year: {iso_year}")
# print(f"ISO Week: {iso_week}")
# print(f"ISO Weekday: {iso_weekday}")

# make_week(datetime.date(2023, 7, 24))
