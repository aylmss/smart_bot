import random

# text=input()
# if text in ["Привет", "Здарова", "Хеллоу"]:
#     print(random.choice(["Здрасте", "Йоу", "Приветики"]))
# elif text in ["Пока", "Увидимся", "Чао"]:
#     print(random.choice(["Буду ждать нашей встречи", "Ок", "Бай-бай"]))
# else:
#     print("Не понял")

import re
import nltk  # pip install --user -U nltk

# Функция очищения текста
def filter(text):
    text=text.lower()
    expression=r'[^\w\s]'  # Регулярное выражение= "Все что не слово и не пробел"
    return re.sub(expression, "", text)  # Substitute на ""

# Сравнить текст пользователя с примером
def text_match(user_text, example):
    user_text=filter(user_text)
    example=filter(example)

    if len(user_text)==0 or len(example)==0:
        return False

    # if user_text.find(example) != -1:
    #     return True

    # if example.find(user_text) != -1:
    #     return True

    example_length=len(example)
    difference=nltk.edit_distance(user_text, example) / example_length

    # return user_text==example
    # return difference<0.4
    return difference<0.2

# text_match("Привет", "Прив")
# print(text_match("Привет как дела", "Привет"))

# # length=6
# # print(nltk.edit_distance("Привет", "Привед")/length)

INTENTS={
    "hello": {
        "examples": ["Привет", "Хеллоу", "Хай"],
        "response": ["Здрасте", "Йоу", "Приветики"],
    },
        "how-are-you": {
        "examples": ["Как дела", "Чем занят", "Чо по чем"],
        "response": ["Вроде ничего", "На чиле, на расслабоне"],
    },
}

# чем занята -> how are you
def get_intent(text):
    for intent_name in INTENTS.keys():
        examples=INTENTS[intent_name]["examples"]
        for example in examples:
            if text_match(text, example):
                return intent_name


# hello -> йоу
def get_response(intent):
    return random.choice(INTENTS[intent]["response"])

# print(get_response("hello"))

# def bot(text):
#     intent=get_intent(text)
#     if not intent:
#         print("Ничего не понятно")
#     else:
#         print(get_response(intent))

# bot("Чем занят")

# text=""
# while text!="Выход":
#     text=input()
#     bot(text)

import json

config_file=open("big_bot_config.json", "r")
BIG_INTENTS=json.load(config_file)

# print(BIG_INTENTS['intents'].keys())

# Задача: Научить модель определять интент по тексту пользователя
# Классификация текстов
# Строчку на вход -> Модель предсказывает класс текста
# Фраза на вхож -> Модель предсказывает интент фразы
# Входные данные (Фразы, Х)
# Выходные данные (Интенты, У)
# Модель обучится на наших примерах и сможет предсказывать интенты по фразе

INTENTS = BIG_INTENTS["intents"]

X=[]
y=[]
for name, intent in INTENTS.items():
    for phrase in intent['examples']:
        X.append(phrase)
        y.append(name)

    for phrase in intent['responses']:
        X.append(phrase)
        y.append(name)

# print(X[:10])
# print(y[1000:1010])
# print(len(X))

# Векторизация текстов 
# Превратить текст в набор чисел (вектор) 
# https://scikit-learn.org/stable/modules/classes.html

# pip install -U scikit-learn
from sklearn.feature_extraction.text import CountVectorizer

# Пример
# 1. Набор текстов={
#     "мама мыла раму",
#     "мыла раму мама", 
#     "раму мама мыла",
# }
# 2. Обучение
# мама=1, мыла=2, раму=3
#   "мама мыла раму" = [1,2,3]
#     "мыла раму мама" = [2,3,1]
#     "раму мама мыла" = [3,1,2]
# 3. Векторизация
# "мама мама мама" = [1,1,1]
# "как мама мыла раму"=[0,1,2,3]

vectorizer=CountVectorizer()
vectorizer.fit(X)     # Обучаем векторайзер

# for i in vectorizer.transform(["как дела чем занят"]).toarray()[0]:
#     if i!=0:
#         print(i, end=',')
# dense=[0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,00,6,0,0,1]
# sparse=[....2,...6,...1]

# from sklearn.neural_network import MLPClassifier   # Импортируем
# mlp_model=MLPClassifier()          # Создаем модель
vecX=vectorizer.transform(X)      # Преобразуем тексты в вектора
# mlp_model.fit(vecX, y)                   # Обучаем модель

# print(mlp_model.score(vecX, y))  # Качество на тренировочной выборке = accurace / больше = лучше

from sklearn.ensemble import RandomForestClassifier
rf_model=RandomForestClassifier()
rf_model.fit(vecX, y)
rf_model.score(vecX, y)

MODEL=rf_model   #mlp_model

def get_intent_ml(text):
    vec_text=vectorizer.transform([text])
    intent=MODEL.predict(vec_text)[0]
    return intent

# print(get_intent_ml("расскажи шутку или анекдот"))
# print(get_intent_ml("шутку или анекдот пожалуйста давай быстро"))
# print(get_intent_ml("какие знаешь города"))
# print(get_intent_ml("чо по приколам брат сделай красиво"))

failure_phrases= BIG_INTENTS['failure_phrases']

INTENTS=BIG_INTENTS['intents']
def get_intent(text):
    for intent_name in INTENTS.keys():
        examples=INTENTS[intent_name]["examples"]
        for example in examples:
            if text_match(text, example):
                return intent_name

# hello -> йоу
def get_response(intent):
    return random.choice(INTENTS[intent]["responses"])

def bot(text):
    text=filter(text)
    intent=get_intent(text)
    # print("get_intent", intent, end='')
    if not intent:
        intent=get_intent_ml(text)
        # print("get_intent_ml", intent, end='')
    if intent:
        return get_response(intent)
    else:
        return random.choice(failure_phrases)

# bot("Привет братишка как дела погода норм")

# text=""
# while text!="Выход":
#     text=input()
#     bot(text)

# pip install python-telegram-bot --pre

# pip install nest_asyncio
import nest_asyncio
nest_asyncio.apply()

from telegram import Update 
from telegram.ext import ApplicationBuilder #  Инструмент чтобы создавать и настраивать приложение (телеграм бот)
from telegram.ext import MessageHandler #  Handler - обработчик - создать реакцию (функцию) на действие

from  telegram.ext import filters

from config import TOKEN

# t.me/july_smart_bot

async def reply(update: Update, context) -> None:
  # ToDo: убрать заглушку, подключить бота
  question = update.message.text
  reply = bot(question)
  print(f"> {question}")
  print(f"< {reply}")
  await update.message.reply_text(reply) #  Ответ пользователю

app = ApplicationBuilder().token(TOKEN).build()

# Создаем обработчик текстовых сообщений
handler = MessageHandler(filters.Text(), reply)

# Добавляем обработчик в приложение
app.add_handler(handler)

app.run_polling()
