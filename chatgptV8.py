import datetime
import os
import random
import sqlite3
import time

import requests
from telebot import TeleBot, types
import openai
from pyqiwip2p import QiwiP2P



test_bot = '6177767883:AAFYGDT8ovUwW0VYk9JBMuZ7AK29DE3nCYg'
owner_bot = '6266058087:AAHuP3jKoaJKrRn7M4WDQBM46TSfuG4LqqE'

bot = TeleBot(token=owner_bot, parse_mode='html')
openai.api_key = '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'
qiwi_token = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImRndjlrai0wMCIsInVzZXJfaWQiOiI5OTg5OTc5NDU1NzAiLCJzZWNyZXQiOiJhMDQ3ZDRiYzkyZTNmZjVmN2NmZmU1NThjY2JiYzJhNGJmYjVmYTBlZmUwNDg4MmRkN2Q0Yjc5YjM1OTRlNzdmIn19'
p2p = QiwiP2P(auth_key=qiwi_token)
connect = sqlite3.connect('db.db', check_same_thread=False)
cursor = connect.cursor()


def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False

class Database:
    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connect.cursor()
    def user_exists(self, user_id):
        with self.connect:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id, )).fetchall()
            return bool(len(result))
    def add_user(self, user_id, user_first_name, username):
        with self.connect:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f"{user_id}", f"{user_first_name}", f"{username}", 0, "user", datetime.datetime.now(), 0, 0, 0, 10, 5))

    def user_money(self, user_id):
        with self.connect:
            result = self.cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,)).fetchmany(1)
            return int(result[0][0])
    def set_money(self, user_id, money):
        with self.connect:
            return self.cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (money, user_id))

    def add_check(self, user_id, money, bill_id):
        with self.connect:
            self.cursor.execute("INSERT INTO check_user VALUES(?, ?, ?)", (user_id, money, bill_id,))

    def get_check(self, bill_id):
        with self.connect:
            result = self.cursor.execute("SELECT * FROM check_user WHERE bill_id=?", (bill_id,)).fetchmany(1)
            if not bool(len(result)):
                return False
            return result[0]

    def delete_check(self, bill_id):
        with self.connect:
            return self.cursor.execute("DELETE FROM check_user WHERE bill_id=?", (bill_id,))

    def set_time_vip(self, user_id, vip_time):
        with self.connect:
            return self.cursor.execute("UPDATE users SET time_vip=? WHERE user_id=?", (vip_time, user_id))

    def get_time_vip(self, user_id):
        with self.connect:
            result = self.cursor.execute("SELECT time_vip FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub
    def get_sub_status(self, user_id):
        with self.connect:
            result = self.cursor.execute("SELECT time_vip FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            if time_sub > int(time.time()):
                return True
            else:
                return False
    def get_time_promo(self, promos):
        with self.connect:
            result = self.cursor.execute("SELECT promo_time FROM promo_codes WHERE promo=?", (promos,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub

db = Database("db.db")


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace('days', 'дней')
        dt = dt.replace('day', 'день')
        return dt


def channel_check():
    btn = types.InlineKeyboardMarkup()
    channel1 = types.InlineKeyboardButton(text='✅ Подписаться на канал', url='https://t.me/King_ProjectBot')
    check_keyboard = types.InlineKeyboardButton('✅  Проверить подписку', callback_data='channel_check')
    btn.add(channel1)
    btn.add(check_keyboard)
    return btn

def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def start_cmd(message: types.Message):
    # cursor.execute(f'alter table users add balance numeric;')
    # cursor.execute(f"UPDATE users SET balance=0 WHERE status='owner'")
    # cursor.execute(f"UPDATE users SET balance=0 WHERE status='user'")
    # cursor.execute(f"UPDATE users SET balance=0 WHERE status='admin'")
    # connect.commit()
    if message.chat.type == 'private':
        # cursor.execute(f"""CREATE TABLE users(
        #             user_id numeric,
        #             user_name varchar,
        #             username varchar,
        #             amount_of_use numeric,
        #             amount_of_use_img numeric,
        #             status varchar,
        #             date_reg varchar
        # )""")
        user_subs = bot.get_chat_member(chat_id=-1001938985284, user_id=message.from_user.id)
        if not check_sub_channel(user_subs):
            bot.send_message(message.chat.id, f'Подпишись на канал чтобы получить доступ к боту!', reply_markup=channel_check())
            return

        try:
            cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
            users = cursor.fetchone()
        except:
            return
        usrbtn = types.ReplyKeyboardMarkup(resize_keyboard=True)
        profile = types.KeyboardButton('Профиль ⭕️')
        rates = types.KeyboardButton('⚜️VIP тарифы')
        activation_promo = types.KeyboardButton('🔑 Активировать промо-код')
        support = types.KeyboardButton('👨‍💻 Техподдержка')
        day_limit = types.KeyboardButton('🆓 Взять сегодняшний лимит')
        popolnit = types.KeyboardButton('💳 Пополнить')
        usrbtn.add(profile, support)
        usrbtn.add(rates, activation_promo)
        usrbtn.add(popolnit)
        usrbtn.add(day_limit)
        admbtn = types.ReplyKeyboardMarkup(resize_keyboard=True)
        profiles = types.KeyboardButton('Профиль ⭕️')
        ratess = types.KeyboardButton('⚜️VIP тарифы')
        count_users = types.KeyboardButton('🔄 Количество пользователей')
        admbtn.add(profiles, ratess)
        admbtn.add(count_users)
        if not message.from_user.username:
            bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
            return
        if not users:
            cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}", 0, "user", datetime.datetime.now(), 0, 0, 0, 10, 5))
            connect.commit()
            bot.send_message(message.chat.id, f'<b>Добро пожаловать!\nНапишите свой вопрос, задачу или код.</b>',
                             reply_markup=usrbtn)
            bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')
            return
        cursor.execute("UPDATE users SET username=? WHERE user_id=?",
                       (f"{message.from_user.username}", f"{message.from_user.id}",))
        cursor.execute("UPDATE users SET user_name=? WHERE user_id=?",
                       (f"{message.from_user.first_name}", f"{message.from_user.id}",))
        connect.commit()
        if users[4] == 'owner' or users[4] == 'admin':
            bot.send_message(message.chat.id, f'<b>Добро пожаловать!\nНапишите свой вопрос, задачу или код.</b>',
                             reply_markup=admbtn)
            return
        bot.send_message(message.chat.id, f'<b>Добро пожаловать!\nНапишите свой вопрос, задачу или код.</b>',
                         reply_markup=usrbtn)
        bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду /start')
    elif message.chat.type == 'supergroup' or message.chat.type == 'group':
        try:
            cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
            users = cursor.fetchone()
        except:
            return
        admbtn = types.InlineKeyboardMarkup()
        profiles = types.InlineKeyboardButton(text='Профиль ⭕️', callback_data='profiles')
        count_users = types.InlineKeyboardButton(text='🔄 Количество пользователей', callback_data='count_users')
        admbtn.add(profiles, count_users)
        usrbtn = types.InlineKeyboardMarkup()
        profile = types.InlineKeyboardButton(text='Профиль ⭕️', callback_data='profile')
        support = types.InlineKeyboardButton(text='👨‍💻 Техподдержка', callback_data='support')
        rates = types.InlineKeyboardButton(text='⚜️VIP тарифы', callback_data='rates')
        btnTopUp = types.InlineKeyboardButton(text='💳 Пополнить', callback_data='top_up')
        day_limit = types.InlineKeyboardButton(text='🆓 Взять сегодняшний лимит', callback_data='day_limit')
        usrbtn.add(profile, support)
        usrbtn.add(rates)
        usrbtn.add(btnTopUp)
        usrbtn.add(day_limit)
        if not message.from_user.username:
            bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
            return
        if not users:
            cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}", 0, "user", datetime.datetime.now(), 0, 0, 0, 10, 5))
            connect.commit()
            bot.send_message(message.chat.id,
                             f'<a href="tg://openmessage?user_id={message.from_user.id}">{message.from_user.first_name}</a> Напишите свой вопрос через команду /chat\nНапример: /chat Напиши мне сочинения про свой отдых',
                             reply_markup=usrbtn)
            bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')
            return
        if users[4] == 'owner' or users[4] == 'admin':
            bot.send_message(message.chat.id, f'<b>Добро пожаловать!\nНапишите свой вопрос, задачу или код.</b>\nПисать через команду /chat\nНапример: /chat Напиши мне сочинения про мир',
                             reply_markup=admbtn)
            return
        bot.send_message(message.chat.id, f'<b>Добро пожаловать!\nНапишите свой вопрос, задачу или код.</b>\nПисать через команду /chat\nНапример: /chat Напиши мне сочинения про мир',
                         reply_markup=usrbtn)
        bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду /start')


@bot.message_handler(commands=['buy'])
def buy_money_cmd(message: types.Message):
    if message.chat.type == 'private':
        if not message.from_user.username:
            bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
            return
        bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду /buy')
        user_subs = bot.get_chat_member(chat_id=-1001938985284, user_id=message.from_user.id)
        if not check_sub_channel(user_subs):
            bot.send_message(message.chat.id, f'Подпишись на канал чтобы получить доступ к боту!',
                             reply_markup=channel_check())
            return
        btnTopUp = types.InlineKeyboardButton(text='💳 Пополнить', callback_data='top_up')
        topUpMenu = types.InlineKeyboardMarkup(row_width=1)
        topUpMenu.add(btnTopUp)
        if not db.user_exists(message.from_user.id):
            db.add_user(user_id=f"{message.from_user.id}", user_first_name=f"{message.from_user.first_name}", username=f"{message.from_user.username}")
            bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')

        bot.send_message(message.chat.id, f'💰 Ваш баланс: {db.user_money(message.from_user.id)}', reply_markup=topUpMenu)
    elif message.chat.type == 'supergroup' or message.chat.type == 'group':
        bot.send_message(message.chat.id, f'Это команда работает только в лс бота <a href="https://t.me/KingChatGPTbot">Перейти в лс бота</a>')

def buy_menu(isUrl=True, url="", bill=""):
    qiwiMenu = types.InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIWI = types.InlineKeyboardButton(text='Ссылка на оплату', url=url)
        qiwiMenu.add(btnUrlQIWI)

    btnCheckQIWI = types.InlineKeyboardButton(text='Проверить оплату', callback_data=f"checks_{bill}")
    qiwiMenu.add(btnCheckQIWI)
    return qiwiMenu


@bot.message_handler(commands=['top'])
def top_buy_cmd(message: types.Message):
    if message.chat.type == 'private':
        if not message.from_user.username:
            bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
            return
        bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду /top')
        user_subs = bot.get_chat_member(chat_id=-1001938985284, user_id=message.from_user.id)
        if not check_sub_channel(user_subs):
            bot.send_message(message.chat.id, f'Подпишись на канал чтобы получить доступ к боту!',
                             reply_markup=channel_check())
            return
        if not message.text[5:]:
            bot.send_message(message.chat.id, f'Напишите сумму пополнения /top [сумма]')
            return
        if is_number(message.text[5:]):
            message_money = int(message.text[5:])
            if message_money >= 15:
                comment = str(message.from_user.id) + "_" + str(random.randint(1000, 9999))
                bill = p2p.bill(amount=message_money, lifetime=15, comment=comment)
                db.add_check(message.from_user.id, message_money, bill.bill_id)

                bot.send_message(message.chat.id, f"Вам нужно отправить {message_money}₽. на наш счет QIWI\nСсылка: {bill.pay_url}\nУказав комментарий к оплате: {comment}", reply_markup=buy_menu(url=bill.pay_url, bill=bill.bill_id))
            else:
                bot.send_message(message.chat.id, f'Минимальная сумма для пополнения 15₽.')
        else:
            bot.send_message(message.chat.id, f'Введите целое число')
    elif message.chat.type == 'supergroup' or message.chat.type == 'group':
        bot.send_message(message.chat.id, f'Это команда работает только в лс бота <a href="https://t.me/KingChatGPTbot">Перейти в лс бота</a>')


@bot.message_handler(commands=['admin'])
def owner_panel_cmd(message: types.Message):
    if message.chat.type == 'private':
        try:
            cursor.execute(f"SELECT status FROM users WHERE user_id='{message.from_user.id}'")
            status = cursor.fetchone()
        except:
            return
        if status[0] == 'admin' or status[0] == 'owner':
            infousers = types.KeyboardButton('ℹ️ Информация о пользователе')
            count_users = types.KeyboardButton('🔄 Количество пользователей')
            rass_user = types.KeyboardButton('📨 Написать пользователю')
            adminbtn = types.ReplyKeyboardMarkup(resize_keyboard=True)
            adminbtn.add(infousers, count_users)
            adminbtn.add(rass_user)
            if not message.from_user.username:
                bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
                return
            bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду /admin')
            if not status:
                cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}", 0, "user",
                datetime.datetime.now(), 0, 0, 0, 10, 5))
                connect.commit()
                bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')
                return
            try:
                bot.send_message(message.chat.id,
                                 f'<b>Добро пожаловать в Admin Panel</b>',
                                 reply_markup=adminbtn)
            except:
                return

