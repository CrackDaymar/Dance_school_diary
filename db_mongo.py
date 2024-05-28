import pymongo

host = 'localhost'
port = 27017
client = pymongo.MongoClient(host, port)
# Выберите базу данных
db = client['Primakova']
collections_holls = db['holls']
collections_training = db['training']
collections_trainer = db['trainer']


def add_trainer(name_teacher, dance_direction, id_teacher):
    add_contant = {
        'name teacher': name_teacher,
        'dance direction': dance_direction,
        'telegram id teacher': id_teacher
    }

    collections_trainer.insert_one(add_contant)


def get_teacher(telegram_id):
    query = {'telegram id teacher': {'$gte': telegram_id}}
    data = collections_trainer.find(query)
    for dat in data:
        return dat['name teacher'], dat['dance direction']


def add_training(date_workout, telegram_id):
    name_teacher, dance_direction = get_teacher(telegram_id)
    add_container = {
        'date training': date_workout,
        'name teacher': name_teacher,
        'dance direction': dance_direction
    }


def add_white_list(id_telegram):
    pass



