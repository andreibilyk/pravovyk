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
network = {"1": "Сімейне право👨‍👩‍👧‍👦",
"11": 'Аліменти💰',
"111": 'Розмір аліментів🤓📊',
"112":'Заборгованість по аліментам😡⏳',
"113": 'Звільнення від сплати🤔',
"12":'Права батьків після розлучення👨‍👦👩‍👦',
"13":'Розлучення💔🙇🏼',
"14": 'Поділ майна🔪',
"15": 'Усиновлення👼🏼',
"16": 'Заповіт📜',
"17": 'Спадок🔗',
"2": 'Трудове право💳',
"21": 'Трудовий договір📄',
"22": 'Звільнення😔',
"23": 'Відпустка🏖',
"24": 'Відрядження🚊✈️',
"25": 'Праця неповнолітніх👶🏼',
"26": 'Лікарняний🏥👩🏼‍⚕️',
"264": 'Виплати💰',
"27": 'Випробування🔮',
"3": 'Право споживача🍞💇🏼‍♂️',
'31':'Права споживача📊💇🏼‍♂️',
'32':'Гарантія⚙️',
'33':'Виявлення недоліків🔬',
'34':'Заміна товару💰🛍',
'35':'Інтернет-магазин🖥',
'4':'Поліція👮🏼🚨',
'41':'Права поліцейських👮🏻‍♀️',
'42':'Пред’явлення посвідчення🙌🏻',
'43':'Стан сп’яніння🍸🚙',
'44':'Складання протоколу🖌👮🏼',
'45':'Штраф💰',
'46':'ДТП🚗',
}
spheres = {
"Сімейне право👨‍👩‍👧‍👦":"1",
'Трудове право💳':"2",
'Право споживача🍞💇🏼‍♂️':'3',
'Поліція👮🏼🚨':'4',
}

@bot.message_handler(commands=['start'])
def handle_commands(message):
 keyboard = types.ReplyKeyboardMarkup()
 starting_button = types.KeyboardButton(text="Поділитись номером телефону😊📲",request_contact=True)
 keyboard.add(starting_button)
 bot.send_message(message.chat.id,"Привіт🎉 Мене звати Pravovyk🤓Я був створений, щоб давати людям відповіді на правові питання😊Ціль мого існування - зробити твоє життя простішим і допомогти тобі з питаннями, з якими ти стикаєшся щодня😎👌🏿. Щоб знайти відповідь вибери сферу права з меню і дотримуйся інструкцій. Якщо ти не знайшов відповідь ти завжди можеш підключити оператора ,  який дасть кваліфіковану відповідь на твоє питання🙋🏼. Крім цього, ти можеш стежити за проектом в соц.мережах, а також на сайті. Сподіваюся, що я стану твоїм кишеньковим помічником, який виручить у потрібну хвилину😌✊🏻. Щоб розпочати спілкуватись зі мною,будь ласка, поділися зі мною своїм номером мобільного телефона, що буде використовуватись для авторизації☺️",reply_markup = keyboard)

@bot.message_handler(commands=['new'])
def new_command(message):
 row = db_worker.select_single(1)
      # Формируем разметку
 markup = utils.generate_markup_keyboard(row[2])
 msg = bot.send_message(message.chat.id,"Обери сферу:",reply_markup = markup)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def main_messages(message):
  text = message.text
  print(message)
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
   conn.close()
   keyboard = types.InlineKeyboardMarkup()
   switch_button = types.InlineKeyboardButton(text="Обрати друга", switch_inline_query="Кишеньковий бот-правовик🤓Натисни на моє ім'я, щоб розпочати бесіду зі мною☺️")
   keyboard.add(switch_button)
   bot.send_message(message.chat.id,"Натисни кнопку та обери друзів, щоб поділитися з ними",reply_markup = keyboard)
   return
  try:
   row = db_worker.select_row("'"+text+"'")
   if row[2]:
    markup = utils.generate_markup(row[2],spheres[text])
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
            u"\U0001F914"
            u"\u2716"
                               "]+", flags=re.UNICODE)
    gog_text = emoji_pattern.sub(r'', text)
    conn.request("POST", "/collect", "v=1&tid=UA-100965704-2&cid=%s&t=pageview&dp=/%s"%(str(message.chat.id),translit(gog_text, 'uk',reversed=True)))
    conn.close()
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
 markup = utils.generate_markup_keyboard(row[2])
 msg = bot.send_message(message.chat.id,"Верифікація пройшла успішно😊Давай почнемо нашу бесіду!😃 Обери сферу:",reply_markup = markup)

@bot.callback_query_handler(func=lambda call: True) #-----InlineKeyboardButton
def callback_inline(call):
    if call.message:

     #print(list_items[-1])
     if call.data in network:
      print(network.get(call.data))
      row = db_worker.select_row("'"+network.get(call.data)+"'")
     else:
      print(call.data)
      row = db_worker.select_row2("'%"+call.data+"%'")
     if row[2]:
      markup = utils.generate_markup(row[2],call.data)
      bot.send_message(call.message.chat.id,row[1], reply_markup = markup)
     else:
      keyboard = types.InlineKeyboardMarkup()
      url_button = types.InlineKeyboardButton(text="Підключити оператора", url="https://t.me/test139899_bot")
      keyboard.add(url_button)
      bot.send_message(call.message.chat.id,row[1]+'''
      <b>Не знайшли відповідь?</b>''',parse_mode='HTML',reply_markup = keyboard)
      bot.send_sticker(call.message.chat.id,"CAADAgADwgEAAi9e9g9yzglfrxXMpQI")
      keyboard = types.InlineKeyboardMarkup()
      url_button = types.InlineKeyboardButton(text="Перейти на веб-сайт", url="http://pravovyk.com")
      keyboard.add(url_button)
      bot.send_message(call.message.chat.id,"Дізнайтесь більше про нас😎",reply_markup = keyboard)
      if row[7]:
       bot.send_document(call.message.chat.id,row[7])



#

server = Flask(__name__)

@server.route('/', methods=['GET'])
def verify():
 return "Hello world!"

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 8443),threaded=True)