@bot.message_handler(commands=['owner'])
def owner_panel_cmd(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 6062336337:
            try:
                cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
                users = cursor.fetchone()
            except:
                return
            admbtn = types.ReplyKeyboardMarkup(resize_keyboard=True)
            add_admin = types.KeyboardButton('➕ Добавить админа')
            remove_admin = types.KeyboardButton('➖ Удалить админа')
            infousers = types.KeyboardButton('ℹ️ Информация о пользователе')
            count_users = types.KeyboardButton('🔄 Количество пользователей')
            gift_sub = types.KeyboardButton('🎁 Подарить подписку')
            gift_balance = types.KeyboardButton('⛔️ Выдать баланс')
            take_balance = types.KeyboardButton('⛔️ Забрать баланс')
            create_promo = types.KeyboardButton('🪄 Создать промо-код')
            lists_promo = types.KeyboardButton('📓 Список промо-кодов')
            remove_promo = types.KeyboardButton('🗑 Удалить промо-код')
            rass = types.KeyboardButton('✉️ Рассылка')
            rass_user = types.KeyboardButton('📨 Написать пользователю')
            list_admin = types.KeyboardButton('📂 Список админов')
            admbtn.add(add_admin, remove_admin)
            admbtn.add(infousers, count_users)
            admbtn.add(gift_balance, take_balance)
            admbtn.add(create_promo, lists_promo)
            admbtn.add(remove_promo, rass)
            admbtn.add(list_admin)
            admbtn.add(rass_user)
            admbtn.add(gift_sub)
            if not message.from_user.username:
                bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
                return
            if not users:
                cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}", 0, "user",
                datetime.datetime.now(), 0, 0, 0, 10, 5))
                connect.commit()
                bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')
                return
            try:
                bot.send_message(message.chat.id,
                                 f'<b>Добро пожаловать в Owner Panel</b>',
                                 reply_markup=admbtn)
            except:
                return


