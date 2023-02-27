from django.shortcuts import render, Http404
from mysql.connector import connect
import json

database_data = {
    "host": "kdaminov.ru",
    "user": "a0742849_olympbot",
    "password": "4CiSluK7",
    "database": "a0742849_olympbot",
    "charset": "utf8"
}


class Database:
    def __init__(self):
        self.connection = connect(**database_data)

    def run(self, *args):
        if not self.connection.is_connected():
            self.connection = connect(**database_data)
        with self.connection.cursor() as cursor:
            cursor.execute(*args)
            self.connection.commit()

    def one(self, *args):
        if not self.connection.is_connected():
            self.connection = connect(**database_data)
        with self.connection.cursor() as cursor:
            cursor.execute(*args)
            res: tuple | None = cursor.fetchone()
            if res is not None and len(res) == 1:
                return res[0]
            else:
                return res

    def all(self, *args):
        if not self.connection.is_connected():
            self.connection = connect(**database_data)
        with self.connection.cursor() as cursor:
            cursor.execute(*args)
            res = cursor.fetchall()
            if len(res) != 0 and len(res[0]) == 1:
                res = [item[0] for item in res]
            return res

    def __del__(self):
        self.connection.close()


db = Database()


def show_subjects(request, user_id: int):
    data = db.one("SELECT data FROM users WHERE user_id = %s" % user_id)
    if data is None:
        return Http404
    data = json.loads(data)
    return render(request, "subjects.html", data)


def show_olympiads(request, user_id: int):
    data = db.one("SELECT data FROM users WHERE user_id = %s" % user_id)
    if data is None:
        return Http404
    data = json.loads(data)
    user_olympiads = sorted(data["olympiads"])
    cool_olympiads = db.all("SELECT activity_name, activity_id FROM cool_olympiads")
    context = {
        "user_olympiads": user_olympiads,
        "cool_olympiads": cool_olympiads
    }
    return render(request, "olympiads.html", context)
