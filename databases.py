from peewee import SqliteDatabase, Model, CharField, DateField, ForeignKeyField, TextField

db = SqliteDatabase('fooder.db')


class Dish(Model):
    name = CharField(unique=True)

    class Meta:
        database = db


class Ingridient(Model):
    name = CharField(unique=True)
    where_to_buy = CharField(choices=(
        ('Bedronka', 'Bedronka'),
        ('Kredens', 'Kredens'),
        ('Delivery', 'Delivery')
    ))

    class Meta:
        database = db


class IngrToDish(Model):
    ingredient = ForeignKeyField(Ingridient)
    how_much_ingr = CharField()
    dish = ForeignKeyField(Dish, backref="ingredients")

    class Meta:
        database = db


class DayMenu(Model):
    date = DateField(unique=True)
    lunch = TextField()
    dinner = TextField()

    class Meta:
        database = db


# db.create_tables([Dish, Ingridient, IngrToDish, DayMenu])
