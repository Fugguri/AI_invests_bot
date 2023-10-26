from datetime import date
import pymysql
from config import Config
from models import *


class Database:
    def __init__(self, cfg: Config):
        self.cfg: Config = cfg
        self.connection = pymysql.connect(
            host=self.cfg.tg_bot.host,
            user=self.cfg.tg_bot.user,
            port=self.cfg.tg_bot.port,
            password=self.cfg.tg_bot.password,
            database=self.cfg.tg_bot.database,
        )
        self.connection.autocommit(True)

    def cbdt(self):
        with self.connection.cursor() as cursor:
            create = """CREATE TABLE IF NOT EXISTS Users
                        (id INT PRIMARY KEY AUTO_INCREMENT,
                        telegram_id BIGINT UNIQUE NOT NULL ,
                        full_name TEXT,
                        username TEXT,
                        has_access BOOL DEFAULT false,
                        role TEXT DEFAULT 'USER',
                        is_registered TEXT DEFAULT 'Нет',
                        firstname TEXT,
                        last_name TEXT,
                        phone TEXT,
                        organization TEXT,
                        last_activity DATETIME
                        );"""
            cursor.execute(create)
            self.connection.commit()

        with self.connection.cursor() as cursor:
            create = """CREATE TABLE IF NOT EXISTS Categories
                        (id INT PRIMARY KEY AUTO_INCREMENT,
                        name TEXT,
                        description TEXT,
                        use_count BIGINT DEFAULT 0
                        );"""
            cursor.execute(create)
            self.connection.commit()
        with self.connection.cursor() as cursor:
            create = """CREATE TABLE IF NOT EXISTS Channels
                        (id INT PRIMARY KEY AUTO_INCREMENT,
                        channel_id BIGINT,
                        username TEXT,
                        link TEXT,
                        name TEXT,
                        description TEXT,
                        use_count INT DEFAULT 0
                        );"""
            cursor.execute(create)
            self.connection.commit()
        with self.connection.cursor() as cursor:
            create = """CREATE TABLE IF NOT EXISTS Keyboards
                        (id INT PRIMARY KEY AUTO_INCREMENT,
                        text TEXT,
                        category text,
                        callback TEXT, 
                        link text
                        );"""
            cursor.execute(create)
            self.connection.commit()

    def add_user(self, user: User):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO Users (full_name, telegram_id, username,last_activity  ) VALUES (%s, %s, %s, now()) ",
                           (user.full_name, user.id, user.username))
            self.connection.commit()
            self.connection.close()

    def add_category(self, category: Category):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO Categories (name, description, use_count) VALUES (%s,%s,  %s) ",
                           (category.name, category.description, category.use_count))
            self.connection.commit()
            self.connection.close()

    def get_all_categories(self):
        result = []
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM Categories""")
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()
            for category in res:

                result.append(Category(*category))
        return result

    def get_all_users(self)-> [User]:
        result = []
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM Users""")
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()
            for user in res:
                result.append(User(*user))
        return result

    def get_channels(self):
        result = []
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM Channels""")
            res = cursor.fetchall()
            self.connection.commit()
            self.connection.close()
            for user in res:
                result.append(Channel(*user))
        return result

    def get_category(self, name):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM Categories WHERE name=%s""", (name,))
            cat = cursor.fetchone()
            if not cat:
                return False
            cursor.execute(
                """SELECT * FROM Keyboards WHERE category=%s""", (name,))
            keys = cursor.fetchall()
            self.connection.commit()
            self.connection.close()
            category = Category(id=cat[0], name=cat[1], description=cat[2],
                                use_count=cat[3], keyboards=[Keyboard(*key) for key in keys])

        return category

    def update_category_count(self, name):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """UPDATE Categories SET use_count = use_count + 1 WHERE name=%s""", (name,))
            cursor.fetchone()
            self.connection.commit()
            cursor.execute(
                """SELECT * FROM Categories WHERE name=%s""", (name,))
            res = cursor.fetchone()
            self.connection.close()
            user = Category(*res)
        return user

    def update_user_data(self, telegram_id,data:dict):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            
            cursor.execute(
                """UPDATE Users SET 
                  firstname =%s,
                  last_name=%s,
                  phone=%s,
                  organization=%s,
                  is_registered =%s
                WHERE telegram_id=%s""", (data.get("firstname"),data.get("lastname"),data.get("phone"),data.get("organization"),"Да",telegram_id,))

            cursor.fetchone()
            self.connection.commit()

    def update_activity(self, telegram_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """UPDATE Users SET last_activity = now() WHERE telegram_id=%s""", (telegram_id,))
            cursor.fetchone()
            self.connection.commit()

    def get_user(self, telegram_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT *
                FROM Users
                WHERE telegram_id=%s""", (telegram_id,))
            res = cursor.fetchone()
            self.connection.commit()
            self.connection.close()
            user = User(*res)
        return user
    
    def is_user_registered(self, telegram_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT is_registered
                FROM Users
                WHERE telegram_id=%s""", (telegram_id,))
            res = cursor.fetchone()
            print(res)
            if res[0] == "Нет":
                return False
            return True

    def get_users_count(self):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT COUNT(*) FROM Users""")
            res = cursor.fetchone()
        return res[0]


if __name__ == "__main__":
    db = Database()
    from config.config import load_config

    config = load_config("config.json", "texts.yml")
    ch = Category(0, "Maria", "test", "test category", 164, 0)
    db.add_category(ch)
