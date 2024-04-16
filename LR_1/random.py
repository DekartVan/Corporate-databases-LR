import faker
import uuid
import psycopg2
from psycopg2.extras import register_uuid
from datetime import datetime, timedelta
import random

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="gameApp",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
register_uuid()

# Создание объекта Faker для генерации фальшивых данных
fake = faker.Faker()

# Генерация пользователей
users = []
for i in range(2000):
    user_id = uuid.uuid4()
    username = fake.user_name()
    password = fake.password()
    users.append((user_id, username, password))

# Вставка пользователей в таблицу
cur = conn.cursor()
cur.executemany("INSERT INTO \"user\" (user_id, username, password) VALUES (%s, %s, %s)", users)
conn.commit()

# Генерация профилей пользователей
profiles = []
for user in users:
    profile_id = uuid.uuid4()
    email = fake.email()
    phone_number = fake.phone_number()
    profiles.append((profile_id, email, phone_number, user[0]))

# Вставка профилей в таблицу
cur.executemany("INSERT INTO profile (profile_id, email, phone_number, user_id) VALUES (%s, %s, %s, %s)", profiles)
conn.commit()

# Генерация игр
apps = []
genres = ['Action', 'Adventure', 'Puzzle', 'Strategy', 'Simulation', 'RPG']
for i in range(500):
    game_id = uuid.uuid4()
    title = fake.text(64)
    genre = random.choice(genres)
    number_of_sales = random.randint(1000, 1000000)
    price = round(random.uniform(0.99, 59.99), 2)
    developer = fake.company()
    apps.append((game_id, title, genre, number_of_sales, price, developer))

# Вставка игр в таблицу
cur.executemany("INSERT INTO game (game_id, title, genre, number_of_sales, price, developer) VALUES (%s, %s, %s, %s, %s, %s)", apps)
conn.commit()

# Генерация отзывов
feedback = []
for user in users:
    for _ in range(random.randint(1, 5)):
        feedback_id = uuid.uuid4()
        text = fake.text()
        stars = random.randint(1, 5)
        game_id = random.choice([app[0] for app in apps])
        feedback.append((feedback_id, text, stars, user[0], game_id))

# Вставка отзывов в таблицу
cur.executemany("INSERT INTO feedback (feedback_id, text, stars, user_id, game_id) VALUES (%s, %s, %s, %s, %s)", feedback)
conn.commit()

# Генерация сессий
sessions = []
for _ in range(3000000):
    session_id = uuid.uuid4()
    start_session = fake.date_time_between(start_date='-1y', end_date='now')
    end_session = start_session + timedelta(minutes=random.randint(1, 120))
    user_id = random.choice([user[0] for user in users])
    game_id = random.choice([app[0] for app in apps])
    sessions.append((session_id, start_session, end_session, user_id, game_id))

# Вставка сессий в таблицу
cur.executemany("INSERT INTO session (session_id, start_session, end_session, user_id, game_id) VALUES (%s, %s, %s, %s, %s)", sessions)
conn.commit()

# Закрытие соединения
cur.close()
conn.close()
