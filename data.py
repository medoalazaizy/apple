import os
import sqlite3

class database:
    def __init__(self):
        if not os.path.isfile("data.db"):
            with sqlite3.connect("data.db") as connection:
                cursor = connection.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS accounts (session TEXT, number TEXT, twofa TEXT, points INTEGER DEFAULT 0)")
                connection.commit()

    def get(self, number):  
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            try:
                res = cursor.execute(f"SELECT * FROM accounts WHERE number='{number}'")
                data = cursor.fetchall()
                for lik in data:
                    return lik
            except:
                return False

    def delete(self, number):
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            try:
                res = cursor.execute(f"DELETE FROM accounts WHERE number='{number}'")
                connection.commit()  
                return True
            except:
                return False

    def view(self):
        list = []
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM accounts")
            entry = cursor.fetchall()
            for i in entry:
                list.append(i)
        return list

    def add_no(self, session, number): 
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO accounts(session, number) VALUES ('{session}', '{number}')")
            connection.commit()
            return True

    def add_yes(self, session, number, twofa):
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO accounts(session, number, twofa) VALUES ('{session}', '{number}', '{twofa}')")
            connection.commit()
            return True

    def update_points(self, string_session, points):
        with sqlite3.connect("data.db") as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE accounts SET points = points + {points} WHERE session = '{string_session}'")
            connection.commit()
            return True