@bot.message_handler(commands=['img'])
def img_chatgpt_cmd(message: types.Message):
    if not message.from_user.username:
        bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
        return
    user_subs = bot.get_chat_member(chat_id=-1001938985284, user_id=message.from_user.id)
    if not check_sub_channel(user_subs):
        bot.send_message(message.chat.id, f'Подпишись на канал чтобы получить доступ к боту!',
                         reply_markup=channel_check())
        return
    try:
        cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
        users = cursor.fetchone()
    except:
        return
    if db.get_sub_status(message.from_user.id):
        try:
            cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
            users = cursor.fetchone()
        except:
            return
        if not message.from_user.username:
            if message.from_user.id == 6062336337:
                pass
            bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
            return
        if not users:
            cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}", 0, "user", datetime.datetime.now(), 0, 0, 0, 10, 5))
            connect.commit()
            bot.send_message(message.chat.id, f'Нажмите /start')
            bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')
            return
        cursor.execute("UPDATE users SET username=? WHERE user_id=?",
                       (f"{message.from_user.username}", f"{message.from_user.id}",))
        cursor.execute("UPDATE users SET user_name=? WHERE user_id=?",
                       (f"{message.from_user.first_name}", f"{message.from_user.id}",))
        connect.commit()
        if message.text[5:].lower().startswith('как тебя зовут'):
            bot.send_message(message.chat.id, f'Меня зовут KING')
        elif message.text[5:].lower().startswith('what is your name'):
            bot.send_message(message.chat.id, f'My name is KING')
        elif message.text[5:].lower().startswith('what`s your name'):
            bot.send_message(message.chat.id, f'My name is KING')
        elif message.text[5:].lower().startswith("what's your name"):
            bot.send_message(message.chat.id, f'My name is KING')
        else:
            edit_text = bot.reply_to(message=message, text=f'⏳ Подготовка ответа...')
            try:
                response = openai.Image.create(
                    prompt=message.text[5:],
                    n=1,
                    size="1024x1024",
                )
                bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id, text=f"<a href='{response['data'][0]['url']}'>Ссылка на фотографию</a>")
                bot.send_message(6062336337, text=f"Запрос от @{message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: <a href='{response['data'][0]['url']}'>Ссылка на фотографию</a>")
                cursor.execute(
                    f'UPDATE users SET amount_of_use_img="{users[3] + 1}" WHERE user_id="{message.from_user.id}"')
                connect.commit()
            except:
                bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id, text=f'❗️Задайте вопрос заново или попробуйте позже...',
                                      disable_web_page_preview=True)
                bot.send_message(6062336337,
                                 f'Запрос от @{message.from_user.username}\nStatus: ❌\nRequest: {message.text[5:]}')
    else:
        if users[10] > 0:
            try:
                cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
                users = cursor.fetchone()
            except:
                return
            if not message.from_user.username:
                if message.from_user.id == 6062336337:
                    pass
                bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
                return
            if not users:
                cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}", 0,
                "user", datetime.datetime.now(), 0, 0, 0, 10, 5))
                connect.commit()
                bot.send_message(message.chat.id, f'Нажмите /start')
                bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')
                return
            cursor.execute("UPDATE users SET username=? WHERE user_id=?",
                           (f"{message.from_user.username}", f"{message.from_user.id}",))
            cursor.execute("UPDATE users SET user_name=? WHERE user_id=?",
                           (f"{message.from_user.first_name}", f"{message.from_user.id}",))
            connect.commit()
            if message.text[5:].lower().startswith('как тебя зовут'):
                bot.send_message(message.chat.id, f'Меня зовут KING')
            elif message.text[5:].lower().startswith('what is your name'):
                bot.send_message(message.chat.id, f'My name is KING')
            elif message.text[5:].lower().startswith('what`s your name'):
                bot.send_message(message.chat.id, f'My name is KING')
            elif message.text[5:].lower().startswith("what's your name"):
                bot.send_message(message.chat.id, f'My name is KING')
            else:
                edit_text = bot.reply_to(message=message, text=f'⏳ Подготовка ответа...')
                try:
                    response = openai.Image.create(
                        prompt=message.text[5:],
                        n=1,
                        size="1024x1024",
                    )
                    bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                          text=f"<a href='{response['data'][0]['url']}'>Ссылка на фотографию</a>")
                    bot.send_message(6062336337,
                                     text=f"Запрос от @{message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: <a href='{response['data'][0]['url']}'>Ссылка на фотографию</a>")
                    cursor.execute(
                        f'UPDATE users SET amount_of_use_img="{users[3] + 1}" WHERE user_id="{message.from_user.id}"')
                    cursor.execute(
                        f'UPDATE users SET question_img="{users[10] - 1}" WHERE user_id="{message.from_user.id}"')
                    connect.commit()
                except:
                    bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                          text=f'❗️Задайте вопрос заново или попробуйте позже...',
                                          disable_web_page_preview=True)
                    bot.send_message(6062336337,
                                     f'Запрос от @{message.from_user.username}\nStatus: ❌\nRequest: {message.text[5:]}')
        else:
            if users[4] == 'owner' or users[4] == 'admin':
                try:
                    cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
                    users = cursor.fetchone()
                except:
                    return
                if not message.from_user.username:
                    if message.from_user.id == 6062336337:
                        pass
                    bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
                    return
                if not users:
                    cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}",
                        0,
                        "user", datetime.datetime.now(), 0, 0, 0, 10, 5))
                    connect.commit()
                    bot.send_message(message.chat.id, f'Нажмите /start')
                    bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')
                    return
                if message.text[5:].lower().startswith('как тебя зовут'):
                    bot.send_message(message.chat.id, f'Меня зовут KING')
                elif message.text[5:].lower().startswith('what is your name'):
                    bot.send_message(message.chat.id, f'My name is KING')
                elif message.text[5:].lower().startswith('what`s your name'):
                    bot.send_message(message.chat.id, f'My name is KING')
                elif message.text[5:].lower().startswith("what's your name"):
                    bot.send_message(message.chat.id, f'My name is KING')
                else:
                    edit_text = bot.reply_to(message=message, text=f'⏳ Подготовка ответа...')
                    try:
                        response = openai.Image.create(
                            prompt=message.text[5:],
                            n=1,
                            size="1024x1024",
                        )
                        bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                              text=f"<a href='{response['data'][0]['url']}'>Ссылка на фотографию</a>")
                        bot.send_message(6062336337,
                                         text=f"Запрос от @{message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: <a href='{response['data'][0]['url']}'>Ссылка на фотографию</a>")
                        cursor.execute(
                            f'UPDATE users SET amount_of_use_img="{users[3] + 1}" WHERE user_id="{message.from_user.id}"')
                        cursor.execute(
                            f'UPDATE users SET question="{users[10] - 1}" WHERE user_id="{message.from_user.id}"')
                        connect.commit()
                    except:
                        bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                              text=f'❗️Задайте вопрос заново или попробуйте позже...',
                                              disable_web_page_preview=True)
                        bot.send_message(6062336337,
                                         f'Запрос от @{message.from_user.username}\nStatus: ❌\nRequest: {message.text[5:]}')
            else:
                bot.send_message(message.from_user.id, f'У вас закончился сегодняшний лимит на фотографии')

@bot.message_handler(commands=['chat'])
def chat_chatgpt_cmd(message: types.Message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group':
        try:
            cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
            users = cursor.fetchone()
        except:
            return
        if db.get_sub_status(message.from_user.id):
            try:
                cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
                users = cursor.fetchone()
            except:
                return
            cursor.execute(f"SELECT * FROM users")
            all_users = cursor.fetchall()
            if not message.from_user.username:
                if message.from_user.id == 6062336337:
                    pass
                bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
                return
            if not users:
                cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}", 0, "user", datetime.datetime.now(), 0, 0, 0, 10, 5))
                connect.commit()
                bot.send_message(message.chat.id, f'Нажмите /start')
                bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')
                return
            cursor.execute("UPDATE users SET username=? WHERE user_id=?",
                           (f"{message.from_user.username}", f"{message.from_user.id}",))
            cursor.execute("UPDATE users SET user_name=? WHERE user_id=?",
                           (f"{message.from_user.first_name}", f"{message.from_user.id}",))
            connect.commit()
            if message.text[6:].lower().startswith('как тебя зовут'):
                bot.send_message(message.chat.id, f'Меня зовут KING')
            elif message.text[6:].lower().startswith('what is your name'):
                bot.send_message(message.chat.id, f'My name is KING')
            elif message.text[6:].lower().startswith('what`s your name'):
                bot.send_message(message.chat.id, f'My name is KING')
            elif message.text[6:].lower().startswith("what's your name"):
                bot.send_message(message.chat.id, f'My name is KING')
            else:
                edit_text = bot.reply_to(message=message, text=f'⏳ Подготовка ответа...')
                try:
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=message.text[6:],
                        temperature=0.7,
                        max_tokens=4000,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
                    bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                          text=f'{response["choices"][0]["text"]}')
                    bot.send_message(6062336337,
                                     f'Запрос от @{message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: {response["choices"][0]["text"]}')
                    cursor.execute(
                        f'UPDATE users SET amount_of_use="{users[3] + 1}" WHERE user_id="{message.from_user.id}"')
                    connect.commit()
                except:
                    bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                          text=f'❗️Задайте вопрос заново или попробуйте позже...',
                                          disable_web_page_preview=True)
                    bot.send_message(6062336337,
                                     f'Запрос от @{message.from_user.username}\nStatus: ❌\nRequest: {message.text[6:]}')
        else:
            if users[9] > 0:
                try:
                    cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
                    users = cursor.fetchone()
                except:
                    return
                if message.text[6:].lower().startswith('как тебя зовут'):
                    bot.send_message(message.chat.id, f'Меня зовут KING')
                elif message.text[6:].lower().startswith('what is your name'):
                    bot.send_message(message.chat.id, f'My name is KING')
                elif message.text[6:].lower().startswith('what`s your name'):
                    bot.send_message(message.chat.id, f'My name is KING')
                elif message.text[6:].lower().startswith("what's your name"):
                    bot.send_message(message.chat.id, f'My name is KING')
                else:
                    edit_text = bot.reply_to(message=message, text=f'⏳ Подготовка ответа...')
                    try:
                        response = openai.Completion.create(
                            model="text-davinci-003",
                            prompt=message.text[6:],
                            temperature=0.7,
                            max_tokens=4000,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0
                        )
                        bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                              text=f'{response["choices"][0]["text"]}')
                        bot.send_message(6062336337,
                                         f'Запрос от @{message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: {response["choices"][0]["text"]}')
                        cursor.execute(
                            f'UPDATE users SET amount_of_use="{users[3] + 1}" WHERE user_id="{message.from_user.id}"')
                        cursor.execute(
                            f"UPDATE users SET question='{users[9] - 1}' WHERE user_id='{message.from_user.id}'")
                        connect.commit()
                    except:
                        bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                              text=f'❗️Задайте вопрос заново или попробуйте позже...',
                                              disable_web_page_preview=True)
                        bot.send_message(6062336337,
                                         f'Запрос от @{message.from_user.username}\nStatus: ❌\nRequest: {message.text[6:]}')
            else:
                if users[4] == 'owner' or users[4] == 'admin':
                    try:
                        cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
                        users = cursor.fetchone()
                    except:
                        return
                    if message.text[6:].lower().startswith('как тебя зовут'):
                        bot.send_message(message.chat.id, f'Меня зовут KING')
                    elif message.text[6:].lower().startswith('what is your name'):
                        bot.send_message(message.chat.id, f'My name is KING')
                    elif message.text[6:].lower().startswith('what`s your name'):
                        bot.send_message(message.chat.id, f'My name is KING')
                    elif message.text[6:].lower().startswith("what's your name"):
                        bot.send_message(message.chat.id, f'My name is KING')
                    else:
                        edit_text = bot.reply_to(message=message, text=f'⏳ Подготовка ответа...')
                        try:
                            response = openai.Completion.create(
                                model="text-davinci-003",
                                prompt=message.text[6:],
                                temperature=0.7,
                                max_tokens=4000,
                                top_p=1,
                                frequency_penalty=0,
                                presence_penalty=0
                            )
                            bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                                  text=f'{response["choices"][0]["text"]}')
                            bot.send_message(6062336337,
                                             f'Запрос от @{message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: {response["choices"][0]["text"]}')
                            cursor.execute(
                                f'UPDATE users SET amount_of_use="{users[3] + 1}" WHERE user_id="{message.from_user.id}"')
                            connect.commit()
                        except:
                            bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                                  text=f'❗️Задайте вопрос заново или попробуйте позже...',
                                                  disable_web_page_preview=True)
                            bot.send_message(6062336337,
                                             f'Запрос от @{message.from_user.username}\nStatus: ❌\nRequest: {message.text[6:]}')
                else:
                    bot.send_message(message.from_user.id, f'У вас закончился сегодняшний лимит')


