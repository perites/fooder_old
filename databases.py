from peewee import SqliteDatabase, Model, CharField, DateField, ForeignKeyField, TextField

db = SqliteDatabase('fooder.db')


class Dish(Model):
    name = CharField()

    class Meta:
        database = db


class Ingridient(Model):
    name = CharField()
    where_to_buy = CharField(choices=(
        ('Bedronka', 'Bedronka'),
        ('Kredens', 'Kredens'),
        ('Delivery', 'Delivery')
    ))

    class Meta:
        database = db


class IngrToDish(Model):
    ingredient = ForeignKeyField(Ingridient)
    hot_much_ingr = CharField()
    dish = ForeignKeyField(Dish, backref="ingredients")

    class Meta:
        database = db


class DayMenu(Model):
    date = DateField(unique=True)
    lunch = TextField()
    dinner = TextField()

    class Meta:
        database = db
