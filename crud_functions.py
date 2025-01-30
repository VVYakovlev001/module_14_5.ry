import sqlite3

connection = sqlite3.connect("initiate.db")
cursor = connection.cursor()

#cursor.execute('''
#CREATE TABLE IF NOT EXISTS Products(
#id INTEGER PRIMARY KEY,
#title TEXT NOT NULL,
#description TEXT,
#price INTEGER
#);
#''')


#cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?,?,?,?)",
#              ("1","Продукт 1","Описание 1","100"))
#cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?,?,?,?)",
#              ("2","Продукт 2","Описание 2","200"))
#cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?,?,?,?)",              ("3","Продукт 3","Описание 3","300"))
#cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?,?,?,?)",
#              ("4","Продукт 4","Описание 4","400"))

#def get_all_products(id, title, description, price):
#    check_products = cursor.execute("SELECT * FROM Products WHERE id=?", (price,))

 #   if check_products.fetchone() is None:
 #       cursor.execute(f'''
 #   INSERT INTO Products VALUES('{id}','{title}','{description}','{price}',0)
#''')
#    connection.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
);
''')

#cursor.execute("INSERT INTO Users (id, username, email, age,balance) VALUES (?,?,?,?,?)",
#              ("1","user 1","user@com","20","1000"))

def add_user(username, email, age):
    chec_user = cursor.execute("SELECT * FROM Users WHERE id = ?",username)
    balance = 1000
    if chec_user.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Users VALUES('{username}','{email}','{age}','{balance}',0)    
''')
    connection.commit()



connection.commit()
connection.close()

'''
Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи
 SQL запроса. Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
username - текст (не пустой)
email - текст (не пустой)
age - целое число (не пустой)
balance - целое число (не пустой)
add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
 Данная функция должна добавлять в таблицу Users вашей БД запись с переданными
  данными. Баланс у новых пользователей всегда равен 1000. Для добавления записей
   в таблице используйте SQL запрос.
is_included(username) принимает имя пользователя и возвращает True, если такой
 пользователь есть в таблице Users, в противном случае False. Для получения записей
  используйте SQL запрос.
'''