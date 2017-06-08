# -*- coding: utf-8 -*-
import config
import os
from flask import Flask, request
import telebot
import logging
from telebot import types
from SQLighter import SQLighter
import utils




bot = telebot.TeleBot(config.token)

db_worker = SQLighter()

@bot.message_handler(commands=['start'])
def handle_commands(message):

 row = db_worker.select_single(1)
    # Формируем разметку
 markup = utils.generate_markup(row[2])
 repeat_all_messages._steps = []
 bot.send_message(message.chat.id,"Обери сферу",reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def repeat_all_messages(message):
 if not hasattr(repeat_all_messages, '_steps'):  # инициализация значения
  repeat_all_messages._steps = []
 text = message.text.encode('utf-8')
 bot.send_message(message.chat.id,''' <a href="tel:+380731681919"> Звоните нам бесплатно! </ a>''',parse_mode='HTML')
 bot.send_message(message.chat.id,'''<a href="www.pravovyk.com">https://pbs.twimg.com/profile_images/700243915325251584/6SSBl9ye.jpg</ a>''',parse_mode='HTML')
 if text == "Обрати сферу📋":
  row = db_worker.select_single(1)
     # Формируем разметку
  markup = utils.generate_markup(row[2])
  repeat_all_messages._steps = []
  bot.send_message(message.chat.id,"Обери сферу",reply_markup=markup)
  return
 elif text == "Назад🔙":
  if len(repeat_all_messages._steps) >= 2:
   text = repeat_all_messages._steps[len(repeat_all_messages._steps)-2]
   repeat_all_messages._steps.remove(repeat_all_messages._steps[len(repeat_all_messages._steps)-1])
   repeat_all_messages._steps.remove(repeat_all_messages._steps[len(repeat_all_messages._steps)-2])
  elif len(repeat_all_messages._steps) < 2:
   row = db_worker.select_single(1)
      # Формируем разметку
   markup = utils.generate_markup(row[2])
   repeat_all_messages._steps = []
   bot.send_message(message.chat.id,"Обери сферу",reply_markup=markup)
   return
 try:
  row = db_worker.select_row(text)
  if row[2]:
   markup = utils.generate_markup(row[2])
   markup.add("Обрати сферу📋","Назад🔙")
   repeat_all_messages._steps.append(text)
   bot.send_message(message.chat.id,row[1],reply_markup=markup)
  else:
   bot.send_message(message.chat.id,row[1],parse_mode='HTML')
  try:
   file_id = db_worker.select_file(text)
   bot.send_document(message.chat.id,file_id)
  except Exception:
   pass
 except BaseException as e:
  bot.send_message(message.chat.id,"Вибачте,інформації ще нема,ми працюємо над цим")

@bot.message_handler(content_types=["document"])
def audio_sent(message):
 bot.send_message(message.chat.id, message.document.file_id)

server = Flask(__name__)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 8443))
