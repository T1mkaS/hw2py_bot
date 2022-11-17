import json, os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

users = {}


@bot.message_handler(content_types=["new_chat_members"])
def new_chat_member_handler(message):
    for member in message.json["new_chat_members"]:
        users[member["username"]] = member["id"]
        if member['username'] == bot.user.username:
            bot.send_message(message.chat.id, f"Привет, сделайте меня админом, чтобы у меня был ко всему доступ!")
        else:
            bot.send_message(message.chat.id, f"Привет, {member['username']}, как у тебя дела?")
    with open("users.json", "w") as users_file:
        json.dump(users, users_file)


@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_message(message.chat.id, "Привет ✌️, меня зовут Бабиджон\nВведите /help, чтобы узнать, что я могу!")


@bot.message_handler(commands=['help'])
def button_message(message):
    bot.send_message(message.chat.id,
                     "Чтобы сделать участника админом наберите /make_admin\nЧтобы забанить человека в чате наберите /ban\nЧтобы разбанить человека в чате наберите /razban\nЧтобы узнать статистику чата наберите /stat\nЧтобы Попросить ливнуть Бабиджона наберите /leave")


@bot.message_handler(commands=['make_admin'])
def make_admin(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Да', callback_data="Да")
    item2 = types.InlineKeyboardButton('Нет', callback_data="Нет")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Сделать кого-то админом?", reply_markup=markup)


def test(message):
    try:
        username = message.text
        if (username[0] == '@'):
            username = username[1:]
        if username not in users.keys():
            raise Exception
        try:
            bot.promote_chat_member(message.chat.id, users[username], True, True, True)
            bot.send_message(message.chat.id, f'Теперь {username} стал админом!')
        except:
            bot.send_message(message.chat.id, 'У меня нет прав сделать его админом(')
    except:
        bot.send_message(message.chat.id,
                         "Человек либо уже админ, либо его нет в базе данных, добавьте его после Бабиджона в группу!")


@bot.message_handler(commands=['stat'])
def make_admin(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Число участников', callback_data="members")
    item2 = types.InlineKeyboardButton('Число админов', callback_data="admins")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Что бы вы хотели узнать?", reply_markup=markup)


@bot.message_handler(commands=['leave'])
def leave(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Да', callback_data="leave")
    item2 = types.InlineKeyboardButton('Нет', callback_data="no_leave")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Вы меня выгоняете?", reply_markup=markup)


@bot.message_handler(commands=['ban'])
def ban(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Да', callback_data="ban")
    item2 = types.InlineKeyboardButton('Нет', callback_data="no_ban")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Забанить кого-то?", reply_markup=markup)


@bot.message_handler(commands=['razban'])
def razban(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Да', callback_data="razban")
    item2 = types.InlineKeyboardButton('Нет', callback_data="no_razban")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Разбанить кого-то?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query1(call):
    if call.data == "Да":
        mesg = bot.send_message(call.message.chat.id, "Введите никнейм юзера ответом на данное сообщение")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(mesg, test)
    elif call.data == "Нет":
        bot.answer_callback_query(call.id, "На нет и суда нет")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "members":
        mesg = bot.send_message(call.message.chat.id,
                                f"В чате всего {bot.get_chat_member_count(call.message.chat.id)} человек(а)")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "admins":
        bot.send_message(call.message.chat.id,
                         f"У нас {len(bot.get_chat_administrators(call.message.chat.id))} админа(ов)")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "no_leave":
        bot.send_message(call.message.chat.id, "Спасибо, барин!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "leave":
        bot.send_message(call.message.chat.id, "Прощайте, барин!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.leave_chat(call.message.chat.id)
    if call.data == "ban":
        mesg = bot.send_message(call.message.chat.id, "Введите никнейм юзера ответом на данное сообщение")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(mesg, ban_user)
    elif call.data == "no_ban":
        bot.answer_callback_query(call.id, "Повезло-повезло")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == "razban":
        mesg = bot.send_message(call.message.chat.id, "Введите никнейм юзера ответом на данное сообщение")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(mesg, razban_user)
    elif call.data == "no_razban":
        bot.answer_callback_query(call.id, "Ну бывает")
        bot.delete_message(call.message.chat.id, call.message.message_id)


def ban_user(message):
    try:
        username = message.text
        if (username[0] == '@'):
            username = username[1:]
        if username not in users.keys():
            raise Exception
        try:
            bot.ban_chat_member(message.chat.id, users[username])
            bot.send_message(message.chat.id, f'Теперь {username} забанен!')
        except:
            bot.send_message(message.chat.id, 'У меня нет прав его забанить(')
    except:
        bot.send_message(message.chat.id, "Его нет в базе данных, добавьте его после Бабиджона в группу!")


def razban_user(message):
    try:
        username = message.text
        if (username[0] == '@'):
            username = username[1:]
        if username not in users.keys():
            raise Exception
        try:
            bot.unban_chat_member(message.chat.id, users[username])
            bot.send_message(message.chat.id, f'Теперь {username} разбанен!')
        except:
            bot.send_message(message.chat.id, 'У меня нет прав его забанить(')
    except:
        bot.send_message(message.chat.id, "Его нет в базе данных, добавьте его после Бабиджона в группу!")


if __name__ == '__main__':
    try:
        with open("users.json") as users_file:
            users = json.load(users_file)
    except:
        print("first launch")
    bot.polling(none_stop=True, interval=0)
