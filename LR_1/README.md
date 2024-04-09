# Лабораторная работа №1 
Выполнил студент группы 6133-010402D Гудков Сергей

Выбранная мной предметная область - онлайн сервис распространения игр и ПО.

Приведём ER-диаграмму базы данных и опишем её более детально:
![ER drawio](https://github.com/DekartVan/Corporate-databases-LR/assets/60447026/77360c53-76c9-4887-a38d-3c297650e9f3)
1. User:
   - user_id (PK): INT (автоинкремент) - уникальный идентификатор пользователя.
   - first_name: VARCHAR (не может быть NULL) - имя пользователя.
   - last_name: VARCHAR (не может быть NULL) - фамилия пользователя.
   - phone_number: VARCHAR (не может быть NULL) - номер телефона пользователя.

2. Profile:
   - profile_id (PK): INT (автоинкремент) - уникальный идентификатор профиля пользователя.
   - username: VARCHAR (не может быть NULL) - никнейм пользователя на платформе.
   - email: VARCHAR (не может быть NULL) - почта пользователя платформы.
   - password: VARCHAR (не может быть NULL) - пароль пользователя платформы.
   - user_id (FK): INT (внешний ключ) - ссылка на user_id в таблице User.

3. Game:
   - game_id (PK): INT (автоинкремент) - уникальный идентификатор игры.
   - title: VARCHAR (не может быть NULL) - название игры.
   - genre: VARCHAR (не может быть NULL) - жанр игры.
   - number_of_sales: INTEGER (не может быть NULL) - количество продаж игры.
   - price: DECIMAL (не может быть NULL) - цена игры.
   - developer: VARCHAR (не может быть NULL) - разработчик игры.

4. Feedback:
   - feedback_id (PK): INT (автоинкремент) - уникальный идентификатор отзыва.
   - text: TEXT (может быть NULL) - текстовый отзыв о игре.
   - stars: INTEGER (не может быть NULL) - количество звёзд, выставленные пользователями игре.

5. Session:
   - session_id (PK): INT (автоинкремент) - уникальный идентификатор сессии.
   - start_session: TIMESTAMP (не может быть NULL) - время начала сессии.
   - end_session: TIMESTAMP (не может быть NULL) - время окончания сессии.
   - user_id (FK): INT (внешний ключ) - ссылка на user_id в таблице User.

6. User_Feedback_Game (Таблица-связь для связи N-M):
   - user_id (FK): INT (внешний ключ) - ссылка на user_id в таблице User.
   - feedback_id (FK): INT (внешний ключ) - ссылка на feedback_id в таблице Feedback.
   - game_id (FK): INT (внешний ключ) - ссылка на game_id в таблице Game.

Опишем связи между всеми сущностями нашей ER-диаграммы:
Связи:
Связи:
- User-Profile: 1-1 связь между сущностями User и Profile. Каждый пользователь имеет только один профиль, и каждый профиль принадлежит только одному пользователю.
- User-Feedback: 1-N связь между сущностями User и Feedback. Каждый пользователь может оставить несколько отзывов, но каждый отзыв принадлежит только одному пользователю.
- Game-Feedback: 1-N связь между сущностями Game и Feedback. Каждая игра может иметь много отзывов, но каждый отзыв относится только к одной игре.
- User-Session: 1-N связь между сущностями User и Session. Каждый пользователь может иметь несколько сессий, но каждая сессия принадлежит только одному пользователю.
- User-Game: N-M связь между сущностями User и Game. Каждый пользователь может иметь много игр, и каждая игра может принадлежать нескольким пользователям.
- User_Feedback_Game: Таблица-связь для связи N-M между сущностями User, Feedback и Game. Каждый пользователь может оставить отзывы для нескольких игр, и каждая игра может иметь отзывы от нескольких пользователей.

## Далее по ER диаграмме в PgAdmin автоматически был создан SQL-скрипт: 
```SQL
BEGIN;

CREATE TABLE IF NOT EXISTS public."user"
(
    user_id uuid NOT NULL,
    first_name character varying(32) NOT NULL,
    last_name character varying(32) NOT NULL,
    phone_number character varying(12) NOT NULL,
    CONSTRAINT pk_user_id PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS public.profile
(
    profile_id uuid NOT NULL,
    username character varying(32) NOT NULL,
    email character varying(40) NOT NULL,
    password character varying(64) NOT NULL,
    user_id uuid,
    CONSTRAINT pk_profile_id PRIMARY KEY (profile_id)
);

CREATE TABLE IF NOT EXISTS public.session
(
    session_id uuid NOT NULL,
    start_session timestamp without time zone NOT NULL,
    end_session timestamp without time zone NOT NULL,
    user_id uuid NOT NULL,
    CONSTRAINT pk_session_id PRIMARY KEY (session_id)
);

CREATE TABLE IF NOT EXISTS public.feedback
(
    feedback_id uuid,
    text text NOT NULL,
    stars smallint NOT NULL,
    PRIMARY KEY (feedback_id)
);

CREATE TABLE IF NOT EXISTS public.game
(
    game_id uuid,
    title character varying(64) NOT NULL,
    genre character varying(32) NOT NULL,
    number_of_sales integer NOT NULL,
    price real NOT NULL,
    developer character varying NOT NULL,
    CONSTRAINT pk_game_id PRIMARY KEY (game_id)
);

CREATE TABLE IF NOT EXISTS public.game_user
(
    game_id uuid,
    user_id uuid NOT NULL,
    feedback_id uuid NOT NULL
);

ALTER TABLE IF EXISTS public.profile
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id)
    REFERENCES public."user" (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.session
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES public."user" (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.game_user
    ADD FOREIGN KEY (game_id)
    REFERENCES public.game (game_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.game_user
    ADD FOREIGN KEY (user_id)
    REFERENCES public."user" (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.game_user
    ADD FOREIGN KEY (feedback_id)
    REFERENCES public.feedback (feedback_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;
```

## Далее создадим индексы к столбцам таблиц:

 Индекс для столбца user_id в таблице "user"
```SQL
CREATE INDEX IF NOT EXISTS idx_user_user_id
    ON public.user USING btree
    (user_id)
    TABLESPACE pg_default;
```

 Индекс для столбца username в таблице profile
```SQL
CREATE INDEX IF NOT EXISTS idx_profile_username
    ON public.profile USING btree
    (username)
    TABLESPACE pg_default;
```

 Индекс для столбца user_id в таблице session
```SQL
CREATE INDEX IF NOT EXISTS idx_session_user_id
    ON public.session USING btree
    (user_id)
    TABLESPACE pg_default;
```

 Индекс для столбца feedback_id в таблице feedback
```SQL
CREATE INDEX IF NOT EXISTS idx_feedback_feedback_id
    ON public.feedback USING btree
    (feedback_id)
    TABLESPACE pg_default;
```

 Индекс для столбца game_id в таблице game
```SQL
CREATE INDEX IF NOT EXISTS idx_game_game_id
    ON public.game USING btree
    (game_id)
    TABLESPACE pg_default;
```

 Индекс для столбца user_id в таблице game_user
```SQL
CREATE INDEX IF NOT EXISTS idx_game_user_user_id
    ON public.game_user USING btree
    (user_id)
    TABLESPACE pg_default;
```

 Индекс для столбца game_id в таблице game_user
```SQL
CREATE INDEX IF NOT EXISTS idx_game_user_game_id
    ON public.game_user USING btree
    (game_id)
    TABLESPACE pg_default;
```

 Индекс для столбца feedback_id в таблице game_user
```SQL
CREATE INDEX IF NOT EXISTS idx_game_user_feedback_id
    ON public.game_user USING btree
    (feedback_id)
    TABLESPACE pg_default;
```

## Разработаем типовые запросы к СУБД:
1. Получение данных для авторизации пользователей, у которых количество приобретенных игр больше среднего:
```SQL
SELECT username, password
FROM "user"
WHERE user_id IN (
    SELECT user_id
    FROM game_user
    GROUP BY user_id
    HAVING COUNT(*) > (
        SELECT AVG(Counted)
        FROM (
            SELECT user_id, COUNT(*) AS Counted
            FROM game_user
            GROUP BY user_id
        ) AS SubQuery
    )
);
```
2. Получить жанр игр, для которых было выполнено наибольшее количество покупок, и количество этих игр:
```SQL
SELECT genre, COUNT(DISTINCT game_id)
FROM game
JOIN game_user ON game.game_id = game_user.game_id
GROUP BY game.genre
HAVING COUNT(*) = (
    SELECT MAX(Counted)
    FROM (
        SELECT COUNT(*) AS Counted
        FROM game
        JOIN game_user ON game.game_id = game_user.game_id
        GROUP BY game.genre
    ) AS SubQuery
);
```
3. Получить электронную почту пользователей, которые оставили наибольшее количество негативных отзывов (с одной звездой) играм в жанре с наивысшим средним рейтингом:
```SQL
SELECT email FROM profile WHERE user_id IN (
    SELECT user_id
    FROM (
        SELECT user_id, COUNT(stars) AS Counted_Stars
        FROM feedback
        JOIN game ON feedback.game_id = game.game_id
        WHERE stars = 1 AND genre = (
            SELECT genre FROM feedback
            JOIN game ON feedback.game_id = game.game_id
            GROUP BY genre
            HAVING AVG(stars) = (
                SELECT MAX(mean) FROM (
                    SELECT genre, AVG(stars) AS mean 
                    FROM feedback
                    JOIN game ON feedback.game_id = game.game_id
                    GROUP BY genre
                ) AS SubQuery
            )
        )
        GROUP BY user_id
    ) AS SubQuery2
    WHERE Counted_Stars = (
        SELECT MAX(Counted_Stars) FROM (
            SELECT user_id, COUNT(stars) AS Counted_Stars
            FROM feedback
            JOIN game ON feedback.game_id = game.game_id
            WHERE stars = 1 AND genre = (
                SELECT genre FROM feedback
                JOIN game ON feedback.game_id = game.game_id
                GROUP BY genre
                HAVING AVG(stars) = (
                    SELECT MAX(mean) FROM (
                        SELECT genre, AVG(stars) AS mean 
                        FROM feedback
                        JOIN game ON feedback.game_id = game.game_id
                        GROUP BY genre
                    ) AS SubQuery
                )
            )
            GROUP BY user_id
        ) AS SubQuery3
    )
);
```
4. Получить средний рейтинг каждого жанра игр, учитывая только те игры, у которых количество покупок ниже среднего и для которых был выполнен хотя бы один вход в течение последней недели:
```SQL
SELECT genre, AVG(stars)
FROM game
JOIN feedback ON game.game_id = feedback.game_id
WHERE game.game_id IN (
    SELECT game_id
    FROM game_user
    WHERE game_id IN (
        SELECT game_id
        FROM game_user
        WHERE game_id IN (
            SELECT game_id
            FROM game
            JOIN session ON game.game_id = session.game_id
            WHERE session.start_session BETWEEN CURRENT_DATE - INTERVAL '1 week' AND CURRENT_DATE
        )
        GROUP BY game_id
        HAVING COUNT(user_id) < (
            SELECT AVG(Counted)
            FROM (
                SELECT game_id, COUNT(user_id) AS Counted
                FROM game_user
                GROUP BY game_id
            ) AS SubQuery
        )
    )
)
GROUP BY genre;
```
5. Получить название игр(ы), у которой(-ых) суммарное время всех сессий максимально:
```SQL
SELECT title
FROM game
WHERE game_id IN (
    SELECT game_id
    FROM (
        SELECT game_id, SUM(EXTRACT(EPOCH FROM (end_session - start_session)) / 3600) AS time_in_game
        FROM session
        GROUP BY game_id
    ) AS SubQuery
    WHERE time_in_game = (
        SELECT MAX(time_in_game) FROM (
            SELECT game_id, SUM(EXTRACT(EPOCH FROM (end_session - start_session)) / 3600) AS time_in_game
            FROM session
            GROUP BY game_id
        ) AS MaxSubQuery
    )
);
```