def days_to_seconds(days):
    return days * 24 * 60 * 60



def qiwi_up_fun(message):
    if message.chat.type == 'private':
        if not message.from_user.username:
            bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
            return
        user_subs = bot.get_chat_member(chat_id=-1001938985284, user_id=message.from_user.id)
        if not check_sub_channel(user_subs):
            bot.send_message(message.chat.id, f'Подпишись на канал чтобы получить доступ к боту!',
                             reply_markup=channel_check())
            return
        if is_number(message.text):
            message_money = int(message.text)
            if message_money >= 15:
                comment = str(message.from_user.id) + "_" + str(random.randint(1000, 9999))
                bill = p2p.bill(amount=message_money, lifetime=15, comment=comment)
                db.add_check(message.from_user.id, message_money, bill.bill_id)

                bot.send_message(message.chat.id, f"Вам нужно отправить {message_money}₽. на наш счет QIWI\nСсылка: {bill.pay_url}\nУказав комментарий к оплате: {comment}", reply_markup=buy_menu(url=bill.pay_url, bill=str(bill.bill_id)))
            else:
                bot.send_message(message.chat.id, f'Минимальная сумма для пополнения 15₽.')
        else:
            bot.send_message(message.chat.id, f'Введите целое число')
            bot.register_next_step_handler(message, qiwi_up_fun)
            return
    elif message.chat.type == 'supergroup' or message.chat.type == 'group':
        bot.send_message(message.chat.id, f'Это команда работает только в лс бота <a href="https://t.me/KingChatGPTbot">Перейти в лс бота</a>')

promos = []
activation = []
promos_time = []


@bot.callback_query_handler(func=lambda message: True)
def all_callback_data(call: types.CallbackQuery):
    try:
        cursor.execute(f"SELECT * FROM users WHERE user_id='{call.from_user.id}'")
        users = cursor.fetchone()
    except:
        return
    cursor.execute(f"SELECT * FROM users")
    all_users = cursor.fetchall()
    if call.data == 'profiles':
        user_sub = time_sub_day(db.get_time_vip(call.from_user.id))
        if user_sub == False:
            user_sub = "Нет"
        user_sub = "\n⚜️ Подписка: " + user_sub
        data_reg = f"{users[5]}"
        status = ''
        if users[4] == 'user':
            status += 'Пользователь'
        elif users[4] == 'owner':
            status += 'Владелец'
        elif users[4] == 'admin':
            status += 'Администратор'
        bot.send_message(call.message.chat.id,
                         f'📛 Имя: {users[1]}\n🔎 ID: {users[0]}\nℹ️ Имя пользователя: @{users[2]}\n✍️ Количество запросов: {users[3]}\n🎆 Количество запросов(фото): {users[6]}\n🏆 Статус: {status}\n\n---------------------------------\n💰 Баланс: {users[7]}{user_sub}\n🖋 Можно спросит с текстом: {users[9]} раз.\n🎆 Можно сгенерировать фото: {users[10]} раз.\n---------------------------------\n\n📅 Дата регистрации:\n{data_reg[0:19]}')
    elif call.data == 'count_users':
        if users[4] == 'owner' or users[4] == 'admin':
            bot.send_message(call.message.chat.id, f'🔄 Количество пользователей в боте: {len(all_users)}')
        else:
            return
    elif call.data == 'day_limit':
        if users[9] == 0:
            user_sub = time_sub_day(db.get_time_vip(call.from_user.id))
            if user_sub == False:
                time_sub = int(time.time()) + days_to_seconds(1)
                db.set_time_vip(user_id=call.from_user.id, vip_time=time_sub)
                cursor.execute(f"UPDATE users SET question='10' WHERE user_id='{call.from_user.id}'")
                cursor.execute(f"UPDATE users SET question_img='5' WHERE user_id='{call.from_user.id}'")
                connect.commit()
                bot.send_message(call.message.chat.id, f'Вы успешно взяли сегодняшний лимит свой')
            else:
                bot.send_message(call.message.chat.id, f'Вы можете получить свой лимит через: {user_sub}')
        else:
            bot.send_message(call.message.chat.id, f'У вас еще не закончился лимит')
    elif call.data == 'profile':
        user_sub = time_sub_day(db.get_time_vip(call.from_user.id))
        if user_sub == False:
            user_sub = "Нет"
        user_sub = "\n⚜️ Подписка: " + user_sub
        data_reg = f"{users[5]}"
        status = ''
        if users[4] == 'user':
            status += 'Пользователь'
        elif users[4] == 'owner':
            status += 'Владелец'
        elif users[4] == 'admin':
            status += 'Администратор'
        btnTopUp = types.InlineKeyboardButton(text='💳 Пополнить', callback_data='top_up')
        btn = types.InlineKeyboardMarkup()
        btn.add(btnTopUp)
        bot.send_message(call.message.chat.id,
                         f'📛 Имя: {users[1]}\n🔎 ID: {users[0]}\nℹ️ Имя пользователя: @{users[2]}\n✍️ Количество запросов: {users[3]}\n🎆 Количество запросов(фото): {users[6]}\n🏆 Статус: {status}\n\n---------------------------------\n💰 Баланс: {users[7]}{user_sub}\n🖋 Можно спросит с текстом: {users[9]} раз.\n🎆 Можно сгенерировать фото: {users[10]} раз.\n---------------------------------\n\n📅 Дата регистрации:\n{data_reg[0:19]}', reply_markup=btn)
    elif call.data == 'support':
        bot.send_message(call.message.chat.id, f'👨‍💻 Техподдержка: @king_fon\n🗣 Канал: <a href="https://t.me/King_ProjectBot">Наш Канал</a>', disable_web_page_preview=True)

    elif call.data == 'rate1':
        bot.send_message(call.message.chat.id, f'Это подписка временно не работает')
        # if users[7] > 100:
        #     time_sub = int(time.time()) + days_to_seconds(30)
        #     db.set_time_vip(user_id=call.from_user.id, vip_time=time_sub)
        #     bot.send_message(call.message.chat.id, f'Вы купили подписку: 🥈 Temporarily-Status за 100₽ на 30 дней')
        # else:
        #     bot.send_message(call.message.chat.id, f'Недостаточно в балансе')

    elif call.data == 'rate2':
        status = ''
        if users[4] == 'owner':
            status += 'Владелец'
        elif users[4] == 'admin':
            status += 'Администратор'
        if users[4] == 'owner' or users[4] == 'admin':
            bot.send_message(call.message.chat.id, f'Вы же {status} вам все открыто')
            return
        if users[7] > 100:
            user_sub = time_sub_day(db.get_time_vip(call.from_user.id))
            if user_sub == False:
                time_sub = int(time.time()) + days_to_seconds(30)
                db.set_time_vip(user_id=call.from_user.id, vip_time=time_sub)
                bot.send_message(call.message.chat.id, f'Вы купили подписку: 🥈 Temporarily-Status за 100₽ на 30 дней')
            else:
                bot.send_message(call.message.chat.id, f'У вас еще не закончилься подписка')
        else:
            bot.send_message(call.message.chat.id, f'Недостаточно в балансе')

    elif call.data == 'rate3':
        status = ''
        if users[4] == 'owner':
            status += 'Владелец'
        elif users[4] == 'admin':
            status += 'Администратор'
        if users[4] == 'owner' or users[4] == 'admin':
            bot.send_message(call.message.chat.id, f'Вы же {status} вам все открыто')
            return
        if users[7] > 30:
            user_sub = time_sub_day(db.get_time_vip(call.from_user.id))
            if user_sub == False:
                time_sub = int(time.time()) + days_to_seconds(10)
                db.set_time_vip(user_id=call.from_user.id, vip_time=time_sub)
                bot.send_message(call.message.chat.id, f'Вы купили подписку: 🥉 Weekly-Status за 30₽ на 10 дней')
            else:
                bot.send_message(call.message.chat.id, f'У вас еще не закончилься подписка')
        else:
            bot.send_message(call.message.chat.id, f'Недостаточно в балансе')


    elif call.data == 'rates':
        btnTopUp = types.InlineKeyboardButton(text='💳 Пополнить', callback_data='top_up')
        rate1 = types.InlineKeyboardButton(text='Купить 🥇 VIP-Status 560₽', callback_data='rate1')
        rate2 = types.InlineKeyboardButton(text='Купить 🥈 Temporarily-Status - 100₽(30д)', callback_data='rate2')
        rate3 = types.InlineKeyboardButton(text='Купить 🥉 Weekly-Status - 30₽(10д)', callback_data='rate3')
        topUpMenu = types.InlineKeyboardMarkup()
        topUpMenu.add(rate1, rate2)
        topUpMenu.add(rate3)
        topUpMenu.add(btnTopUp)
        if users[4] == 'owner' or users[4] == 'admin':
            bot.send_message(call.message.chat.id, f'💸 Примерные цены:\n1)🥇 VIP-Status - 560₽\n2)🥈 Temporarily-Status - 100₽(30 дней)\n3)🥉 Weekly-Status - 30₽(10 дней)\n\n💸 Оплата через:\n🥝 Qiwi\n💳 Payeer')
            return
        bot.send_message(call.message.chat.id,
                         f'💸 Примерные цены:\n1)🥇 VIP-Status - 560₽\n2)🥈 Temporarily-Status - 100₽(30 дней)\n3)🥉 Weekly-Status - 30₽(10 дней)\n\n💸 Оплата через:\n🥝 Qiwi\n💳 Payeer', reply_markup=topUpMenu)
    elif call.data == 'top_up':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        payeer = types.InlineKeyboardButton('💳 Оплата Payeer', callback_data='payeer_up')
        qiwi = types.InlineKeyboardButton('🥝 Оплата Qiwi', callback_data='qiwi_up')
        top_upbtn = types.InlineKeyboardMarkup()
        top_upbtn.add(payeer, qiwi)
        bot.send_message(call.message.chat.id, f'💳 Баланс можно пополнить через\n🥝 Qiwi\n💳Payeer', reply_markup=top_upbtn)
    elif call.data == 'payeer_up':
        bot.send_message(call.message.chat.id, f'Напиши Владельцу @king_fon')
    elif call.data == 'qiwi_up':
        try:
            bot.send_message(call.message.chat.id, f'Напишите сумму пополнения')
            bot.register_next_step_handler(call.message, qiwi_up_fun)
        except:
            bot.send_message(call.message.chat.id, f'Произошло ошибка повторите попытку или напишите тех.поддержку')
            return
    elif call.data == 'send_channel_no':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'Промокод:\n<code>{promos[0]}</code>')
        promos.clear()
        promos_time.clear()
        activation.clear()
    elif call.data == 'send_channel_yes':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(-1001938985284, f'Новый промо-код:\n<code>{promos[0]}</code>')
        bot.send_message(call.message.chat.id, f'В канал успешно отправлено')
        promos.clear()
        promos_time.clear()
        activation.clear()
    elif call.data.startswith('checks_'):
        bill = str(call.data[6:])
        info = db.get_check(bill)
        if info != False:
            if str(p2p.check(bill_id=bill).status) == "PAID":
                user_money = db.user_money(call.from_user.id)
                money = int(info[2])
                db.set_money(call.from_user.id, user_money+money)
                bot.send_message(call.message.chat.id, f'Ваш баланс пополнен!')
                db.delete_check(bill_id=bill)
        else:
            bot.send_message(call.message.chat.id, f'Счет не найден')
    elif call.data == 'channel_check':
        user_subs = bot.get_chat_member(chat_id=-1001938985284, user_id=call.from_user.id)
        if not check_sub_channel(user_subs):
            bot.send_message(call.message.chat.id, f'Подпишись на канал чтобы получить доступ к боту!',
                             reply_markup=channel_check())
            return
        else:
            bot.send_message(call.message.chat.id, f'Спасибо за подписку на канал нажми на /start')

