import sqlite3
from loguru import logger
import datetime

logger.add('info.log', format="{time} {level} {message}",
           level='INFO', rotation="10KB", compression='zip')


# conn = psycopg2.connect(**connections_params)
# cursor = conn.cursor()
#
# sql = "INTO frosthaven (id serial primary key,name varchar, name_player varchar, gold int, exp int, level int )"
# cursor.execute(sql)
# conn.commit()


def db_connection_teacher(func):
    def wrapper(*args, **kwargs):
        # Установить соединение с базой данных
        conn = sqlite3.connect('teachers.db')
        cursor = conn.cursor()

        # Вызвать функцию с переданными аргументами
        result = func(cursor, *args, **kwargs)

        # Применить изменения и закрыть соединение
        conn.commit()
        cursor.close()
        conn.close()

        return result

    return wrapper


def db_connection_workouts(func):
    def wrapper(*args, **kwargs):
        # Установить соединение с базой данных
        conn = sqlite3.connect('workouts.db')
        cursor = conn.cursor()

        # Вызвать функцию с переданными аргументами
        result = func(cursor, *args, **kwargs)

        # Применить изменения и закрыть соединение
        conn.commit()
        cursor.close()
        conn.close()

        return result

    return wrapper


@db_connection_teacher
def get_dance_direction(cursor, id_teacher):
    sql = f'''
    SELECT dance_direction FROM teachers WHERE id_teacher = {id_teacher}
    '''

    cursor.execute(sql)
    data = cursor.fetchall()

    return data


@db_connection_teacher
def get_name_teacher(cursor, id_teacher):
    sql = f'''
    SELECT name_teacher FROM teachers WHERE id_teacher = {id_teacher}
    '''

    cursor.execute(sql)
    data = cursor.fetchall()

    return data


@db_connection_teacher
def create_table_teacher(cursor):
    sql = '''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY,
                name_teacher varchar,
                dance_direction VARCHAR,
                id_telegram VARCHAR                
            )
        '''

    cursor.execute(sql)


@db_connection_workouts
def create_table_workouts(cursor):
    sql = '''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY,
                name_teacher VARCHAR,
                id_teacher VARCHAR,
                dance_direction VARCHAR,
                date_workout DATE,
                hole VARCHAR,
                type_workout VARCHAR,
                replacement VARCHAR                           
            )
        '''

    cursor.execute(sql)


@db_connection_teacher
def add_workout(cursor, id_teacher, date_workout, hole, type_workout, replacement):
    create_table_workouts()
    insert_query = '''
            INSERT INTO messages (name_teacher,id_teacher, dance_direction, date_workout, hole, type_workout, 
            replacement)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
    dance_direction = get_dance_direction(id_teacher)
    name_teacher = get_name_teacher(id_teacher)
    data = (name_teacher, id_teacher, dance_direction, date_workout, hole, type_workout, replacement)
    cursor.execute(insert_query, data)


@db_connection_teacher
def add_teacher(cursor, name_teacher, dance_direction, id_teacher):
    create_table_teacher()
    insert_query = '''
                INSERT INTO messages (name_teacher,dance_direction, id_telegram)
                VALUES (?, ?, ?)
            '''
    data = (name_teacher, dance_direction, id_teacher)
    cursor.execute(insert_query, data)


@db_connection_teacher
def get_all_teacher(cursor):
    sql = """
    SELECT * FROM teachers
    """

    cursor.execute(sql)
    data = cursor.fetchall()

    return data


@db_connection_workouts
def get_all_workouts(cursor, date):
    sql = f"""
    SELECT * FROM workouts WHERE date_workout = {date}
    """

    cursor.execute(sql)
    data = cursor.fetchall()

    return data


@db_connection_workouts
def check_and_schedule_training(cursor, date_time_str, trainer_name):
    # Преобразуем строку с датой и временем в объект datetime
    try:
        date_time = datetime.datetime.strptime(date_time_str, '%d.%m.%Y %H:%M')
    except ValueError:
        return "Некорректный формат даты и времени. Используйте формат ДД.ММ.ГГГГ ЧЧ:ММ."

    # Проверяем наличие тренировок на указанное время и в течение часа
    start_time = date_time - datetime.timedelta(hours=1)
    end_time = date_time + datetime.timedelta(hours=1)

    cursor.execute('''
        SELECT date FROM training_dates
        WHERE trainer = ? AND date BETWEEN ? AND ?
    ''', (trainer_name, start_time, end_time))

    existing_trainings = cursor.fetchall()

    if existing_trainings:
        # Если есть тренировки, возвращаем информацию о них
        return f"На {date_time_str} есть следующие тренировки с тренером {trainer_name}:\n" + \
               '\n'.join([existing[0].strftime('%H:%M') for existing in existing_trainings])
    else:
        # Если нет тренировок, то записываем новую
        cursor.execute('INSERT INTO training_dates (date, trainer) VALUES (?, ?)', (date_time, trainer_name))
        return f"Тренировка с тренером {trainer_name} на {date_time_str} успешно записана."

# Пример использования функции
result = check_and_schedule_training("18.09.2023 14:30", "Имя вашего тренера")
print(result)