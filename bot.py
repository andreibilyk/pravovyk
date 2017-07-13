# -*- coding: utf-8 -*-
import config
import os
from flask import Flask, request
import telebot
import logging
from telebot import types
from SQLighter import SQLighter
import utils
from random import randint
import re
import sys
import uuid
import http.client
import urllib
from transliterate import translit, get_available_language_codes

bot = telebot.TeleBot(config.token)
db_worker = SQLighter()

@bot.message_handler(commands=['start'])
def handle_commands(message):
 print(str(message.chat.id))
 keyboard = types.InlineKeyboardMarkup()
 starting_button = types.InlineKeyboardButton(text="Поділитись номером телефону😊", callback_data="start_but",request_contact=True)
 keyboard.add(starting_button)
 bot.send_message(message.chat.id,"Привіт🎉 Мене звати Pravovyk🤓Я був створений, щоб давати людям відповіді на правові питання😊Ціль мого існування - зробити твоє життя простішим і допомогти тобі з питаннями, з якими ти стикаєшся щодня😎👌🏿. Щоб знайти відповідь вибери сферу права з меню і дотримуйся інструкцій. Якщо ти не знайшов відповідь ти завжди можеш підключити оператора ,  який дасть кваліфіковану відповідь на твоє питання🙋🏼. Крім цього, ти можеш стежити за проектом в соц.мережах, а також на сайті. Сподіваюся, що я стану твоїм кишеньковим помічником, який виручить у потрібну хвилину😌✊🏻. Щоб розпочати спілкуватись зі мною,будь ласка, поділися зі мною своїм номером мобільного телефона, що буде використовуватись для авторизації☺️",reply_markup = keyboard)



@bot.message_handler(func=lambda message: True, content_types=['text'])
def main_messages(message):
  text = message.text

  if text == "Обрати сферу📋":
   row = db_worker.select_single(1)
     # Формируем разметку
   markup = utils.generate_markup(row[2])
   bot.send_message(message.chat.id,"Обери сферу",reply_markup=markup)
   return
  elif text == "Ми в соц.мережах🤓🤳":
   conn = http.client.HTTPConnection("www.google-analytics.com")
   conn.request("POST", "/collect", "v=1&tid=UA-100965704-2&cid=%s&t=pageview&dp=/socials"%str(message.chat.id))
   conn.close()
   keyboard = types.InlineKeyboardMarkup()
   instagram_button = types.InlineKeyboardButton(text="Ми в Instagram", url="https://instagram.com/pravovyk")
   facebook_button = types.InlineKeyboardButton(text="Ми у Facebook", url="http://fb.me/pravovyk")
   keyboard.add(instagram_button)
   keyboard.add(facebook_button)
   bot.send_message(message.chat.id,"Слідкуйте за нами у соц.мережах, дізнавайтесь кожного дня новини у світі права📚 Слідкуйте за сім'єю Правовиків👨‍👩‍👧‍👦 та ситуації, у котрі потрапляють члени сім'ї, і з якими зіштовхується кожен з нас!😎'",reply_markup = keyboard)
   return
  elif text == "Поділитися з друзями👥":
   conn = http.client.HTTPConnection("www.google-analytics.com")
   conn.request("POST", "/collect", "v=1&tid=UA-100965704-2&cid=%s&t=pageview&dp=/share"%str(message.chat.id))
   response = conn.getresponse()
   print(str(response.status))
   print(str(response.reason))
   conn.close()
   keyboard = types.InlineKeyboardMarkup()
   switch_button = types.InlineKeyboardButton(text="Обрати друга", switch_inline_query="Кишеньковий бот-правовик🤓Натисни на моє ім'я, щоб розпочати бесіду зі мною☺️")
   keyboard.add(switch_button)
   bot.send_message(message.chat.id,"Натисни кнопку та обери друзів, щоб поділитися з ними",reply_markup = keyboard)
   return
  try:
   row = db_worker.select_row("'"+text+"'")
   if row[2]:
    print('1')
    markup = utils.generate_markup(row[2])
    conn = http.client.HTTPConnection("www.google-analytics.com")
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\u200d"
            u"\u23f3"#⏳
            u"\u2642"#♂
            u"\ufe0f"
            u"\u2699"#⚙️
            u"\U0001f913"
            u"\u2640"#♀
            u"\u2019"
            u"\u2708"#✈️
            u"\u2695"#⚕
                               "]+", flags=re.UNICODE)
    gog_text = emoji_pattern.sub(r'', text)
    print(gog_text)
    conn.request("POST", "/collect", "v=1&tid=UA-100965704-2&cid=%s&t=pageview&dp=/%s"%(str(message.chat.id),translit(gog_text, 'uk',reversed=True)))
    conn.close()
    print("3")
    print(markup)
    bot.send_message(message.chat.id,row[1],reply_markup=markup)
   else:
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Підключити оператора", url="https://t.me/andrei_bilyk")
    keyboard.add(url_button)
    bot.send_message(message.chat.id,row[1]+'''
   <b>Не знайшли відповідь?</b>''',parse_mode='HTML',reply_markup = keyboard)
    bot.send_sticker(message.chat.id,"CAADAgADwgEAAi9e9g9yzglfrxXMpQI")
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на веб-сайт", url="http://pravovyk.com")
    keyboard.add(url_button)
    bot.send_message(message.chat.id,"Дізнайтесь більше про нас😎",reply_markup = keyboard)
   try:
    file_id = db_worker.select_file(text)
    bot.send_document(message.chat.id,file_id)
   except Exception:
    pass
  except BaseException as e:
   bot.send_message(message.chat.id,"Вибачте,інформації ще нема,ми працюємо над цим!"+str(e))

@bot.message_handler(content_types=["sticker"])
def sticker_sent(message):
 bot.send_message(message.chat.id, message.sticker.file_id)

@bot.message_handler(content_types=["document"])
def pdf_sent(message):
 print(message)
@bot.message_handler(content_types=["contact"])
def contact_sent(message):
 db_worker.user_create(message.contact.phone_number[-10:],message.from_user.first_name,message.from_user.last_name,str(message.chat.id))
 row = db_worker.select_single(1)
      # Формируем разметку
 markup = utils.generate_markup(row[2])
 msg = bot.send_message(message.chat.id,"Верифікація пройшла успішно😊Давай почнемо нашу бесіду!😃 Обери сферу:",reply_markup = markup)

@bot.callback_query_handler(func=lambda call: True) #-----InlineKeyboardButton
def callback_inline(call):
    if call.message:
     row = db_worker.select_row("'"+call.data[-1]+"'")
     if row[2]:
      markup = utils.generate_markup(row[2],call.data)
      bot.send_message(call.message.chat.id,row[1],reply_markup=markup)





server = Flask(__name__)



@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 8443),threaded=True)
