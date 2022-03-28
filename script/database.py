import sqlite3

def insert_bot_user(chat_id, name):
    db_connection = sqlite3.connect('feed_reader.db')
    db_cursor = db_connection.cursor()
    # Check User is Exist Or Not
    user = db_cursor.execute("""SELECT ChatId FROM BotUsers WHERE ChatId = (?) LIMIT 1""", (chat_id,)).fetchone()
    # Insert New User
    if not user:
        try:
            db_cursor.execute("""INSERT INTO BotUsers (ChatId, name) VALUES (?, ?)""", (chat_id, name))
        except sqlite3.Error as error:
            print(error)
            pass
    # Close DB Connection
    db_connection.commit()
    db_connection.close()

def insert_rss_link(chat_id, link):
    db_connection = sqlite3.connect('feed_reader.db')
    db_cursor = db_connection.cursor()
    # Check User is Exist Or Not
    user = db_cursor.execute("""SELECT id FROM BotUsers WHERE ChatId = (?) LIMIT 1""", (chat_id,)).fetchone()
    link_record = db_cursor.execute("""SELECT id FROM UsersLinks WHERE UserId = (?) AND Link = (?) LIMIT 1""", (user[0], link)).fetchone()
    # Insert New User
    if not link_record:
        try:
            db_cursor.execute("""INSERT INTO UsersLinks (UserId, Link) VALUES (?, ?)""", (user[0], link))
        except sqlite3.Error as error:
            print(error)
            pass
    # Close DB Connection
    db_connection.commit()
    db_connection.close()
