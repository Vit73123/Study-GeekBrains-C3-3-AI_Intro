import telebot
from random import *
import json
import requests

films = {}
API_URL = 'https://7012.deeppavlov.ai/model'

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)


# Загрузить информацию о фильмах из файла
def load_films():
    global films
    with open("films.json", "r", encoding="utf-8") as fh:
        films = json.load(fh)


# Запуск бота /start
@bot.message_handler(commands=['start'])
def start_message(message):
    load_films()
    bot.send_message(message.chat.id, "Фильмотека была загружена по умолчанию!")


# Обработчик команды /all
# Вывод наименований всех фильмов, которые есть в библиотеке
@bot.message_handler(commands=['all'])
def show_all(message):
    try:
        bot.send_message(message.chat.id, "Вот список фильмов")
        bot.send_message(message.chat.id, "\n".join(films.keys()))
    except:
        bot.send_message(message.chat.id, "Фильмотека пустая")


# ОБработчик команды /save
# Сохранить текущую информацию о фильмах в файл библиотеки
@bot.message_handler(commands=['save'])
def save_all(message):
    with open("films.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(films, indent=2, ensure_ascii=False))
    bot.send_message(message.chat.id, "Наша фильмотека была успешно сохранена в файле films.json")


# ОБработчик команды /wiki
# Запросить в Википедии информацию по тексту сообщения
@bot.message_handler(commands=['wiki'])
def wiki(message):
    quest = message.text.split()[1:]
    qq = " ".join(quest)
    data = {'question_raw': [qq]}
    try:
        res = requests.post(API_URL,json=data,verify=False).json()
        bot.send_message(message.chat.id, res)
    except:
        bot.send_message(message.chat.id, "Что-то я ничего не нашел :-(")


# Обработчик любого текстового сообщения, которое не относится к командам бота
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    # Приветствие бота
    if "дела" in message.text.lower():
        bot.send_message(message.chat.id, "Дела у меня хорошо, сам как?")

    # Вывод информации о фильме, если в тексте введено название фильма
    film_msg = str.capitalize(message.text)
    if film_msg in films.keys():
        film = films.get(film_msg)
        film_msg = "\n\n".join([
            film.get("country"),
            str(film.get("year")),
            film.get("description"),
        ])
        bot.send_message(message.chat.id, film_msg)


bot.polling()
