
# - *- coding: utf- 8 - *-
import datetime
import logging
import random
import sqlite3
import time


# Путь к БД
path_to_db = "botBD.sqlite"

def logger(statement):
    logging.basicConfig(
        level=logging.INFO,
        filename="logs.log",
        format=f"[Executing] [%(asctime)s] | [%(filename)s LINE:%(lineno)d] | {statement}",
        datefmt="%d-%b-%y %H:%M:%S"
    )
    logging.info(statement)


def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())

def handle_silently(function):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            logger("{}({}, {}) failed with exception {}".format(
                function.__name__, repr(args[1]), repr(kwargs), repr(e)))
        return result

    return wrapped

# Добавление пользователя
def add_userx(user_id, user_login, user_name, tex, obraschenie, reg_date):
    with sqlite3.connect(path_to_db) as db:
        db.execute("INSERT INTO storage_users "
                   "(user_id, user_login, user_name, tex, obraschenie, reg_date) "
                   "VALUES (?, ?, ?, ?, ?, ?)",
                   [user_id, user_login, user_name, 10, obraschenie, reg_date])
        db.commit()

# Изменение пользователя
def update_userx(user_id, **kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = f"UPDATE storage_users SET XXX WHERE user_id = {user_id}"
        sql, parameters = update_format_with_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()

# Удаление пользователя
def delete_userx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "DELETE FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        db.execute(sql, parameters)
        db.commit()

# Получение пользователя
def get_userx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchone()
    return get_response

# Получение пользователей
def get_usersx(**kwargs):
    with sqlite3.connect(path_to_db) as db:
        sql = "SELECT * FROM storage_users WHERE "
        sql, parameters = get_format_args(sql, kwargs)
        get_response = db.execute(sql, parameters)
        get_response = get_response.fetchall()
    return get_response



# Получение всех пользователей
def get_all_usersx():
    with sqlite3.connect(path_to_db) as db:
        get_response = db.execute("SELECT * FROM storage_users")
        get_response = get_response.fetchall()
    return get_response


def create_bdx():
    with sqlite3.connect(path_to_db) as db:
        # Создание БД с хранением данных пользователей
        check_sql = db.execute("PRAGMA table_info(storage_users)")
        check_sql = check_sql.fetchall()
        check_create_users = [c for c in check_sql]
        if len(check_create_users) == 7:
            print("                        DB был найден (1/8)")
        else:
            db.execute("CREATE TABLE storage_users("
                       "increment INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "user_id INTEGER, user_login TEXT, user_name TEXT, "
                       "tex TEXT, obraschenie TEXT, reg_date TIMESTAMP)")
            print("                        DB не была найдена (1/8) | Создание DB...")


        db.commit()
create_bdx()