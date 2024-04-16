# Лабораторная работа №1 
Выполнил студент группы 6133-010402D Гудков Сергей

Выбранная мной предметная область - онлайн магазин книг.

Приведём ER-диаграмму базы данных и опишем её более детально:
![изображение](https://github.com/DekartVan/Corporate-databases-LR/assets/60447026/27608437-9564-4996-ace2-858edbc1f853)

В центре внимания книги, у каждой из которых есть автор или некоторое количество авторов (связь N:M), также каждая книга физически находится на некотором складе, на этом складе может как содержаться множество одинаковых книг, так и те же самые книги могут храниться на разных складах (связь N:M). Также у складов есть контактное лицо, которое представляет склад (связь 1:1). У каждой книги есть один основной жанр (связь 1:M). Также магазин закупает свои книги у нескольких конкретных издательств, и каждая книга представлена только одним издательством (связь 1:M).
Или короче:
- Одна книга принадлежит одному издателю (один-ко-многим).
- Одна книга относится к одному жанру (один-ко-многим).
- Один автор может написать много книг, и каждая книга может иметь много авторов (многие-ко-многим).
- Одна книга может храниться на многих складах, и на каждом складе может быть много книг (многие-ко-многим).
- Каждый склад имеет своё контактное лицо (один-ко-одному).

---------

Далее приведу скрипт SQL-скрипта для создания данной Базы Даннных: 

```SQL
BEGIN;

-- Создание таблицы book
CREATE TABLE IF NOT EXISTS public.book
(
    book_id integer,
    title character varying(128) NOT NULL,
    genre character varying(64) NOT NULL,
    rating smallint,
    author character varying(64) NOT NULL,
    price real NOT NULL,
    num_sales integer,
    fk_publisher_id integer NOT NULL,
    fk_genre_id integer NOT NULL,
    CONSTRAINT pk_book_id PRIMARY KEY (book_id)
);

-- Создание таблицы publisher
CREATE TABLE IF NOT EXISTS public.publisher
(
    publisher_id integer,
    name character varying(128) NOT NULL,
    city character varying(64) NOT NULL,
    adress character varying(128) NOT NULL,
    contact_phone character varying(64) NOT NULL,
    purpose character varying(64) NOT NULL,
    ownership character varying(64) NOT NULL,
    CONSTRAINT pk_publisher_id PRIMARY KEY (publisher_id)
);

-- Создание таблицы author
CREATE TABLE IF NOT EXISTS public.author
(
    author_id integer,
    last_name character varying(64) NOT NULL,
    first_name character varying(64) NOT NULL,
    rating smallint,
    CONSTRAINT pk_author_id PRIMARY KEY (author_id)
);

-- Создание таблицы warehouse
CREATE TABLE IF NOT EXISTS public.warehouse
(
    warehouse_id integer,
    city character varying(64) NOT NULL,
    adress character varying(128) NOT NULL,
    size "char" NOT NULL,
    fk_contact integer NOT NULL,
    PRIMARY KEY (warehouse_id)
);

-- Создание таблицы warehouse_contact_person
CREATE TABLE IF NOT EXISTS public.warehouse_contact_person
(
    warehouse_contact_person_id integer,
    last_name character varying(64) NOT NULL,
    first_name character varying(64) NOT NULL,
    num_phone character varying(64) NOT NULL,
    sex "char" NOT NULL,
    CONSTRAINT pk_warehouse_contact_person_id PRIMARY KEY (warehouse_contact_person_id)
);

-- Создание таблицы genre
CREATE TABLE IF NOT EXISTS public.genre
(
    genre_id integer,
    name character varying(64) NOT NULL,
    description text NOT NULL,
    CONSTRAINT pk_genre_id PRIMARY KEY (genre_id)
);


-- Создание связующей таблицы book_auyhor
CREATE TABLE IF NOT EXISTS public.book_author
(
    book_book_id integer,
    author_author_id integer
);

-- Создание связующей таблицы book_warehouse
CREATE TABLE IF NOT EXISTS public.book_warehouse
(
    book_book_id integer,
    warehouse_warehouse_id integer
);

-- Добавление вторичного ключа (создание связи с таблицей publisher 1:M)
ALTER TABLE IF EXISTS public.book
    ADD CONSTRAINT fk_publisher_book_id FOREIGN KEY (fk_publisher_id)
    REFERENCES public.publisher (publisher_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

-- Добавление вторичного ключа (создание связи с таблицей genre 1:M)
ALTER TABLE IF EXISTS public.book
    ADD CONSTRAINT fk_genre_book_id FOREIGN KEY (fk_genre_id)
    REFERENCES public.genre (genre_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

-- Добавление вторичного ключа (создание связи warehouse с таблицей warehouse_contact_person_id 1:1)
	  ADD CONSTRAINT fk_contact_id_key UNIQUE (fk_contact),
    ADD CONSTRAINT fk_contact_warehouse_id FOREIGN KEY (fk_contact)
    REFERENCES public.warehouse_contact_person (warehouse_contact_person_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

-- Добавление вторичного ключа в связующую таблицу
ALTER TABLE IF EXISTS public.book_author
    ADD FOREIGN KEY (book_book_id)
    REFERENCES public.book (book_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

-- Добавление вторичного ключа в связующую таблицу
ALTER TABLE IF EXISTS public.book_author
    ADD FOREIGN KEY (author_author_id)
    REFERENCES public.author (author_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

-- Добавление вторичного ключа в связующую таблицу
ALTER TABLE IF EXISTS public.book_warehouse
    ADD FOREIGN KEY (book_book_id)
    REFERENCES public.book (book_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

-- Добавление вторичного ключа в связующую таблицу
ALTER TABLE IF EXISTS public.book_warehouse
    ADD FOREIGN KEY (warehouse_warehouse_id)
    REFERENCES public.warehouse (warehouse_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;
```
---------

Для всех колонок, которые могут использоваться для поиска данных - создадим индексы для ускорения процесса поиска и сортировки:
```SQL
-- Индексы для таблицы "book"
CREATE INDEX idx_book_title ON public.book (title);
CREATE INDEX idx_book_genre ON public.book (genre);
CREATE INDEX idx_book_author ON public.book (author);
CREATE INDEX idx_book_price ON public.book (price);
CREATE INDEX idx_book_rating ON public.book (rating);

-- Индексы для таблицы "publisher"
CREATE INDEX idx_publisher_name ON public.publisher (name);

-- Индексы для таблицы "author"
CREATE INDEX idx_author_last_name ON public.author (last_name);
CREATE INDEX idx_author_first_name ON public.author (first_name);

-- Индексы для таблицы "warehouse"
CREATE INDEX idx_warehouse_city ON public.warehouse (city);

-- Индексы для таблицы "warehouse_contact_person"
CREATE INDEX idx_contact_person_last_name ON public.warehouse_contact_person (last_name);
CREATE INDEX idx_contact_person_first_name ON public.warehouse_contact_person (first_name);

-- Индексы для таблицы "genre"
CREATE INDEX idx_genre_name ON public.genre (name);

```

---------
Разработаем 5 типовых запросов к Базе данных:

**Выборка книг определенного жанра с наибольшим количеством продаж:**
```SQL
SELECT b.title, b.num_sales
FROM public.book b
JOIN public.genre g ON b.fk_genre_id = g.genre_id
WHERE g.name = 'Adventure'
ORDER BY b.num_sales DESC;
```

**Выборка книг с самым высоким рейтингом:**
```SQL
SELECT title, rating
FROM public.book
WHERE rating = (SELECT MAX(rating) FROM public.book);
```

**Выборка всех книг, доступных на определенном складе:**
```SQL
SELECT b.title, b.price
FROM public.book b
JOIN public.book_warehouse bw ON b.book_id = bw.book_book_id
JOIN public.warehouse w ON bw.warehouse_warehouse_id = w.warehouse_id
WHERE w.city = 'Geraldside';
```

**Выборка всех авторов и их средний рейтинг:**
```SQL
SELECT a.last_name, a.first_name, AVG(b.rating) AS avg_rating
FROM public.author a
JOIN public.book_author ba ON a.author_id = ba.author_author_id
JOIN public.book b ON ba.book_book_id = b.book_id
GROUP BY a.last_name, a.first_name;
```

**Выборка издателей и количество книг, которые они издали:**
```SQL
SELECT p.name, COUNT(b.book_id) AS num_books_published
FROM public.publisher p
JOIN public.book b ON p.publisher_id = b.fk_publisher_id
GROUP BY p.name;
```

---------
Займёмся наполнение базы данных. Для этого воспользуемся Python. Числовые данные будем генерировать с помощью функция библиотеки random, текстовые с помощью библиотеки faker. Скрипт наполнения базы данных принял следуйщий вид: 
```Python
# Импорт библиотек
import faker 
import psycopg2
from datetime import datetime, timedelta
import random

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="bookstore",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Создание объекта Faker для генерации фальшивых данных
fake = faker.Faker()

# Жанры книг
genres = ['Science Fiction', 'Mystery', 'Romance', 'Adventure', 'Fantasy', 'Horror', 'Drama', 'Poetry', 'Popular Science', 'Historical Fiction', 'Biography', 'Thriller', 'Psychology', 'Philosophy', 'Classics', 'Non-fiction', 'Humor', 'Travel Guides', 'Self-help', 'Memoirs']

# Заполнение таблицы "genre"
for idx, genre in enumerate(genres, start=1):
    cur.execute("INSERT INTO public.genre (genre_id, name, description) VALUES (%s, %s, %s)", (idx, genre, f"Description for {genre}"))
conn.commit()

# Генерация авторов книг
authors = []
for i in range(1, 20001):  # Генерация 2000 авторов
    last_name = fake.last_name()
    first_name = fake.first_name()
    rating = random.randint(1, 10)
    authors.append((i, last_name, first_name, rating))
# Заполнение таблицы "author"
cur.executemany("INSERT INTO public.author (author_id, last_name, first_name, rating) VALUES (%s, %s, %s, %s)", authors)
conn.commit()

# Генерация издателей
publishers = []
for i in range(1, 1001):  # Генерация 50 издателей
    name = fake.company()
    city = fake.city()
    address = fake.address()
    contact_phone = fake.phone_number()
    purpose = fake.word()
    ownership = random.choice(['Public', 'Private'])
    publishers.append((i, name, city, address, contact_phone, purpose, ownership))
# Заполнение таблицы "publisher"
cur.executemany("INSERT INTO public.publisher (publisher_id, name, city, adress, contact_phone, purpose, ownership) VALUES (%s, %s, %s, %s, %s, %s, %s)", publishers)
conn.commit()

# Генерация контактных лиц складов
existing_warehouse_contacts = [i for i in range(1, 1501)]  # Существующие контактные лица складов
warehouse_contacts = []
for i in range(1, 1501):  # Генерация 100 контактных лиц складов
    contact_id = existing_warehouse_contacts.pop(random.randint(0, len(existing_warehouse_contacts) - 1))
    last_name = fake.last_name()
    first_name = fake.first_name()
    num_phone = fake.phone_number()
    sex = random.choice(['M', 'F'])
    warehouse_contacts.append((contact_id, last_name, first_name, num_phone, sex))
# Заполнение таблицы "warehouse_contact_person"
cur.executemany("INSERT INTO public.warehouse_contact_person (warehouse_contact_person_id, last_name, first_name, num_phone, sex) VALUES (%s, %s, %s, %s, %s)", warehouse_contacts)
conn.commit()

# Генерация складов
warehouses = []
for i in range(1, 1500):  # Генерация 1500 складов
    city = fake.city()
    address = fake.address()
    size = random.choice(['S', 'M', 'L'])
    fk_contact = random.randint(1, 1501)  # Ссылка на контактное лицо склада
    warehouses.append((i, city, address, size, fk_contact))
# Заполнение таблицы "warehouse"
cur.executemany("INSERT INTO public.warehouse (warehouse_id, city, adress, size, fk_contact) VALUES (%s, %s, %s, %s, %s)", warehouses)
conn.commit()

# Генерация книг
books = []
for i in range(1, 5000001):  # Генерация 5000000 книг
    title = fake.text(max_nb_chars=128)
    genre = random.choice(genres)
    rating = random.randint(1, 10)
    author = fake.name()
    price = round(random.uniform(5.99, 99.99), 2)
    num_sales = random.randint(100, 1000000)
    publisher_id = random.randint(1, 50)  # Ссылка на издателя книги
    author_id = random.randint(1, 200)  # Ссылка на автора книги
    books.append((i, title, genre, rating, author, price, num_sales, publisher_id, genres.index(genre) + 1))
# Заполнение таблицы "book"
cur.executemany("INSERT INTO public.book (book_id, title, genre, rating, author, price, num_sales, fk_publisher_id, fk_genre_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", books)
conn.commit()

# Генерация связей книг с авторами
book_authors = []
for i in range(1, 5000001):  # Генерация 5000000 связей книг с авторами
    book_id = random.randint(1, 5000001)
    author_id = random.randint(1, 20000)
    book_authors.append((book_id, author_id))
# Заполнение таблицы "book_author"
cur.executemany("INSERT INTO public.book_author (book_book_id, author_author_id) VALUES (%s, %s)", book_authors)
conn.commit()

# Генерация связей книг с складами
book_warehouses = []
for i in range(1, 5000000):  # Генерация 5000000 связей книг с складами
    book_id = random.randint(1, 5000000)
    warehouse_id = random.randint(1, 1499)
    book_warehouses.append((book_id, warehouse_id))
# Заполнение таблицы "book_warehouse"
# Заполнение таблицы "book_warehouse"
cur.executemany("INSERT INTO public.book_warehouse (book_book_id, warehouse_warehouse_id) VALUES (%s, %s)", book_warehouses)
conn.commit()

# Закрытие соединения
cur.close()
conn.close()
```
---------
### Оптимизация скорости выполнения запросов к Базе Данным
Посмотрим на время выполнения каждого из запросов:

|Номер запроса|1|2|3|4|5|
|-------------|-|-|-|-|-|
|Время выполнения, мс|2882|7091|333|5122|1052|

По данным таблицы видно, что второй и четвёртый запросы обрабатываются дольше всего. Это и попробуем оптимизировать. 

Для начала поигаремся с настройками сервера. Для оптимизации запросов в PostgreSQL внесём изменения в настройки базы данных, они будут влиять на производительность выполнения запросов. Вот несколько ключевых параметров, которые можно настроить для улучшения производительности:

- shared_buffers:
Этот параметр определяет количество памяти, выделенной для кэширования данных в оперативной памяти. Увеличение этого параметра может улучшить производительность запросов, так как больше данных будет храниться в памяти и не будет требовать чтения с диска.
- work_mem:
Определяет количество памяти, выделенной для операций сортировки и хэширования в рамках одного сеанса. Увеличение этого параметра может ускорить выполнение операций сортировки и хэширования, но следует учитывать, что это может увеличить использование памяти для каждого соединения.
- effective_cache_size:
Определяет оценочный объем кэша файловой системы и оперативной памяти, доступной для PostgreSQL. Установка этого параметра на корректное значение может помочь PostgreSQL принимать более эффективные решения о том, какие данные кэшировать в памяти.

|Эксперимент|Запрос 1 (мс)|Запрос 2 (мс)|Запрос 3 (мс)|Запрос 4 (мс)|Запрос 5 (мс)|shared_buffers (MB)|work_mem (MB)|effective_cache_size (GB)|
|-----------|--------|--------|--------|--------|--------|----------------|------------------|-------------|
|0|905|1611|373|5414|1040|128|4|4|
|1|922|1692|356|7918|1060|128|4|2|
|2|945|1623|496|10555|1138|128|4|1|
|3|849|1612|353|5518|1016|128|8|4|
|4|819|1716|401|10568|1174|1024|8|4|
|5|815|1648|351|5300|1125|4096|8|4|
|6|911|1620|440|5215|1115|4096|4|4|

- Зависимость от размера shared_buffers:
При увеличении размера shared_buffers с 128 MB до 4096 MB время выполнения запросов немного сокращается или остается примерно одинаковым. Однако при максимальном значении shared_buffers (1024 MB) время выполнения некоторых запросов увеличивается, что может свидетельствовать о неоптимальном использовании ресурсов.

- Зависимость от размера work_mem:
Увеличение размера work_mem с 4 MB до 8 MB приводит к снижению времени выполнения запросов в большинстве случаев. Особенно заметно ускорение для запросов 1 и 3.

- Зависимость от размера effective_cache_size:
Изменения в размере effective_cache_size не оказывают значительного влияния на время выполнения запросов в рамках проведенных экспериментов.

Выводы:
- Наилучшая производительность была достигнута при размере shared_buffers 4096 MB, work_mem 8 MB и effective_cache_size 4 GB.
- Увеличение размера shared_buffers и work_mem способствует улучшению производительности, однако следует избегать излишне больших значений, чтобы избежать неэффективного использования ресурсов.
