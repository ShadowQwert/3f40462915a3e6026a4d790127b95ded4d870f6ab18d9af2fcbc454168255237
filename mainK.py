import telebot
from telebot import types
import sqlite3
from steam import make_trade_1_item
from steampy.client import SteamClient
# создаем бота
bot = telebot.TeleBot('')

conn = sqlite3.connect('mainBase.db', check_same_thread=False)
cursor = conn.cursor()


cur_balance = 400
key_value = 150
num_keys = 0

# обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    userid = message.from_user.id
    username = message.from_user.username
    cursor.execute(f'SELECT COUNT(1) FROM userData WHERE userid={userid}')
    test1 = cursor.fetchone()
    if test1[0] == 0:
        cursor.execute('INSERT INTO userData (userid, username) VALUES (?, ?)', (userid, username))
        conn.commit()
    else:
        print('already exists')

    cursor.execute(f'SELECT balance FROM userData WHERE userid={userid}')
    balance1 = cursor.fetchone()[0]

    # создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    key_buy_btn = types.KeyboardButton('Купить ключ')
    support_btn = types.KeyboardButton('Поддержка')
    cash_btn = types.KeyboardButton('Пополнить баланс')
    keyboard.add(key_buy_btn, cash_btn, support_btn)

    bot.reply_to(message, f"Текущий баланс: {balance1}", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Поддержка')
def count_handler(message):
    bot.reply_to(message, "По вопросам писать: @JustF32"
                          "@shadowqwert")

# обработчик нажатия на кнопку Тест
@bot.message_handler(func=lambda message: message.text == 'Купить ключ')
def count_handler(message):
    # создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    menu_button = types.KeyboardButton('В меню')
    keyboard.add(menu_button)
    # отправляем сообщение с выбором меню и клавиатурой
    bot.reply_to(message, "Введите колличество:", reply_markup=keyboard)
    bot.register_next_step_handler(message, check_value1)

@bot.message_handler(func=lambda message: message.text == 'Пополнить баланс')
def count_handler(message):
    bot.reply_to(message, 'Отправьте на указанный киви кошелек <сам кошелек> от 10 до 500р и введите свой ник в примечании. Баланс будет зачислен в течении часа')

def check_value1(message):
    global num_keys
    cursor.execute(f'SELECT balance FROM userData WHERE userid={message.from_user.id}')
    balance1 = cursor.fetchone()[0]

    if message.text == 'В меню':
        back_to_menu_handler(message)
    num_keys = int(message.text)
    if balance1 < num_keys * key_value:
        bot.reply_to(message, "Недостаточно средств")
    else:
        cursor.execute(f"SELECT tradelink FROM userData WHERE userid = {message.from_user.id}")
        tradelink = cursor.fetchone()[0]
        if tradelink == '':
            addlink(message.text, message.from_user.id)
            bot.reply_to(message, "Введите ссыдку на трейд")
            bot.register_next_step_handler(message, trade)
        else:
            if gotrade(tradelink):
                balance1 -= num_keys * key_value
                conn.execute(f'UPDATE userData SET balance = ? WHERE userid = ?', (f'{balance1}', message.from_user.id))
                conn.commit()
                bot.reply_to(message, f"Успешно")
                num_keys = 0
                back_to_menu_handler(message)

def trade(message):
    global cur_balance, num_keys

    cursor.execute(f'SELECT balance FROM userData WHERE userid={message.from_user.id}')
    balance1 = cursor.fetchone()[0]

    if message.text == 'В меню':
        back_to_menu_handler(message)

    addlink(message.text, message.from_user.id)

    cursor.execute(f"SELECT tradelink FROM userData WHERE userid = {message.from_user.id}")
    tradelink = cursor.fetchone()[0]
    if gotrade(tradelink):
        balance1 -= num_keys * key_value
        conn.execute(f'UPDATE userData SET balance = ? WHERE userid = ?', (f'{balance1}', message.from_user.id))
        conn.commit()
        bot.reply_to(message, f"Успешно")
        num_keys = 0
        back_to_menu_handler(message)

# обработчик нажатия на кнопку В меню
@bot.message_handler(func=lambda message: message.text == 'В меню')
def back_to_menu_handler(message):
    send_welcome(message)

# обработчик нажатия на кнопку Тестирование
@bot.message_handler(func=lambda message: message.text == 'Тестирование')
def test_complete_handler(message):
    # отправляем сообщение о завершении тестирования
    bot.reply_to(message, "Тестирование завершено!")


def addlink(link, id2):
    conn.execute(f'UPDATE userData SET tradelink = ? WHERE userid = ?', (f'{link}', id2))
    conn.commit()
# Тут мы добавляем ссылку

def gotrade(link):
    tradeStatus = True
    steam_client = SteamClient('3B24111B3C934BD1FED5873AF3664560')
    steam_client.login('ai905818403', 'ZdPgbnEmoa', 'steamguard.json')
    make_trade_1_item('Mann Co. Supply Crate Key', 'Mann Co. Supply Crate Key', link)

    #Здесь нужно сделать трейд сам#
    if tradeStatus:
        return True
    else:
        print('error')
        return False
# Трейдим ключи


# запускаем бота
bot.polling()