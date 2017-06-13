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
from smsclub import SMSer
import re
import sys
from User import User

bot = telebot.TeleBot(config.token)
user = User()
db_worker = SQLighter()

@bot.message_handler(commands=['start'])
def handle_commands(message):
 keyboard = types.InlineKeyboardMarkup()
 starting_button = types.InlineKeyboardButton(text="Розпочати😊", callback_data="start_but")
 keyboard.add(starting_button)
 bot.send_message(message.chat.id,"Привіт🎉 Мене звати Pravovyk🤓Я був створений, щоб давати людям відповіді на правові питання😊Ціль мого існування - зробити твоє життя простішим і допомогти тобі з питаннями, з якими ти стикаєшся щодня😎👌🏿. Щоб знайти відповідь вибери сферу права з меню і дотримуйся інструкцій. Якщо ти не знайшов відповідь ти завжди можеш підключити оператора ,  який дасть кваліфіковану відповідь на твоє питання🙋🏼. Крім цього, ти можеш стежити за проектом в соц.мережах, а також на сайті. Сподіваюся, що я стану твоїм кишеньковим помічником, який виручить у потрібну хвилину😌✊🏻. Щоб розпочати спілкуватись зі мною натисни кнопку👇🏻",reply_markup = keyboard)



@bot.message_handler(func=lambda message: True, content_types=['text'])
def main_messages(message):
 if user.verified == True:
  if not hasattr(main_messages, '_steps'):  # инициализация значения
   main_messages._steps = []
  text = message.text.encode('utf-8')
  if text == "Обрати сферу📋":
   row = db_worker.select_single(1)
     # Формируем разметку
   markup = utils.generate_markup(row[2])
   markup.add("Ми в соц.мережах🤓🤳")
   markup.add("Поділитися з друзями👥")
   main_messages._steps = []
   bot.send_message(message.chat.id,"Обери сферу",reply_markup=markup)
   return
  elif text == "Назад🔙":
   if len(main_messages._steps) >= 2:
    text = main_messages._steps[len(main_messages._steps)-2]
    main_messages._steps.remove(main_messages._steps[len(main_messages._steps)-1])
    main_messages._steps.remove(main_messages._steps[len(main_messages._steps)-2])
   elif len(main_messages._steps) < 2:
    row = db_worker.select_single(1)
      # Формируем разметку
    markup = utils.generate_markup(row[2])
    main_messages._steps = []
    bot.send_message(message.chat.id,"Обери сферу",reply_markup=markup)
    return
  elif text == "Ми в соц.мережах🤓🤳":
   keyboard = types.InlineKeyboardMarkup()
   instagram_button = types.InlineKeyboardButton(text="Ми в Instagram", url="https://instagram.com/pravovyk")
   facebook_button = types.InlineKeyboardButton(text="Ми у Facebook", url="http://fb.me/pravovyk")
   keyboard.add(instagram_button)
   keyboard.add(facebook_button)
   bot.send_message(message.chat.id,"Слідкуйте за нами у соц.мережах, дізнавайтесь кожного дня новини у світі права📚 Слідкуйте за сім'єю Правовиків👨‍👩‍👧‍👦 та ситуації, у котрі потрапляють члени сім'ї, і з якими зіштовхується кожен з нас!😎'",reply_markup = keyboard)
   return
  elif text == "Поділитися з друзями👥":
   keyboard = types.InlineKeyboardMarkup()
   switch_button = types.InlineKeyboardButton(text="Обрати друга", switch_inline_query="Кишеньковий бот-правовик🤓Натисни на моє ім'я, щоб розпочати бесіду зі мною☺️")
   keyboard.add(switch_button)
   bot.send_message(message.chat.id,"Натисни кнопку та обери друзів, щоб поділитися з ними",reply_markup = keyboard)
   return
  try:
   row = db_worker.select_row(text)
   if row[2]:
    markup = utils.generate_markup(row[2])
    markup.add("Обрати сферу📋","Назад🔙")
    main_messages._steps.append(text)
    bot.send_message(message.chat.id,row[1],reply_markup=markup)
   else:
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Підключити оператора", url="https://t.me/andrei_bilyk")
    keyboard.add(url_button)
    bot.send_message(message.chat.id,row[1]+'''
   <b>Не знайшли відповідь?</b>''',parse_mode='HTML',reply_markup = keyboard)
    bot.send_sticker(message.chat.id,"CAADAgADwAEAAi9e9g_X8nwrz1fTFwI")
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
   bot.send_message(message.chat.id,"Вибачте,інформації ще нема,ми працюємо над цим!")

@bot.message_handler(content_types=["sticker"])
def file_sent(message):
 bot.send_message(message.chat.id, message.sticker.file_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "start_but":
          # поиск в базе
          user.verified = False
          msg = bot.send_message(call.message.chat.id,"Ви ще не верифіковані у сервісі pravovyk.com. Будь ласка, введіть Ваш мобільний номер телефону, на нього буде відправлений код верифікації.Кишеньковий помічник Pravovyk є безкоштовним продуктом сервісу pravovyk.com.")
          bot.register_next_step_handler(msg, sms_verification)
          return
        elif call.data == "code_one_more":
            try:
             number = str(randint(100000,999999))
             t = SMSer()
             t.send_text(message.text,"Ваш код для верифікації: "+number)
             msg = bot.send_message(message.chat.id,"Ваш код для верифікації надісланий на номер:"+message.text.encode('utf-8'))
             bot.register_next_step_handler(msg, code_verif)
            except BaseException as e:
             bot.send_message(message.chat.id,"Вибачте, виникли технічні несправності, вибачте за незруучності!"+str(e))

def sms_verification(message):
 number = str(randint(100000,999999))
 try:
  validate_mobile(message.text)
 except BaseException as e:
  msg = bot.send_message(message.chat.id,"Номер телефону введений некоректно. Спробуйте ще раз")
  bot.register_next_step_handler(msg, sms_verification)
  return
 try:
  t = SMSer()
  print("1")
  t.send_text(message.text.encode('utf-8'),("Ваш код для верифікації: "+number).encode('utf-8'))
  print("sent")
  msg = bot.send_message(message.chat.id,"Ваш код для верифікації надісланий на номер:"+message.text.encode('utf-8'))
  bot.register_next_step_handler(msg, code_verif)
  user.setCode(number)
  user.setPhone(message.text)
 except BaseException as e:
  bot.send_message(message.chat.id,"Вибачте, виникли технічні несправності, вибачте за незруучності!"+str(e))

def validate_mobile(value):

    rule = re.compile(r'^(?:\+?38)?[0]\d{9,11}$')

    if not rule.search(value):
        raise BaseException

def code_verif(message):
 if message.text.encode('utf-8') == user.code:
  row = db_worker.select_single(1)
       # Формируем разметку
  markup = utils.generate_markup(row[2])
  markup.add("Ми в соц.мережах🤓🤳")
  markup.add("Поділитися з друзями👥")
  user.verified = True
  msg = bot.send_message(message.chat.id,"Верифікація пройшла успішно😊Давай почнемо нашу бесіду?😃 Обери сферу:",reply_markup = markup)
  bot.register_next_step_handler(msg,main_messages)
 else:
  keyboard = types.InlineKeyboardMarkup()
  starting_button = types.InlineKeyboardButton(text="Надіслати код ще раз", callback_data="code_one_more")
  keyboard.add(starting_button)
  bot.send_message(message.chat.id,"Код верифікації - невірний🙈",reply_markup = keyboard)

server = Flask(__name__)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 8443))
