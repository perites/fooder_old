import datetime
import json
import logging


from databases import DayMenu, Dish, IngrToDish, Ingridient


class Day():
    def __init__(self, day_obj):
        self.day_obj = day_obj
        self.date = day_obj.date
        self.week_number = day_obj.date.isocalendar()[1]
        self.weekday = self.weekday_name(day_obj.date.isocalendar()[2])
        self.lunch = self.get_dish_objects(json.loads(day_obj.lunch), "l")
        self.dinner = self.get_dish_objects(json.loads(day_obj.dinner), "d")
        self.deliverys = {}
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
        for dishes in [self.lunch, self.dinner]:
            for dish in dishes or []:
                for ingr in dish.ingredients:
                    if ingr.ingredient.name not in ingredients and ingr.ingredient.where_to_buy != "Delivery":
                        ingredient = {}
                        ingredient["name"] = ingr.ingredient.name
                        ingredient["amount"] = [ingr.how_much_ingr]
                        ingredients[ingr.ingredient.name] = ingredient
                    elif ingr.ingredient.name in ingredients:
                        ingredients[ingr.ingredient.name]["amount"].append(ingr.how_much_ingr)

                    elif ingr.ingredient.where_to_buy == "Delivery":
                        if dish.name in json.loads(self.day_obj.lunch):
                            self.deliverys["lunch_delivery"] = {"delivery_name": dish.name, "link": ingr.ingredient.name}
                        elif dish.name in json.loads(self.day_obj.dinner):
                            self.deliverys["dinner_delivery"] = {"delivery_name": dish.name, "link": ingr.ingredient.name}

        for k, v in ingredients.items():
            ingredients[k]["amount"] = "+".join(v["amount"])
        return list(ingredients.values())

    def get_dish_objects(self, list_dishes, time):
        answer = []
        for dish_name in list_dishes:
            try:
                answer.append(Dish.get(Dish.name == dish_name))
            except Dish.DoesNotExist:
                logging.error(f"in get_dish_objects : Probaly deleted dish : {dish_name}")
                if time == 'l':
                    lunch_dishes = json.loads(self.day_obj.lunch)
                    lunch_dishes.remove(dish_name)
                    self.day_obj.lunch = json.dumps(lunch_dishes)
                elif time == "d":
                    dinner_dishes = json.loads(self.day_obj.dinner)
                    dinner_dishes.remove(dish_name)
                    self.day_obj.dinner = json.dumps(dinner_dishes)

                self.day_obj.save()

        return answer

    def to_json_for_api(self):
        json_data = {"date": self.date,
                     "weekday": self.weekday,
                     "lunch": json.loads(self.day_obj.lunch),
                     "dinner": json.loads(self.day_obj.dinner),
                     "deliverys": self.deliverys,
                     "ingredients": self.ingredients
                     }

        return json_data


class IngrManager():
    def __init__(self, ingr_name):
        self.ingr_obj = Ingridient.get(Ingridient.name == ingr_name)

    def delete_ingr(self):
        for recept in IngrToDish.select().where(IngrToDish.ingredient == self.ingr_obj):
            recept.delete_instance()
        self.ingr_obj.delete_instance()

    def change_name(self, new_name):
        self.ingr_obj.name = new_name
        self.ingr_obj.save()

    def change_where_to_buy(self, where_to_buy):
        self.ingr_obj.where_to_buy = where_to_buy
        self.ingr_obj.save()


class DishManager():
    def __init__(self, dish_name):
        self.dish_obj = Dish.get(Dish.name == dish_name)

    def add_ingridient(self, ingr, amount):
        IngrToDish.create(ingredient=Ingridient.get(Ingridient.name == ingr), how_much_ingr=amount, dish=self.dish_obj)

    def delete_ingr(self, ingr):
        ingr = Ingridient.get(Ingridient.name == ingr)
        ingr_to_delete = IngrToDish.get(IngrToDish.ingredient == ingr, IngrToDish.dish == self.dish_obj)
        ingr_to_delete.delete_instance()

    def change_amount(self, ingr, amount):
        ingr = Ingridient.get(Ingridient.name == ingr)
        ingr_to_change = IngrToDish.get(IngrToDish.ingredient == ingr, IngrToDish.dish == self.dish_obj)
        ingr_to_change.how_much_ingr = amount
        ingr_to_change.save()

    def change_name(self, new_name):
        self.dish_obj.name = new_name
        self.dish_obj.save()

    def delete_dish(self):
        for recept in IngrToDish.select().where(IngrToDish.dish == self.dish_obj):
            recept.delete_instance()

        self.dish_obj.delete_instance()

    def get_ingredients(self):
        return self.dish_obj.ingredients


class DayManager():
    def __init__(self, date):
        try:
            self.day_obj = DayMenu.get(DayMenu.date == date)
        except DayMenu.DoesNotExist:
            self.day_obj = DayMenu.create(date=date, lunch=json.dumps([]), dinner=json.dumps([]))

        self.day = Day(self.day_obj)

    def make_week(self):
        week = []
        week_number = self.day_obj.date.isocalendar()[1]

        for n in range(-7, 8):
            new_date = self.day_obj.date + datetime.timedelta(days=n)
            if new_date.isocalendar()[1] == week_number:
                week.append(new_date)

        week.sort()
        return week

    def create_days_of_week(self):
        return [DayManager(day_date).day for day_date in self.make_week()]

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
