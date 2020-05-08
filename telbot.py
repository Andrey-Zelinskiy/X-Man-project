
import photo
import telebot
from telebot import types
import apiai
import json
import sqlite3 as sql
import pyowm
import PROJECT as base_data
from geopy.geocoders import Nominatim
geolocatot = Nominatim()


bot = telebot.TeleBot('1005384316:AAE9RD5AeBFM_-Fg1V8AXKP1JFraODvjl6A')

owm = pyowm.OWM('ae3ad246e9f8a06c7eeaf52f89b841b6', language='ru')
photo.initRC()

start_keyboard = types.ReplyKeyboardMarkup(True, True)
weather_keyboard = types.ReplyKeyboardMarkup(True, True)

button_phone_number = types.KeyboardButton(
    text='Отправить номер телефона', request_contact=True)

button_location = types.KeyboardButton(
    text='Отправить местонахождения', request_location=True)
button_exit = types.KeyboardButton(text="/back")

weather_keyboard.row(button_location, button_exit)
start_keyboard.row(button_phone_number)

Keyboard = types.ReplyKeyboardMarkup(True, True)
button_talk = types.KeyboardButton(text='Давай поговорим')
button_weather = types.KeyboardButton(text='Узнать погоду')
button_person = types.KeyboardButton(text='Найти случайного собеседника')
button_search = types.KeyboardButton(text="/Find_user")
Keyboard.add(button_talk, button_weather)
Keyboard.add(button_person)
Keyboard.add(button_search)

keybord2 = types.ReplyKeyboardMarkup(True, True)
button_talk_2 = types.KeyboardButton(text='Закончить беседу')
keybord2.add(button_talk_2)


keybord_talk = types.ReplyKeyboardMarkup(True, True)
keybord_talk.add(button_exit)


@bot.message_handler(commands=["start"])
def start(mes):
    base_data.input_base(mes.chat.id, False, "photo", False,
                         0, name=mes.chat.first_name, username=mes.chat.username)
    bot.send_message(
        mes.chat.id, "Привет это чат бот в данный момент бот находиться в"
        " разработке, для полной работы отправьте мне вашу фотографию", reply_markup=start_keyboard)


@bot.message_handler(commands=['back'])
def back_weather(mes):
    base_data.set_search_flag(mes.chat.id, False)
    base_data.start_call(base_data.out_id_2(mes.chat.id), 1)
    base_data.start_call(mes.chat.id, 0)
    bot.send_message(mes.chat.id, "😉Вы в главном меню😉", reply_markup=Keyboard)


@bot.message_handler(content_types=["photo"])
def photo_take(mes):
    if base_data.out_search_flag(mes.chat.id) == "True":
        file_info = bot.get_file(mes.photo[len(mes.photo)-1].file_id)
        donwload_file = bot.download_file(file_info.file_path)
        path = "Papka\\" + " find_ " + str(mes.chat.id)+".png "
        new_file = open(path, "wb")
        new_file.write(donwload_file)
        new_id = photo.recognize(path)
        if new_id != 1:
            base_data.set_search_flag(mes.chat.id, False)
            answer = "Никнейм пользователя похожего на ваше фотографии: @" + \
                base_data.out_username(new_id) + "\n"
            answer += "Номер телефона: +" + \
                str(base_data.out_number_phone(new_id))
            bot.send_message(mes.chat.id, answer, reply_markup=Keyboard)
        else:
            bot.send_message(
                mes.chat.id, "Пользователь не найден", reply_markup=Keyboard)
    else:
        file_info = bot.get_file(mes.photo[len(mes.photo)-1].file_id)
        donwload_file = bot.download_file(file_info.file_path)
        name = "Papka\\" + str(mes.chat.id) + ".png"
        new_file = open(name, "wb")
        new_file.write(donwload_file)
        binar = sql.Binary(donwload_file)
        base_data.insert_photo(mes.chat.id, binar)
        bot.reply_to(mes, "Спасибо за фото")
        photo.takePhoto(mes.chat.id, "Papka\\"+str(mes.chat.id)+".png")


@bot.message_handler(commands=['Find_user'])
def find_people(mes):
    bot.send_message(
        mes.chat.id, "Отправте фотографии человека которого ищете!!", reply_markup=keybord_talk)
    base_data.set_search_flag(mes.chat.id, True)


@bot.message_handler(content_types=['contact'])
def phone_number(mes):
    if (mes.chat.id != mes.contact.user_id):
        bot.reply_to(mes, "Это не ваш номер телефона!")
        return
    base_data.set_phone_number(mes.contact.phone_number, mes.chat.id)
    bot.send_message(mes.chat.id, "Твой номер " +
                     mes.contact.phone_number, reply_markup=Keyboard)


@bot.message_handler(content_types=['location'])
def locat(mes):
    lat = mes.location.latitude
    lon = mes.location.longitude
    loc = geolocatot.reverse(f"{lat}, {lon}")
    # print(loc.raw)
    city = loc.raw['address']['city']
    observation = owm.weather_at_coords(lat, lon)
    w = observation.get_weather()
    temp = w.get_temperature('celsius')['temp']
    answer = f"В городе {city} сейчас {w.get_detailed_status()} \n"
    answer += f"Температура в районе {round(temp)} градусов\n\n"
    if temp < 10:
        answer += 'Очень холодно, оденься потеплее))'
    elif temp < 17:
        answer += 'Прохладно, лучше оденься:)'
    else:
        answer += 'Не холодно, хоть в трусах иди:)'
    bot.send_message(mes.chat.id, answer, reply_markup=Keyboard)


@bot.message_handler(regexp="Узнать погоду")
def wea(mes):
    bot.send_message(mes.chat.id, "Покажите где вы находитесь, для этого включите GPS и нажмите отправить местоположение",
                     reply_markup=weather_keyboard)


@bot.message_handler(regexp="найти случайного собеседника")
def call_person(mes):
    base_data.start_call(mes.chat.id, 1)
    bot.send_message(mes.chat.id, "Поиск собеседника. Просьба Ожидайте!")
    sear = base_data.out_search(1)
    for i in sear:
        print(i[5])
        if mes.chat.id != i[0]:
            base_data.start_call(mes.chat.id, i[0])
            base_data.start_call(i[0], mes.chat.id)
            bot.send_message(mes.chat.id, "Собеседник найден",
                             reply_markup=keybord_talk)
            bot.send_message(i[0], "Собеседник найден",
                             reply_markup=keybord_talk)
            break


@bot.message_handler(content_types=["text"])
def call(mes):

    te = base_data.out_id_2(mes.chat.id)
    if te != 0 and te != 1:
        bot.send_message(te, mes.text)
        return
    if base_data.out_photo_flag(mes.chat.id) == "True":
        if base_data.out_flag(mes.chat.id) == "True":
            if mes.text.lower() == "закончить беседу":
                base_data.flag_false(mes.chat.id)
                bot.send_message(
                    mes.chat.id, "Ну ладно,поговрим потом.", reply_markup=Keyboard)
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
        else:
            bot.send_message(mes.chat.id, "Я не знаю такой команды(")
    else:
        bot.send_message(
            mes.chat.id, "У вас нет доступа!!! Скиньте свою фотографию")


bot.polling()
