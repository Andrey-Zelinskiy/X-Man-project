
import telebot
from telebot import types
import apiai
import json
import sqlite3 as sql
import pyowm
import PROJECT as base_data

bot = telebot.TeleBot('1005384316:AAE9RD5AeBFM_-Fg1V8AXKP1JFraODvjl6A')

owm = pyowm.OWM('ae3ad246e9f8a06c7eeaf52f89b841b6', language='ru')


rows = base_data.out_data()
for row in rows:
    name = str(row[0]) + ".png"
    if row[2] == "False":
        continue
    new_file = open(name, "wb")
    data = row[1]
    new_file.write(data)


mark = types.ReplyKeyboardMarkup(True, True)
mark.row_width
mark.row('Давай поговорим')
mark.row('Какая погода?')


keybord2 = types.ReplyKeyboardMarkup(True, True)
keybord2.row('Закончить беседу')


@bot.message_handler(commands=["start"])
def start(mes):
    base_data.input_base(mes.chat.id, False, "photo", False)
    bot.send_message(
        mes.chat.id, "Привет это чат бот в данный момент бот находиться в разработке, для полной работы отправьте мне вашу фотографию", reply_markup=mark)


@bot.message_handler(content_types=["photo"])
def photo(mes):
    file_info = bot.get_file(mes.photo[len(mes.photo)-1].file_id)
    donwload_file = bot.download_file(file_info.file_path)
    binar = sql.Binary(donwload_file)
    base_data.insert_photo(mes.chat.id, binar)
    bot.reply_to(mes, "Спасибо за фото")


@bot.message_handler(content_types=["text"])
def call(mes):
    if base_data.out_photo_flag(mes.chat.id) == "True":
        if base_data.out_flag(mes.chat.id) == "True":
            if mes.text.lower() == "закончить беседу":
                base_data.flag_false(mes.chat.id)
                bot.send_message(
                    mes.chat.id, "Ну ладно,поговрим потом.", reply_markup=mark)
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
            base_data.flag_true(mes.chat.id)
            bot.send_sticker(
                mes.chat.id, 'CAADAgADSgkAAnlc4glshq449fyDqBYE', reply_markup=keybord2)
        elif mes.text.lower() == "какая погода?":
            bot.send_message(mes.chat.id, "Узнаю погоду.")
            observation = owm.weather_at_place('Минск')
            w = observation.get_weather()
            temp = w.get_temperature('celsius')['temp']
            answer = f"В городе сейчас {w.get_detailed_status()} \n"
            answer += f"Температура в районе {round(temp)} градусов\n\n"
            if temp < 10:
                answer += 'Очень холодно, оденься потеплее))'
            elif temp < 17:
                answer += 'Прохладно, лучше оденься:)'
            else:
                answer += 'Не холодно, хоть в трусах иди:)'
            bot.send_message(mes.chat.id, answer)
        else:
            bot.send_message(mes.chat.id, "Я не знаю такой команды(")
    else:
        bot.send_message(
            mes.chat.id, "У вас нет доступа!!! Скиньте свою фотографию")


bot.polling()
