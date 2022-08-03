import types
import telebot
import config
from telebot import types
from DB import DB
import mysql.connector
import json
import random

bot = telebot.TeleBot(config.TOKEN)
database = DB(config.mysql)
bot.send_message(1294113685, "Start Bot")

def json_loads(data):
    try:
        return json.loads(data)
    except:
        return None

def get_user(message):
    data = database.select('users', ['id', 'name', 'status', 'settings'], [['id', '=', message.chat.id]], 1)
    if (data):
        return {"id": data[0][0], "name": data[0][1], "status": data[0][2], "settings": json.loads(data[0][3])}
    else:
        database.insert('users', ['id', 'name', 'status', 'settings'], [[message.chat.id, message.chat.first_name, 'menu', '{\"win\": [], \"lost\": []}']])
        return {"id": message.chat.id, "name": message.chat.first_name, "status": 'menu', "settings": {"win": [], "lost": []}}

def log(message, user):
    query = "INSERT INTO log (text) VALUES (%s)"

def user_update(user, status=None, settings=None):
    if status and not settings:
        database.update('users', {'status': status}, [['id', '=', user['id']]])
    elif settings and not status:
        database.update('users', {'settings': settings}, [['id', '=', user['id']]])
    else:
        database.update('users', {'status': status, 'settings': settings}, [['id', '=', user['id']]])

def markups(buttons):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b = []
    for i in buttons:
        b.append(types.KeyboardButton(i))
    markup.add(*b)
    return markup

def menu_markups(user):
    answer = markups(["Поиск противника🔍", "Настройки⚙️", "Информацияℹ️"])
    return answer

@bot.message_handler(commands=['start'])
def start_message(message):
    user = get_user(message)
    bot.send_message(message.chat.id,"Привет! Я бот, в котором можно играть в крестики нолики")
    log(message, user)
    user_update(user, "menu")

@bot.message_handler(commands=["reload_menu"])
def start_message(message):
    user = get_user(message)
    bot.send_message(message.chat.id,"Перезаряжаю!!!!!!!!!!", reply_markup=menu_markups(user))
    log(message, user)
    user_update(user, "menu")

class MessageHandler:
    def menu(bot, message, user):
        if "НАСТРОЙКИ" in message.text:
            # return MessageHandler.Settings.to_main(bot, message, user)
            return True
        
        if "ПОИСК ПРОТИВНИКА":
            return MessageHandler.found(bot, message, user)

    def to_menu(bot, message, user):
        bot.send_message(user["id"], "Хорошего дня", reply_markup=menu_markups(user))
        user_update(user, status="menu")
        return True
    
    # class Settings:
    #     def main(bot, maessage, user):
    
    def found(bot, message, user):
        bot.send_message(user["id"], "Поиск соперника", reply_markup=menu_markups(user))        
        user_update(user, status="found")
        a = database.select('users', 'id',[["status", "=", "found"]])
        b = len(a) - 1
        c = a[random.randint(0, b)]
        c = c[0]
        print(c)

        return True
    
    class Game:
        def menu(bot, message, user):
            bot.send_message(user["id"], "Игра найдена", reply_markup=markups("Стоп"))
            if "СТОП" in message.text:
                bot.send_message(user["id"], "Вы уверенны?", reply_markups=markups("Да", "Отмена"))

                if "ДА" in message.text:
                    bot.send_message(user["id"], "Выход из матча", reply_markups=menu_markups(user))
                    user_update(user, status="menu")
                    return True

                if "Отмена" in message.text:
                    return True
                
        def to_menu(bot, message, user):
            bot.send_message(user["id"], "Хорошего дня", reply_markup=menu_markups(user))
            user_update(user, status="menu")
            return MessageHandler.to_menu
    

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(f"{message.chat.id} {message.chat.first_name} |{message.text}|")
    message.text = message.text.strip().replace("  ", " ").replace("\t\t", "\t")
    user = get_user(message)
    message.text = message.text.upper()
    log(message, user)
    action = {
        "menu": MessageHandler.menu,
        # "settings": MessageHandler.Settings.main,
        "found": MessageHandler.found,
        "game_menu": MessageHandler.Game.menu
    }
    if action.get(user["status"]):
        if not action[user["status"]](bot, message, user):
            bot.send_message(user["id"], "Не понял!")
    else:
        bot.send_message(user["id"], f"Статус {user['status']} не найден!")
    return

bot.polling()