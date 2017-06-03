# -*- coding: utf-8 -*-
import config
import os
from flask import Flask, request
import telebot
import logging
from telebot import types
from SQLighter import SQLighter
import utils
import sqlite3




bot = telebot.TeleBot(config.token)



@bot.message_handler(commands=['start'])
def handle_commands(message):
 db_worker = SQLighter(config.database_name)
 row = db_worker.select_single(1)
    # Формируем разметку
 markup = utils.generate_markup(row[1])
 repeat_all_messages._steps = []
 bot.send_message(message.chat.id,"Обери сферу",reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def repeat_all_messages(message):
 if not hasattr(repeat_all_messages, '_steps'):  # инициализация значения
  repeat_all_messages._steps = []
 if message.text == "Обрати сферу":
  repeat_all_messages._steps.clear()
  handle_commands(message)
  return
 elif message.text == "Назад":
  if len(repeat_all_messages._steps) >= 2:
   message.text = repeat_all_messages._steps[len(repeat_all_messages._steps)-2]
   repeat_all_messages._steps.remove(repeat_all_messages._steps[len(repeat_all_messages._steps)-1])
   repeat_all_messages._steps.remove(repeat_all_messages._steps[len(repeat_all_messages._steps)-2])
  elif len(repeat_all_messages._steps) < 2:
   repeat_all_messages._steps.clear()
   handle_commands(message)
   return
 db_worker = SQLighter(config.database_name)
 try:
  row = db_worker.select_row(message.text)
  markup = utils.generate_markup(row[1])
  markup.add("Обрати сферу","Назад")
  repeat_all_messages._steps.append(message.text)
  bot.send_message(message.chat.id,row[0],reply_markup=markup)
 except BaseException:
  bot.send_message(message.chat.id,"Вибачте,інформації ще нема,ми працюємо над цим")

server = Flask(__name__)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 8443))
