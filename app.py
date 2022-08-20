import telebot
from config import KEYS, TOKEN
from extensions import CurrencyConvertor, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n' \
           '<имя валюты цену которой хотите узнать> ' \
           '<имя валюты в которой надо узнать цену первой валюты> ' \
           '<количество первой валюты>\n' \
           'Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in KEYS.keys():
        text = text + '\n' + key
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        answer = CurrencyConvertor.handle_message(message.text)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, answer)


bot.polling()
