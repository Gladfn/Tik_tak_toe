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
board = [
        ['--', '--', '--'],
        ['--', '--', '--'],
        ['--', '--', '--']
    ]
cikl = 0


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
        database.insert('users', ['id', 'name', 'status', 'settings'], [[message.chat.id, message.chat.first_name, 'menu', '{\"win\": [], \"lost\": [], \"settings\": [], \"id\": []}']])
        return {"id": message.chat.id, "name": message.chat.first_name, "status": 'menu', "settings": {"win": [], "lost": [], "settings": [], "id": []}}

def two_users(message):

    a = database.select('users', 'id',[["status", "=", "found"]])
        
    if len(a) < 2:
        print("Соперников нет")
    else:
        b = a[0]
        c = a[1]

    data_1 = database.select('users', ["id", "name", "status", "settings"], [["id", "=", b[0]]], 1)
    data_2 = database.select('users', ["id", "name", "status", "settings"], [["id", "=", c[0]]], 1)

    a = [0, 0]
    user_1 = {"id": data_1[0][0], "name": data_1[0][1], "status": data_1[0][2], "settings": json.loads(data_1[0][3])}
    user_2 = {"id": data_2[0][0], "name": data_2[0][1], "status": data_2[0][2], "settings": json.loads(data_2[0][3])}

    return [user_1, user_2]

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

