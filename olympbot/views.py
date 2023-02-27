from django.shortcuts import render, Http404
from mysql.connector import connect
from django.views.decorators.cache import never_cache
import json

database_data = {
    "host": "kdaminov.ru",
    "user": "a0742849_olympbot",
    "password": "4CiSluK7",
    "database": "a0742849_olympbot",
    "charset": "utf8"
}


def run(*args):
    with connect(**database_data) as connection:
        with connection.cursor() as cursor:
            cursor.execute(*args)
            connection.commit()


def one(*args):
    with connect(**database_data) as connection:
        with connection.cursor() as cursor:
            cursor.execute(*args)
            res: tuple | None = cursor.fetchone()
            if res is not None and len(res) == 1:
                return res[0]
            else:
                return res


def all(*args):
    with connect(**database_data) as connection:
        with connection.cursor() as cursor:
            cursor.execute(*args)
            res = cursor.fetchall()
            if len(res) != 0 and len(res[0]) == 1:
                res = [item[0] for item in res]
            return res


@never_cache
def show_subjects(request, user_id: int):
    data = one("SELECT data FROM users WHERE user_id = %s" % user_id)
    if data is None:
        return Http404
    data = json.loads(data)
    return render(request, "subjects.html", data)


@never_cache
def show_olympiads(request, user_id: int):
    data = one("SELECT data FROM users WHERE user_id = %s" % user_id)
    if data is None:
        return Http404
    data = json.loads(data)
    user_olympiads = sorted(data["olympiads"])
    cool_olympiads = all("SELECT activity_name, activity_id FROM cool_olympiads")
    context = {
        "user_olympiads": user_olympiads,
        "cool_olympiads": cool_olympiads
    }
    return render(request, "olympiads.html", context)
