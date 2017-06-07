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
 bot.send_message(""" <p style="text-align: center;">Згідно зі ст.&nbsp;4 Закону України &laquo;Про права споживача&raquo;</p>
<p style="text-align: center;">Споживач має наступні <em><strong>права</strong></em>:</p>
<ul style="list-style-type: disc;">
<li><strong>захист своїх прав державою</strong> (здійснюють управління захисту прав споживачів, органи Держспоживстандарту, судові органи);</li>
<li><strong>належну якість</strong> продукції та обслуговування;</li>
<li><strong>безпеку</strong> продукції;</li>
<li>необхідну, доступну, достовірну та вчасну <strong>інформацію</strong> про продукцію, її кількість, якість, асортимент, а також про її виробника (виконавця, продавця);</li>
<li>відшкодування <strong>майнової та моральної шкоди</strong>, завданої через недоліки продукції (дефекту), відповідно до закону;</li>
<li>звернутися до суду та інших уповноважених державних органів по <strong>захист порушених прав</strong>;</li>
<li>об'єднатися в <strong>громадські організації</strong> споживачів (об'єднання споживачів).</li>
</ul> """,parse_mode='HTML')
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
   bot.send_message(message.chat.id,+row[1].encode('utf-8'))
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
