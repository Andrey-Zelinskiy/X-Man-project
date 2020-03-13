import telebot
from telebot import types
import apiai
import json


# class Person:
#     def __init__(self, id, trup):
#         self.__id = id
#         self.__trup = trup

#     @property
#     def id(self):
#         return self.__id, self.__trup


bot = telebot.TeleBot('973098900:AAEOGKTQi6EgaDLpyjm3D_0YsVdcQwXhgMw')

mark = types.ReplyKeyboardMarkup(True, True)
mark.row_width
mark.row('Давай поговорим')
mark.row('Потуши свет')


keybord2 = types.ReplyKeyboardMarkup(True, True)
keybord2.row('Закончить беседу')

list_person = dict()


@bot.message_handler(commands=["start"])
def start(mes):
    list_person[mes.chat.id] = False
    bot.send_message(
        mes.chat.id, "Привет это чат бот для додиков, в данный момент бот находиться в разработке", reply_markup=mark)
    print(mes.from_user.id)


@bot.message_handler(content_types=["text"])
def call(mes):
    if list_person[mes.chat.id]:
        if mes.text.lower() == "закончить беседу":
            list_person[mes.chat.id] = False
            bot.send_message(mes.chat.id, "Ну ладно,поговрим потом.")
        else:
            request = apiai.ApiAI(
                '2c0a2c59f7b546e08504ab43b013a8e8').text_request()
            request.lang = 'ru'
            request.session_id = 'BatlabAIBot'
            request.query = mes.text
            responseJSON = json.loads(
                request.getresponse().read().decode('utf-8'))
            response = responseJSON['result']['fulfillment']['speech']
            if response:
                bot.send_message(mes.chat.id, response)
            else:
                bot.send_message(mes.chat.id, "Я вас не понял")
    elif mes.text.lower() == "давай поговорим":
        list_person[mes.chat.id] = True
        bot.send_sticker(
            mes.chat.id, 'CAADAgADSgkAAnlc4glshq449fyDqBYE', reply_markup=keybord2)
    else:
        bot.send_message(mes.chat.id, mes.text)


bot.polling()
