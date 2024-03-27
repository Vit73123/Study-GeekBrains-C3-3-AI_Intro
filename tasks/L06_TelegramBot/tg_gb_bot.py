import telebot
from random import *
import json
import requests
from deeppavlov import build_model

films=[]
API_URL='https://7012.deeppavlov.ai/model'

def save():
    with open(".temp/films.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(films,ensure_ascii=False))
    print("Наша фильмотека была успешно сохранена в файле films.json")

def load():
    global films
    with open(".temp/films.json", "r", encoding="utf-8") as fh:
        films=json.load(fh)
    print("Фильмотека была успешно загружена")   


API_TOKEN='5411681423:AAG8HUjRH--jrFHAV2UNb1_KueTmwv9_NA8'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        load()
        bot.send_message(message.chat.id,"Фильмотека была успешно загружена!")

    except:
        films.append("Матрица")
        films.append("Солярис")
        films.append("Властелин колец")
        films.append("Техасская резня бензопилой")
        films.append("Санта Барбара") 
        bot.send_message(message.chat.id,"Фильмотека была загружена по умолчанию!")


@bot.message_handler(commands=['all'])
def show_all(message):
    bot.send_message(message.chat.id,"Вот список фильмов")
    bot.send_message(message.chat.id, ", ".join(films))

@bot.message_handler(commands=['wiki'])
def wiki(message):
    quest = message.text.split()[1:]
    qq=" ".join(quest)
    data = { 'question_raw': [qq]}
    try:
        res = requests.post(API_URL,json=data,verify=False).json()
        bot.send_message(message.chat.id, res)
    except:
        bot.send_message(message.chat.id, "Что-то я ничего не нашел :-(")

bot.polling()