@bot.message_handler(commands=['inline'])
def inline_start_game(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_1_1 = types.InlineKeyboardButton(f'--', callback_data = 'b_1_1')
    item_1_2 = types.InlineKeyboardButton(f'--', callback_data = 'b_1_2')
    item_1_3 = types.InlineKeyboardButton(f'--', callback_data = 'b_1_3')
    item_2_1 = types.InlineKeyboardButton(f'--', callback_data = 'b_2_1')
    item_2_2 = types.InlineKeyboardButton(f'--', callback_data = 'b_2_2')
    item_2_3 = types.InlineKeyboardButton(f'--', callback_data = 'b_2_3')
    item_3_1 = types.InlineKeyboardButton(f'--', callback_data = 'b_3_1')
    item_3_2 = types.InlineKeyboardButton(f'--', callback_data = 'b_3_2')
    item_3_3 = types.InlineKeyboardButton(f'--', callback_data = 'b_3_3')
    markup_inline.add(item_1_1, item_1_2, item_1_3, item_2_1, item_2_2, item_2_3, item_3_1, item_3_2, item_3_3)
    bot.send_message(message.chat.id, 'Hi', reply_markup = markup_inline)
    print(f'Comand from user id {message.from_user.id} with the name {message.from_user.first_name}:       {message.text}')

@bot.message_handler(commands=['start'])
def start_message(message):
    
    board = [
        ['--', '--', '--'],
        ['--', '--', '--'],
        ['--', '--', '--']
    ]
    
    user = get_user(message)
    bot.send_message(message.chat.id,"Привет! Я бот, в котором можно играть в крестики нолики", reply_markup=menu_markups(user))
    log(message, user)
    user_update(user, "menu")

@bot.message_handler(commands=["reload_menu"])
def start_message(message):
    
    board = [
        ['--', '--', '--'],
        ['--', '--', '--'],
        ['--', '--', '--']
    
    ]
    
    user = get_user(message)
    bot.send_message(message.chat.id,"Перезаряжаю!!!!!!!!!!", reply_markup=menu_markups(user))
    log(message, user)
    user_update(user, "menu")

@bot.message_handler(commands=['inline'])
def inline_start_game(message):
    markup_inline = types.InlineKeyboardMarkup()
    x = 'X'
    o = 'O'
    # chosing = chose()
    # if chosing == 'x' || chosing == 'X':

#def deаfewes(message):
    if (message.text == 'X') or (message.text == 'O'):
       bot.send_message(message.from_user.id.choose())

    item_1_1 = types.InlineKeyboardButton(f'{board[0][0]}', callback_data = 'b_1_1')
    item_1_2 = types.InlineKeyboardButton(f'{board[0][1]}', callback_data = 'b_1_2')
    item_1_3 = types.InlineKeyboardButton(f'{board[0][2]}', callback_data = 'b_1_3')
    item_2_1 = types.InlineKeyboardButton(f'{board[1][0]}', callback_data = 'b_2_1')
    item_2_2 = types.InlineKeyboardButton(f'{board[1][1]}', callback_data = 'b_2_2')
    item_2_3 = types.InlineKeyboardButton(f'{board[1][2]}', callback_data = 'b_2_3')
    item_3_1 = types.InlineKeyboardButton(f'{board[2][0]}', callback_data = 'b_3_1')
    item_3_2 = types.InlineKeyboardButton(f'{board[2][1]}', callback_data = 'b_3_2')
    item_3_3 = types.InlineKeyboardButton(f'{board[2][2]}', callback_data = 'b_3_3')
    markup_inline.add(item_1_1, item_1_2, item_1_3, item_2_1, item_2_2, item_2_3, item_3_1, item_3_2, item_3_3)
    bot.send_message(message.chat.id, 'Теперь Вы можете играть, управляя полем с помощью кнопок:', reply_markup = markup_inline)
    print(f'Comand from user id {message.from_user.id} with the name {message.from_user.first_name}:       {message.text}')

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'b_1_1':
            board[0][0] = 'X'
            print(f'User press:        b_1_1, {board[0][0]}')
        elif call.data == 'b_1_2':
            board[0][1] = 'X'
            print(f'User press:        b_1_2, {board[0][1]}')
        elif call.data == 'b_1_3':
            board[0][2] = 'X'
            print(f'User press:        b_1_3, {board[0][2]}')
        elif call.data == 'b_2_1':
            board[1][0] = 'X'
            print(f'User press:        b_2_1, {board[1][0]}')
        elif call.data == 'b_2_2':
            board[1][1] = 'X'
            print(f'User press:        b_2_2, {board[1][1]}')
        elif call.data == 'b_2_3':
            board[1][2] = 'X'
            print(f'User press:        b_2_3, {board[1][2]}')
        elif call.data == 'b_3_1':
            board[2][0] = 'X'
            print(f'User press:        b_3_1, {board[2][0]}')
        elif call.data == 'b_3_2':
            board[2][1] = 'X'
            print(f'User press:        b_3_2, {board[2][1]}')
        elif call.data == 'b_3_3':
            board[2][2] = 'X'
            print(f'User press:        b_3_3, {board[2][2]}')
        if call.data == "start the game":
            print('Start')
            # markup_buttons_pers = types.InlineKeyboardMarkup()
            # item_x = types.InlineKeyboardButton('X')
            # item_o = types.InlineKeyboardButton('O')
            # markup_buttons_pers.add(item_x, item_o)
            # bot.send_message(message.chat.id, 'хороший выбор', reply_markup=markup_buttons_pers)



class MessageHandler:
    def menu(bot, message, user):
        if "НАСТРОЙКИ" in message.text:
            # return MessageHandler.Settings.to_main(bot, message, user)
            return True
        
        if "ПОИСК ПРОТИВНИКА":
            
            board = [
            ['--', '--', '--'],
            ['--', '--', '--'],
            ['--', '--', '--'],
            ['--', '--', '--']
            ]
            return MessageHandler.found(bot, message, user)

    def to_menu(bot, message, user):
        bot.send_message(user["id"], "Хорошего дня", reply_markup=menu_markups(user))
        user_update(user, "menu")
        return True
    
    # class Settings:
    #     def main(bot, maessage, user):
    
    def found(bot, message, user):
        bot.send_message(user["id"], "Поиск соперника", reply_markup=menu_markups(user))  
        user_update(user, status="found")
        a = database.select('users', 'id',[["status", "=", "found"]])
        rand = random.randint(1, 2)
        if rand == 1:
            user["settings"]["settings"].append(1)
            user_update(user, "found", json.dumps(user["settings"], indent=2))
        if rand == 2:
            user["settings"]["settings"].append(2)
            user_update(user, "found", json.dumps(user["settings"], indent=2))
        if len(a) < 2:
            print("Соперников нет")
        
        else:
            date_users = two_users(message)
            
            print(date_users[0])
            print(date_users[1])

            a_1 = date_users[0]
            a_2 = date_users[1]

            id_1 = a_1['id']
            id_2 = a_2['id']

            user_update(date_users[0], status="game_menu", settings=id_2)
            user_update(date_users[1], status="game_menu", settings=id_1)

            return MessageHandler.Game.menu(bot, message, user)

        return True
    
    class Game:
        def menu(bot, message, user):
            if "ПОИСК ПРОТИВНИКА" in message.text:
                bot.send_message(user["id"], "Игра найдена")
            
            
            markup_inline = types.InlineKeyboardMarkup()
            item_1_1 = types.InlineKeyboardButton(f'{board[0][0]}', callback_data = 'b_1_1')
            item_1_2 = types.InlineKeyboardButton(f'{board[0][1]}', callback_data = 'b_1_2')
            item_1_3 = types.InlineKeyboardButton(f'{board[0][2]}', callback_data = 'b_1_3')
            item_2_1 = types.InlineKeyboardButton(f'{board[1][0]}', callback_data = 'b_2_1')
            item_2_2 = types.InlineKeyboardButton(f'{board[1][1]}', callback_data = 'b_2_2')
            item_2_3 = types.InlineKeyboardButton(f'{board[1][2]}', callback_data = 'b_2_3')
            item_3_1 = types.InlineKeyboardButton(f'{board[2][0]}', callback_data = 'b_3_1')
            item_3_2 = types.InlineKeyboardButton(f'{board[2][1]}', callback_data = 'b_3_2')
            item_3_3 = types.InlineKeyboardButton(f'{board[2][2]}', callback_data = 'b_3_3')
            markup_inline.add(item_1_1, item_1_2, item_1_3, item_2_1, item_2_2, item_2_3, item_3_1, item_3_2, item_3_3)
            bot.send_message(message.chat.id, 'Hi', reply_markup = markup_inline)
        
                # if (board[0][0] == 'X' or 'O') and (board[0][1] == 'X' or 'O') and (board[0][2] == 'X' or 'O'):
                #     print("Игрок выиграл")
                #     break

            a = database.select('users', 'settings', [['id', '=', message.chat.id]])
            a = a[0]

            # print(f'Comand from user id {message.from_user.id} with the name {message.from_user.first_name}:{message.text}')
            # if "СТОП" in message.text:
            #     bot.send_message(user["id"], "Вы уверенны?", reply_markups=markups("Да", "Отмена"))

            #     if "ДА" in message.text:
            #         bot.send_message(user["id"], "Выход из матча", reply_markups=menu_markups(user))
            #         user_update(user, status="menu", settings='{}')
            #         return MessageHandler.Game.to_menu(bot, message, user)

            #     if "Отмена" in message.text:
            #         return True
            
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