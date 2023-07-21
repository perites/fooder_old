import datetime
import json

from databases import DayMenu, Dish


class Day():
    def __init__(self, day_obj):
        self.date = day_obj.date
        self.week_number = day_obj.date.isocalendar().week
        self.weekday = self.weekday_name(day_obj.date.isocalendar().weekday)
        self.lunch = self.get_dish_objects(json.loads(day_obj.lunch))
        self.dinner = self.get_dish_objects(json.loads(day_obj.dinner))
        self.ingredients = self.get_ingredients_for_day(day_obj)

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

    def get_ingredients_for_day(self, day):
        ingredients = {}
        if self.lunch:
            for dish in self.lunch:
                for ingr in dish.ingredients:
                    if ingr not in ingredients and ingr.ingredient.where_to_buy != "Delivery":
                        ingredients[ingr] = ingr.hot_much_ingr
                    else:
                        ingredients[ingr] += "+" + ingr.hot_much_ingr
        if self.dinner:
            for dish in self.dinner:
                for ingr in dish.ingredients:
                    if ingr not in ingredients and ingr.ingredient.where_to_buy != "Delivery":
                        ingredients[ingr] = ingr.hot_much_ingr
                    else:
                        ingredients[ingr] += "+" + ingr.hot_much_ingr

        return list(ingredients.items())

    def get_dish_objects(self, list_dishes):
        return [ManageDish(dish_name).dish_obj for dish_name in list_dishes]


class ManageDish():
    def __init__(self, dish_name):
        self.dish_obj = Dish.get(Dish.name == dish_name)

    def get_ingredients(self):
        return self.dish_obj.ingredients


class ManageDay():
    def __init__(self, date):
        try:
            self.day_obj = DayMenu.get(DayMenu.date == date)
        except DayMenu.DoesNotExist:
            self.day_obj = DayMenu.create(date=date, lunch=json.dumps([]), dinner=json.dumps([]))

        self.day = Day(self.day_obj)

    def make_week(self):
        week = []
        week_number = self.day_obj.date.isocalendar().week

        for n in range(-7, 8):
            new_date = self.day_obj.date + datetime.timedelta(days=n)
            if new_date.isocalendar().week == week_number:
                week.append(new_date)

        week.sort()
        return week

    def days_of_week(self):
        return [ManageDay(day_date).day for day_date in self.make_week()]

    def change_day(self, selected_dish, form):
        if form == 'dish_lunch':
            lunch_dishes = json.loads(self.day_obj.lunch)
            lunch_dishes.append(selected_dish)
            self.day_obj.lunch = json.dumps(lunch_dishes)

        elif form == 'dish_dinner':
            dinner_dishes = json.loads(self.day_obj.dinner)
            dinner_dishes.append(selected_dish)
            self.day_obj.dinner = json.dumps(dinner_dishes)

        elif form == 'dish_lunch_delete':
            lunch_dishes = json.loads(self.day_obj.lunch)
            lunch_dishes.remove(selected_dish)
            self.day_obj.lunch = json.dumps(lunch_dishes)

        elif form == 'dish_dinner_delete':
            dinner_dishes = json.loads(self.day_obj.dinner)
            dinner_dishes.remove(selected_dish)
            self.day_obj.dinner = json.dumps(dinner_dishes)

        self.day_obj.save()


# import random
# def create_tetttt():
#     dishes = ["mashed potato", "chicken", "salat", "kotlet"]
#     for n in range(-4, 11):
#         menu_for_day_l = [random.choice(dishes), random.choice(dishes)]
#         menu_for_day_d = [random.choice(dishes), random.choice(dishes)]
#         DayMenu.create(date=datetime.date.today() + datetime.timedelta(days=n), lunch=json.dumps(menu_for_day_l), dinner=json.dumps(menu_for_day_d))

# create_tetttt()


# def recept_for_weeks():
#     week = []
#     for x in DayMenu.select():
#         if x.date not in week:
#             print("\nnew week")
#             week = ManageTables().make_week(x.date)

#         date_format = "%Y-%m-%d"

#         # if x.date == datetime.datetime.strptime("2023-07-21", date_format).date():
#         #     lunch_dishes = json.loads(x.lunch)
#         #     # lunch_dishes.pop(2)
#         #     # lunch_dishes.pop(2)
#         #     x.lunch = json.dumps(lunch_dishes)
#         #     x.save()

#         print("\nweekday : ", x.date.isocalendar().weekday, "\nmenu lunch:", x.lunch, "\nmenu dinner :", x.dinner)

# recept_for_weeks()


# def see_all():
#     ingrs = Ingridient.select()
#     if not ingrs:
#         print(ingrs)
#     for ingr in ingrs:
#         print(ingr.name, "--- ingr")

#     dishes = Dish.select()
#     for dish in dishes:
#         print("\n", dish.name, "--- dish")
#         print("recept:")
#         recept = dish.ingredients
#         for ingr in recept:
#             print(ingr.ingredient.name, ingr.hot_much_ingr)

# see_all()
