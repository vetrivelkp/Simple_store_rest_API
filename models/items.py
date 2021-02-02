import sqlite3

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect("mydata.db")
        cursor = connection.cursor()

        select_sql = "SELECT * FROM items WHERE name = ?"
        items = cursor.execute(select_sql, (name,))
        row = items.fetchone()
        connection.close()
        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect("mydata.db")
        cursor = connection.cursor()

        insert_sql = "INSERT INTO items VALUES(?,?)"

        cursor.execute(insert_sql, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect("mydata.db")
        cursor = connection.cursor()

        upd_sql = "UPDATE items SET price = ? WHERE name = ?"

        cursor.execute(upd_sql, (self.price, self.name))
        connection.commit()
        connection.close()
