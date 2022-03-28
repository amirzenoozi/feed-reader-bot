from dotenv import load_dotenv
import script.utils
import script.database as db
import sqlite3
import telebot
import os

config = load_dotenv(".localenv")
app = telebot.TeleBot(os.getenv('BOT_TOKEN'))
db_connection = sqlite3.connect('feed_reader.db')
db_cursor = db_connection.cursor()

try:
    db_cursor.executescript('''CREATE TABLE IF NOT EXISTS BotUsers (id INTEGER PRIMARY KEY AUTOINCREMENT, ChatId CHAR(50), Name CHAR(50));''')
    db_cursor.executescript('''CREATE TABLE IF NOT EXISTS UsersLinks (id INTEGER PRIMARY KEY AUTOINCREMENT, UserId CHAR(50), Link CHAR(150), FOREIGN KEY (UserId) REFERENCES BotUsers (id));''')
except sqlite3.Error as error:
    print(error)
    pass

db_connection.commit()
db_connection.close()

@app.message_handler(commands=['start'])
def say_hello(messages):
    app.send_message(messages.chat.id, f'Wellcome Dear {messages.from_user.first_name}🌹')
    app.send_message(messages.chat.id, f'Here you can Classify Your Image')
    app.send_message(messages.chat.id, f'Now send me the photo so I can tell you 😉')
    db.insert_bot_user(messages.from_user.id, messages.from_user.first_name)

@app.message_handler(commands=['new'])
def get_link(messages):
    msg = app.reply_to(messages, f'I\'m Waiting You To Send Your RSS Link... ⏳')
    app.register_next_step_handler(msg, process_new_rss_link)


def process_new_rss_link(message):
    try:
        chat_id = message.chat.id
        link = message.text
        db.insert_rss_link(chat_id, link)
        app.reply_to(message, 'Your New RSS Link Saved Successfully!🌹')
    except Exception as e:
        app.reply_to(message, 'Oops!')


if __name__ == '__main__':
    # Running Telegram Bot
    print("We Are Starting The Bot...")
    app.infinity_polling()