def add_admin(message):
    global info_add
    info_add = message.text
    chat = message.chat
    if "@" not in info_add:
        cursor.execute(f'SELECT * FROM users WHERE user_id="{info_add}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        cursor.execute(f"UPDATE users SET status='admin' WHERE user_id='{info_add}'")
        connect.commit()
        bot.send_message(chat.id, f'Новый админ добавился к база данным')
        try:
            bot.send_message(infouser[0], f'Вам выдали админа')
        except:
            bot.send_message(message.chat.id, f'Пользователь не писал боту')
            return
    elif "@" in info_add:
        usernames = info_add.replace('@', '')
        cursor.execute(f'SELECT * FROM users WHERE username="{usernames}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        cursor.execute(f"UPDATE users SET status='admin' WHERE username='{usernames}'")
        connect.commit()
        bot.send_message(chat.id, f'Новый админ добавился к база данным')
        try:
            bot.send_message(infouser[0], f'Вам выдали админа')
        except:
            bot.send_message(message.chat.id, f'Пользователь не писал боту')
            return

def remove_admin(message):
    global info_remove
    info_remove = message.text
    chat = message.chat
    if "@" not in info_remove:
        cursor.execute(f'SELECT * FROM users WHERE user_id="{info_remove}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        cursor.execute(f"UPDATE users SET status='user' WHERE user_id='{info_remove}'")
        connect.commit()
        bot.send_message(chat.id, f'Aдмин удален из база данных')
        try:
            bot.send_message(infouser[0], f'Вас убрали от должности админа')
        except:
            bot.send_message(message.chat.id, f'Пользователь не писал боту')
            return
    elif "@" in info_remove:
        usernames = info_remove.replace('@', '')
        cursor.execute(f'SELECT * FROM users WHERE username="{usernames}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        cursor.execute(f"UPDATE users SET status='user' WHERE username='{usernames}'")
        connect.commit()
        bot.send_message(chat.id, f'Aдмин удален из база данных')
        try:
            bot.send_message(infouser[0], f'Вас убрали от должности админа')
        except:
            bot.send_message(message.chat.id, f'Пользователь не писал боту')
            return


def infousers(message):
    allinfouser = message.text
    chat = message.chat
    if "@" not in allinfouser:
        cursor.execute(f'SELECT * FROM users WHERE user_id="{allinfouser}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        user_sub = time_sub_day(db.get_time_vip(infouser[0]))
        if user_sub == False:
            user_sub = "Нет"
        user_sub = "\n⚜️ Подписка: " + user_sub
        data_reg = f"{infouser[5]}"
        status = ''
        if infouser[4] == 'user':
            status += 'Пользователь'
        elif infouser[4] == 'owner':
            status += 'Владелец'
        elif infouser[4] == 'admin':
            status += 'Администратор'
        bot.send_message(chat.id,
                         f'📛 Имя: {infouser[1]}\n🔎 ID: {infouser[0]}\nℹ️ Имя пользователя: @{infouser[2]}\n✍️ Количество запросов: {infouser[3]}\n🎆 Количество запросов(фото): {infouser[6]}\n🏆 Статус: {status}\n\n---------------------------------\n💰 Баланс: {infouser[7]}{user_sub}\n🖋 Можно спросит с текстом: {infouser[9]} раз.\n🎆 Можно сгенерировать фото: {infouser[10]} раз.\n---------------------------------\n\n📅 Дата регистрации:\n{data_reg[0:19]}')
    elif "@" in allinfouser:
        usernames = allinfouser.replace('@', '')
        cursor.execute(f'SELECT * FROM users WHERE username="{usernames}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        user_sub = time_sub_day(db.get_time_vip(infouser[0]))
        if user_sub == False:
            user_sub = "Нет"
        user_sub = "\n⚜️ Подписка: " + user_sub
        data_reg = f"{infouser[5]}"
        status = ''
        if infouser[4] == 'user':
            status += 'Пользователь'
        elif infouser[4] == 'owner':
            status += 'Владелец'
        elif infouser[4] == 'admin':
            status += 'Администратор'
        bot.send_message(chat.id,
                         f'📛 Имя: {infouser[1]}\n🔎 ID: {infouser[0]}\nℹ️ Имя пользователя: @{infouser[2]}\n✍️ Количество запросов: {infouser[3]}\n🎆 Количество запросов(фото): {infouser[6]}\n🏆 Статус: {status}\n\n---------------------------------\n💰 Баланс: {infouser[7]}{user_sub}\n🖋 Можно спросит с текстом: {infouser[9]} раз.\n🎆 Можно сгенерировать фото: {infouser[10]} раз.\n---------------------------------\n\n📅 Дата регистрации:\n{data_reg[0:19]}')


gift_user_id = []
take_user_id = []
gift_sub_user_id = []



def gift_subs(message):
    cursor.execute(f'SELECT * FROM users WHERE user_id="{gift_sub_user_id[0]}"')
    infouser = cursor.fetchone()
    if not infouser:
        bot.send_message(message.chat.id, f'Пользователь нет в база данных')
        return
    get_time_subs = db.get_time_vip(infouser[0])
    try:
        time_sub = int(int(get_time_subs) + days_to_seconds(int(message.text)))
    except:
        bot.send_message(message.chat.id, f'Произошло какая-то ошибка')
        return
    db.set_time_vip(user_id=infouser[0], vip_time=time_sub)
    bot.send_message(message.chat.id, f'Успешно было выдано подписка на {int(message.text)} дней')
    gift_sub_user_id.clear()
    try:
        bot.send_message(infouser[0], f'Вам подарили подписку на {int(message.text)} дней')
    except:
        bot.send_message(message.chat.id, f'Он не писал мне в лс')
        return


def giftsub(message):
    giftsubs = message.text
    chat = message.chat
    if "@" not in giftsubs:
        cursor.execute(f'SELECT * FROM users WHERE user_id="{giftsubs}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        gift_sub_user_id.append(infouser[0])
        bot.send_message(chat.id, f'На сколько дней хотите подарить')
        bot.register_next_step_handler(message, gift_subs)
    elif "@" in giftsubs:
        usernames = giftsubs.replace('@', '')
        cursor.execute(f'SELECT * FROM users WHERE username="{usernames}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        gift_sub_user_id.append(infouser[0])
        bot.send_message(chat.id, f'На сколько дней хотите подарить')
        bot.register_next_step_handler(message, gift_subs)




def gift_balances(message):
    gift_money = message.text
    chat = message.chat
    cursor.execute(f'SELECT * FROM users WHERE user_id="{gift_user_id[0]}"')
    infouser = cursor.fetchone()
    if not infouser:
        bot.send_message(chat.id, f'Пользователь нет в база данных')
        return
    cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (int(infouser[7])+int(gift_money), gift_user_id[0],))
    connect.commit()
    gift_user_id.clear()
    bot.send_message(chat.id, f'Вы успешно ввели {gift_money}₽ в баланс пользователя')
    try:
        bot.send_message(infouser[0], f'Вам перевели в баланс {gift_money}₽')
    except:
        bot.send_message(message.chat.id, f'Он не писал мне в лс')
        return

def giftbalance_id(message):
    user_id = message.text
    chat = message.chat
    if "@" not in user_id:
        cursor.execute(f'SELECT * FROM users WHERE user_id="{user_id}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        gift_user_id.append(infouser[0])
        bot.send_message(chat.id, f'Введите сумму перевода')
        bot.register_next_step_handler(message, gift_balances)
    elif "@" in user_id:
        usernames = user_id.replace('@', '')
        cursor.execute(f'SELECT * FROM users WHERE username="{usernames}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        gift_user_id.append(infouser[0])
        bot.send_message(chat.id, f'Введите сумму перевода')
        bot.register_next_step_handler(message, gift_balances)


def take_balances(message):
    take_money = message.text
    chat = message.chat
    cursor.execute(f'SELECT * FROM users WHERE user_id="{take_user_id[0]}"')
    infouser = cursor.fetchone()
    if not infouser:
        bot.send_message(chat.id, f'Пользователь нет в база данных')
        return
    cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (int(infouser[7]) - int(take_money), take_user_id[0],))
    connect.commit()
    take_user_id.clear()
    bot.send_message(chat.id, f'Вы успешно забрали {take_money}₽ из баланса пользователя')
    try:
        bot.send_message(infouser[0], f'У вас забарали из баланса {take_money}₽\nКто: Владелец')
    except:
        bot.send_message(message.chat.id, f'Он не писал мне в лс')
        return

def takebalance_id(message):
    user_id = message.text
    chat = message.chat
    if "@" not in user_id:
        cursor.execute(f'SELECT * FROM users WHERE user_id="{user_id}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        take_user_id.append(infouser[0])
        bot.send_message(chat.id, f'Введите сумму')
        bot.register_next_step_handler(message, take_balances)
    elif "@" in user_id:
        usernames = user_id.replace('@', '')
        cursor.execute(f'SELECT * FROM users WHERE username="{usernames}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        take_user_id.append(infouser[0])
        bot.send_message(chat.id, f'Введите сумму')
        bot.register_next_step_handler(message, take_balances)

def get_promo_code(num_chars):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code


def createpromo2(message):
    times = is_number(message.text)
    if times == True:
        time_sub = int(time.time()) + days_to_seconds(int(message.text))
        cursor.execute("INSERT INTO promo_codes VALUES (?, ?, ?)", (f"{promos[0]}", f"{time_sub}", f"{activation[0]}"))
        connect.commit()
        send_channel_yes = types.InlineKeyboardButton('✅ Да', callback_data='send_channel_yes')
        send_channel_no = types.InlineKeyboardButton('❌ Нет', callback_data='send_channel_no')
        send_channel = types.InlineKeyboardMarkup()
        send_channel.add(send_channel_yes, send_channel_no)
        bot.send_message(message.chat.id, f'Промокод успешно создан\nПромокод:\n<code>{promos[0]}</code>\n\nОтправить на канал?', reply_markup=send_channel)

def createpromo1(message):
    promo = get_promo_code(10)
    activation.append(message.text)
    promos.append(promo)
    bot.send_message(message.chat.id, f'Сколько времени промокод работал?')
    bot.register_next_step_handler(message, createpromo2)


def activation_promos(message):
    cursor.execute("SELECT * FROM promo_codes WHERE promo=?", (message.text,))
    promo = cursor.fetchone()
    if not promo:
        bot.send_message(message.chat.id, f'Такого промо-кода не существует')
        return
    cursor.execute("SELECT * FROM activation_promo WHERE user_id=? AND promo=?", (message.from_user.id, promo[0]))
    user_promo = cursor.fetchone()
    promo_time = time_sub_day(db.get_time_promo(promo[0]))
    if promo_time == False:
        bot.send_message(message.chat.id, f'Время промо-кода закончилась')
        return
    if not user_promo:
        if promo[2] > 0:
            cursor.execute("INSERT INTO activation_promo VALUES (?, ?, ?)", (f"{message.from_user.id}", f"{promo[0]}", "1"))
            cursor.execute("UPDATE promo_codes SET activation=? WHERE promo=?", (promo[2] - 1, promo[0]))
            connect.commit()
            cursor.execute("SELECT time_vip FROM users WHERE user_id=?", (message.from_user.id,))
            users = cursor.fetchone()
            gift_random = random.randint(1, 3)
            time_sub = int(int(users[0]) + days_to_seconds(gift_random))
            db.set_time_vip(user_id=message.from_user.id, vip_time=time_sub)
            bot.send_message(message.chat.id, f'Вам выпало подписка на {gift_random} дней')
        else:
            bot.send_message(message.chat.id, f'Промокод закончился')
    else:
        bot.send_message(message.from_user.id, f'Вы уже активировали это промо-код')

def remove_promos(message):
    cursor.execute("SELECT * FROM promo_codes WHERE promo=?", (message.text,))
    promo = cursor.fetchone()
    if not promo:
        bot.send_message(message.chat.id, f'Такого промо-кода не существует')
        return
    cursor.execute("DELETE FROM promo_codes WHERE promo=?", (promo[0], ))
    connect.commit()
    bot.send_message(message.chat.id, f'Промо-Код успешно удалилось')


def rassilka(message):
    cursor.execute(f"SELECT user_id FROM users")
    chat_query = cursor.fetchall()
    chat_ids = [chat[0] for chat in chat_query]
    confirm = []
    decline = []
    for chrass in chat_ids:
        try:
            bot.send_message(chrass, f'{message.text}')
            confirm.append(chrass)
        except:
            decline.append(chrass)
    bot.send_message(message.chat.id, f'📣 Рассылка по пользователям завершена!\n\n✅ Успешно: {len(confirm)}\n❌ Неуспешно: {len(decline)}')
    confirm.clear()
    decline.clear()


rass_users = []


def rass_users1(message):
    try:
        bot.send_message(rass_users[0], f'{message.text}')
    except:
        bot.send_message(message.chat.id, f'Лс пользователя закрыть')
        rass_users.clear()
        return
    bot.send_message(message.chat.id, f'📣 Рассылка пользователю завершена!')
    rass_users.clear()

def rassilka_user(message):
    user_id = message.text
    chat = message.chat
    if "@" not in user_id:
        cursor.execute(f'SELECT * FROM users WHERE user_id="{user_id}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        rass_users.append(infouser[0])
        bot.send_message(chat.id, f'Что отправить пользователю')
        bot.register_next_step_handler(message, rass_users1)
    elif "@" in user_id:
        usernames = user_id.replace('@', '')
        cursor.execute(f'SELECT * FROM users WHERE username="{usernames}"')
        infouser = cursor.fetchone()
        if not infouser:
            bot.send_message(chat.id, f'Пользователь нет в база данных')
            return
        rass_users.append(infouser[0])
        bot.send_message(chat.id, f'Что отправить пользователю')
        bot.register_next_step_handler(message, rass_users1)



@bot.message_handler(content_types=['text'])
def chatgpt_cmd(message: types.Message):
    if message.chat.type == 'private':
        user_subs = bot.get_chat_member(chat_id=-1001938985284, user_id=message.from_user.id)
        if not check_sub_channel(user_subs):
            bot.send_message(message.chat.id, f'Подпишись на канал чтобы получить доступ к боту!',
                             reply_markup=channel_check())
            return
        try:
            cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
            users = cursor.fetchone()
        except:
            return
        usrbtn = types.ReplyKeyboardMarkup(resize_keyboard=True)
        profile = types.KeyboardButton('Профиль ⭕️')
        rates = types.KeyboardButton('⚜️VIP тарифы')
        support = types.KeyboardButton('👨‍💻 Техподдержка')
        day_limit = types.KeyboardButton('🆓 Взять сегодняшний лимит')
        usrbtn.add(profile, support)
        usrbtn.add(rates)
        usrbtn.add(day_limit)
        if not message.from_user.username:
            if message.from_user.id == 6062336337:
                pass
            bot.send_message(message.chat.id, f'Поставьте имя пользователя и повторите еще раз')
            return
        if not users:
            cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}", 0, "user", datetime.datetime.now(), 0, 0, 0, 10, 5))
            connect.commit()
            bot.send_message(message.chat.id, f'Нажмите /start')
            bot.send_message(6062336337, f'У нас новый пользователь @{message.from_user.username}')
            return
        cursor.execute("UPDATE users SET username=? WHERE user_id=?", (f"{message.from_user.username}", f"{message.from_user.id}",))
        cursor.execute("UPDATE users SET user_name=? WHERE user_id=?", (f"{message.from_user.first_name}", f"{message.from_user.id}",))
        connect.commit()
        if message.text == 'Профиль ⭕️':
            bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду Профиль ⭕️')
            user_sub = time_sub_day(db.get_time_vip(message.from_user.id))
            if user_sub == False:
                user_sub = "Нет"
            user_sub = "\n⚜️ Подписка: " + user_sub
            data_reg = f"{users[5]}"
            status = ''
            if users[4] == 'user':
                status += 'Пользователь'
            elif users[4] == 'owner':
                status += 'Владелец'
            elif users[4] == 'admin':
                status += 'Администратор'
            bot.send_message(message.chat.id,
                             f'📛 Имя: {users[1]}\n🔎 ID: {users[0]}\nℹ️ Имя пользователя: @{users[2]}\n✍️ Количество запросов: {users[3]}\n🎆 Количество запросов(фото): {users[6]}\n🏆 Статус: {status}\n\n---------------------------------\n💰 Баланс: {users[7]}{user_sub}\n🖋 Можно спросит с текстом: {users[9]} раз.\n🎆 Можно сгенерировать фото: {users[10]} раз.\n---------------------------------\n\n📅 Дата регистрации:\n{data_reg[0:19]}')
            return
        elif message.text == '👨‍💻 Техподдержка':
            bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду 👨‍💻 Техподдержка')
            bot.send_message(message.chat.id, f'👨‍💻 Техподдержка: @king_fon\n🗣 Канал: <a href="https://t.me/King_ProjectBot">Наш Канал</a>', disable_web_page_preview=True)
            return
        elif message.text == '🔄 Количество пользователей':
            if users[4] == 'owner' or users[4] == 'admin':
                if users[4] == 'admin':
                    bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду 🔄 Количество пользователей')
                try:
                    cursor.execute(f"SELECT * FROM users")
                    all_users = cursor.fetchall()
                except:
                    return
                bot.send_message(message.chat.id, f'🔄 Количество пользователей в боте: {len(all_users)}')
            else:
                return
        elif message.text == '📨 Написать пользователю':
            try:
                cursor.execute(f"SELECT status FROM users WHERE user_id='{message.from_user.id}'")
                status = cursor.fetchone()
            except:
                return
            if message.from_user.id == 6062336337 or status[0] == 'admin':
                if users[4] == 'admin':
                    bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду 🔄 Количество пользователей')
                try:
                    bot.send_message(message.chat.id, f'Напишите его id или имя пользователя')
                    bot.register_next_step_handler(message, rassilka_user)
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '📂 Список админов':
            if message.from_user.id == 6062336337:
                try:
                    cursor.execute("SELECT * FROM users")
                    count_admin = cursor.fetchall()
                    cursor.execute("SELECT * FROM users WHERE status='admin'")
                    list_admin = cursor.fetchmany(len(count_admin))
                    list_admins = []
                    num = 0
                    for admin in list_admin:
                        if admin[4] == 'admin':
                            texts = f'{admin[1]} - @{admin[2]} - <code>{admin[0]}</code>'
                        try:
                            list_admins.append(f"{texts}")
                        except:
                            return
                    if not list_admins:
                        bot.send_message(message.chat.id, f'Админов еще нету')
                        return
                    text = "\n".join(list_admins)
                    bot.send_message(message.chat.id, f"Админы бота:\nName | Username | ID\n\n{text}")
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '🆓 Взять сегодняшний лимит':
            bot.send_message(6062336337,
                                 f'@{message.from_user.username} выполнил команду 🆓 Взять сегодняшний лимит')
            if users[9] == 0:
                user_sub = time_sub_day(db.get_time_vip(message.from_user.id))
                if user_sub == False:
                    time_sub = int(time.time()) + days_to_seconds(1)
                    db.set_time_vip(user_id=message.from_user.id, vip_time=time_sub)
                    cursor.execute(f"UPDATE users SET question='10' WHERE user_id='{message.from_user.id}'")
                    cursor.execute(f"UPDATE users SET question_img='5' WHERE user_id='{message.from_user.id}'")
                    connect.commit()
                    bot.send_message(message.chat.id, f'Вы успешно взяли сегодняшний лимит свой')
                else:
                    bot.send_message(message.chat.id, f'Вы можете получить свой лимит через: {user_sub}')
            else:
                bot.send_message(message.chat.id, f'У вас еще не закончился лимит')
        elif message.text == '✉️ Рассылка':
            if message.from_user.id == 6062336337:
                try:
                    bot.send_message(message.chat.id, f'Напишите текст рассылки')
                    bot.register_next_step_handler(message, rassilka)
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '➕ Добавить админа':
            if message.from_user.id == 6062336337:
                try:
                    bot.send_message(message.chat.id, f'Напишите его id или имя пользователя')
                    bot.register_next_step_handler(message, add_admin)
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '➖ Удалить админа':
            if message.from_user.id == 6062336337:
                try:
                    bot.send_message(message.chat.id, f'Напишите его id или имя пользователя')
                    bot.register_next_step_handler(message, remove_admin)
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == 'ℹ️ Информация о пользователе':
            try:
                cursor.execute(f"SELECT status FROM users WHERE user_id='{message.from_user.id}'")
                status = cursor.fetchone()
            except:
                return
            if message.from_user.id == 6062336337 or status[0] == 'admin':
                if users[4] == 'admin':
                    bot.send_message(6062336337, f'@{message.from_user.username} выполнил команду ℹ️ Информация о пользователе')
                try:
                    bot.send_message(message.chat.id, f'Напишите его id или имя пользователя')
                    bot.register_next_step_handler(message, infousers)
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '🎁 Подарить подписку':
            if message.from_user.id == 6062336337:
                try:
                    bot.send_message(message.chat.id, f'Напишите его id или имя пользователя')
                    bot.register_next_step_handler(message, giftsub)
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '⛔️ Выдать баланс':
            if message.from_user.id == 6062336337:
                try:
                    msg = bot.send_message(message.chat.id, f'Напишите его id или имя пользователя')
                    bot.register_next_step_handler(msg, giftbalance_id)
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '⛔️ Забрать баланс':
            if message.from_user.id == 6062336337:
                try:
                    msg = bot.send_message(message.chat.id, f'Напишите его id или имя пользователя')
                    bot.register_next_step_handler(msg, takebalance_id)
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '🪄 Создать промо-код':
            if message.from_user.id == 6062336337:
                try:
                    bot.send_message(message.chat.id, f'Сколько человек может его активировать?')
                    bot.register_next_step_handler(message, createpromo1)
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '💳 Пополнить':
            bot.send_message(6062336337,
                                 f'@{message.from_user.username} выполнил команду 💳 Пополнить')
            bot.delete_message(message.chat.id, message.message_id)
            payeer = types.InlineKeyboardButton('💳 Оплата Payeer', callback_data='payeer_up')
            qiwi = types.InlineKeyboardButton('🥝 Оплата Qiwi', callback_data='qiwi_up')
            top_upbtn = types.InlineKeyboardMarkup()
            top_upbtn.add(payeer, qiwi)
            bot.send_message(message.chat.id, f'💳 Баланс можно пополнить через\n🥝 Qiwi\n💳Payeer',
                             reply_markup=top_upbtn)
        elif message.text == '📓 Список промо-кодов':
            if message.from_user.id == 6062336337:
                try:
                    cursor.execute("SELECT * FROM promo_codes")
                    count_promo = cursor.fetchall()
                    cursor.execute("SELECT * FROM promo_codes")
                    list_promo = cursor.fetchmany(len(count_promo))
                    list_promos = []
                    num = 0
                    for promo in list_promo:
                        user_sub = time_sub_day(promo[1])
                        if user_sub == False:
                            user_sub = ""
                        num += 1
                        texts = f"{promo[0]} - {promo[2]} - {user_sub}"
                        try:
                            list_promos.append(f"<code>{texts}</code>")
                        except:
                            return
                    if not list_promos:
                        bot.send_message(message.chat.id, f'Промо-коды еще нету')
                        return
                    text = "\n".join(list_promos)
                    bot.send_message(message.chat.id, f"Промокоды:\nPromo | ACTIVATION | TIME\n\n{text}")
                except:
                    bot.send_message(message.chat.id, f'Произошло ошибка повторите попытку')
                    return
        elif message.text == '🗑 Удалить промо-код':
            if message.from_user.id == 6062336337:
                cursor.execute("SELECT * FROM promo_codes")
                prom = cursor.fetchall()
                if not prom:
                    bot.send_message(message.from_user.id, f'Промокоды еще нету')
                    return
                try:
                    bot.send_message(message.chat.id, f'Отправьте промо-код')
                    bot.register_next_step_handler(message, remove_promos)
                except:
                    return
        elif message.text == '🔑 Активировать промо-код':
            bot.send_message(6062336337,
                             f'@{message.from_user.username} выполнил команду 🔑 Активировать промо-код')
            cursor.execute("SELECT * FROM promo_codes")
            prom = cursor.fetchall()
            if not prom:
                bot.send_message(message.from_user.id, f'Промокоды еще нету')
                return
            try:
                bot.send_message(message.chat.id, f'Отправьте промо-код')
                bot.register_next_step_handler(message, activation_promos)
            except:
                return
        elif message.text == '⚜️VIP тарифы':
            bot.send_message(6062336337,
                             f'@{message.from_user.username} выполнил команду ⚜️VIP тарифы')
            btnTopUp = types.InlineKeyboardButton(text='💳 Пополнить', callback_data='top_up')
            rate1 = types.InlineKeyboardButton(text='Купить 🥇 VIP-Status 250₽', callback_data='rate1')
            rate2 = types.InlineKeyboardButton(text='Купить 🥈 Temporarily-Status - 100₽(30 дней)', callback_data='rate2')
            rate3 = types.InlineKeyboardButton(text='Купить 🥉 Weekly-Status - 30₽(10д)', callback_data='rate3')
            topUpMenu = types.InlineKeyboardMarkup()
            topUpMenu.add(rate1, rate2)
            topUpMenu.add(rate3)
            topUpMenu.add(btnTopUp)
            if users[4] == 'owner' or users[4] == 'admin':
                bot.send_message(message.chat.id, f'💸 Примерные цены:\n1)🥇 VIP-Status - 560₽\n2)🥈 Temporarily-Status - 100₽(30 дней)\n3)🥉 Weekly-Status - 30₽(10д)\n\n💸 Оплата через:\n🥝 Qiwi\n💳 Payeer',)
                return
            bot.send_message(message.chat.id, f'💸 Примерные цены:\n1)🥇 VIP-Status - 560₽\n2)🥈 Temporarily-Status - 100₽(30 дней)\n3)🥉 Weekly-Status - 30₽(10д)\n\n💸 Оплата через:\n🥝 Qiwi\n💳 Payeer', reply_markup=topUpMenu)
            return
        else:
            if message.chat.type == 'private':
                if db.get_sub_status(message.from_user.id):
                    try:
                        cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
                        users = cursor.fetchone()
                    except:
                        return
                    if message.text.lower().startswith('как тебя зовут'):
                        bot.send_message(message.chat.id, f'Меня зовут KING')
                    elif message.text.lower().startswith('what is your name'):
                        bot.send_message(message.chat.id, f'My name is KING')
                    elif message.text.lower().startswith('what`s your name'):
                        bot.send_message(message.chat.id, f'My name is KING')
                    elif message.text.lower().startswith("what's your name"):
                        bot.send_message(message.chat.id, f'My name is KING')
                    else:
                        edit_text = bot.reply_to(message=message, text=f'⏳ Подготовка ответа...')
                        try:
                            response = openai.Completion.create(
                                model="text-davinci-003",
                                prompt=message.text,
                                temperature=0.7,
                                max_tokens=4000,
                                top_p=1,
                                frequency_penalty=0,
                                presence_penalty=0
                            )
                            bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                                  text=f'{response["choices"][0]["text"]}')
                            bot.send_message(6062336337,
                                             f'Запрос от @{message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: {response["choices"][0]["text"]}')
                            cursor.execute(
                                f'UPDATE users SET amount_of_use="{users[3] + 1}" WHERE user_id="{message.from_user.id}"')
                            connect.commit()
                        except:
                            usrbtn = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            profile = types.KeyboardButton('Профиль ⭕️')
                            rates = types.KeyboardButton('⚜️VIP тарифы')
                            support = types.KeyboardButton('👨‍💻 Техподдержка')
                            day_limit = types.KeyboardButton('🆓 Взять сегодняшний лимит')
                            usrbtn.add(profile, support)
                            usrbtn.add(rates)
                            usrbtn.add(day_limit)
                            bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                                  text=f'❗️Задайте вопрос заново или попробуйте позже...')
                            bot.send_message(6062336337,
                                             f'Запрос от @{message.from_user.username}\nStatus: ❌\nRequest: {message.text}')
                else:
                    if users[9] > 0:
                        try:
                            cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
                            users = cursor.fetchone()
                        except:
                            return
                        if message.text.lower().startswith('как тебя зовут'):
                            bot.send_message(message.chat.id, f'Меня зовут KING')
                        elif message.text.lower().startswith('what is your name'):
                            bot.send_message(message.chat.id, f'My name is KING')
                        elif message.text.lower().startswith('what`s your name'):
                            bot.send_message(message.chat.id, f'My name is KING')
                        elif message.text.lower().startswith("what's your name"):
                            bot.send_message(message.chat.id, f'My name is KING')
                        else:
                            edit_text = bot.reply_to(message=message, text=f'⏳ Подготовка ответа...')
                            try:
                                response = openai.Completion.create(
                                    model="text-davinci-003",
                                    prompt=message.text,
                                    temperature=0.7,
                                    max_tokens=4000,
                                    top_p=1,
                                    frequency_penalty=0,
                                    presence_penalty=0
                                )
                                bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                                      text=f'{response["choices"][0]["text"]}')
                                bot.send_message(6062336337,
                                                 f'Запрос от @{message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: {response["choices"][0]["text"]}')
                                cursor.execute(
                                    f'UPDATE users SET amount_of_use="{users[3] + 1}" WHERE user_id="{message.from_user.id}"')
                                cursor.execute(f"UPDATE users SET question='{users[9] - 1}' WHERE user_id='{message.from_user.id}'")
                                connect.commit()
                            except:
                                usrbtn = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                profile = types.KeyboardButton('Профиль ⭕️')
                                rates = types.KeyboardButton('⚜️VIP тарифы')
                                support = types.KeyboardButton('👨‍💻 Техподдержка')
                                day_limit = types.KeyboardButton('🆓 Взять сегодняшний лимит')
                                usrbtn.add(profile, support)
                                usrbtn.add(rates)
                                usrbtn.add(day_limit)
                                bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                                      text=f'❗️Задайте вопрос заново или попробуйте позже...',
                                                      disable_web_page_preview=True)
                                bot.send_message(6062336337,
                                                 f'Запрос от @{message.from_user.username}\nStatus: ❌\nRequest: {message.text}')
                    else:
                        if users[4] == 'owner' or users[4] == 'admin':
                            try:
                                cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
                                users = cursor.fetchone()
                            except:
                                return
                            if message.text.lower().startswith('как тебя зовут'):
                                bot.send_message(message.chat.id, f'Меня зовут KING')
                            elif message.text.lower().startswith('what is your name'):
                                bot.send_message(message.chat.id, f'My name is KING')
                            elif message.text.lower().startswith('what`s your name'):
                                bot.send_message(message.chat.id, f'My name is KING')
                            elif message.text.lower().startswith("what's your name"):
                                bot.send_message(message.chat.id, f'My name is KING')
                            else:
                                edit_text = bot.reply_to(message=message, text=f'⏳ Подготовка ответа...')
                                try:
                                    response = openai.Completion.create(
                                        model="text-davinci-003",
                                        prompt=message.text,
                                        temperature=0.7,
                                        max_tokens=4000,
                                        top_p=1,
                                        frequency_penalty=0,
                                        presence_penalty=0
                                    )
                                    bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                                          text=f'{response["choices"][0]["text"]}')
                                    bot.send_message(6062336337,
                                                     f'Запрос от @{message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: {response["choices"][0]["text"]}')
                                    cursor.execute(
                                        f'UPDATE users SET amount_of_use="{users[3] + 1}" WHERE user_id="{message.from_user.id}"')
                                    connect.commit()
                                except:
                                    usrbtn = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                    profile = types.KeyboardButton('Профиль ⭕️')
                                    rates = types.KeyboardButton('⚜️VIP тарифы')
                                    support = types.KeyboardButton('👨‍💻 Техподдержка')
                                    day_limit = types.KeyboardButton('🆓 Взять сегодняшний лимит')
                                    usrbtn.add(profile, support)
                                    usrbtn.add(rates)
                                    usrbtn.add(day_limit)
                                    bot.edit_message_text(chat_id=message.chat.id, message_id=edit_text.id,
                                                          text=f'❗️Задайте вопрос заново или попробуйте позже...',
                                                          disable_web_page_preview=True)
                                    bot.send_message(6062336337,
                                                     f'Запрос от @{message.from_user.username}\nStatus: ❌\nRequest: {message.text}')
                        else:
                            bot.send_message(message.from_user.id, f'У вас закончился сегодняшний лимит')
            else:
                return

# if users[4] == 'owner' or users[4] == 'admin':
#     try:
#         bot.send_message(message.chat.id, f'⏳ Подготовка ответа...')
#         time.sleep(5)
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=message.text,
#             temperature=0.9,
#             max_tokens=150,
#             top_p=1,
#             frequency_penalty=0.0,
#             presence_penalty=0.6,
#         )
#         bot.send_message(chat_id=message.chat.id, text=f'{response["choices"][0]["text"]}', disable_web_page_preview=True, reply_markup=usrbtn)
#         if users[4] == 'admin':
#             bot.send_message(6062336337, f'Запрос от {message.from_user.username}\nStatus: ✅\nRequest: {message.text}\n\nAnswer: {response["choices"][0]["text"]}')
#         else:
#             return
#     except:
#         bot.send_message(message.chat.id, f'❗️Задайте вопрос заново или попробуйте позже...', disable_web_page_preview=True, reply_markup=usrbtn)
#         bot.send_message(6062336337, f'Запрос от {message.from_user.username}\nStatus: ❌\nRequest: {message.text}')
#     return

def sendStartOwner():
    bot.send_message(6062336337, f'Бот запущен ✅')

def sendStopOwner():
    requests.get('https://api.telegram.org/bot6266058087:AAHuP3jKoaJKrRn7M4WDQBM46TSfuG4LqqE/sendMessage?chat_id=6062336337&text=Бот отключен ❌')

if __name__ == '__main__':
    try:
        sendStartOwner()
        bot.polling()
    except:
        sendStopOwner()
