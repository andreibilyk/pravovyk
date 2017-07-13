# -*- coding: utf-8 -*-
from SQLighter import SQLighter
from telebot import types
import random
import re

def generate_markup_keyboard(answers):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    print("start_keyboard")
    markup = types.ReplyKeyboardMarkup()
    # Склеиваем правильный ответ с неправильными
    list_items = []
    for item in answers.split(','):
        list_items.append(item)
    # Хорошенько перемешаем все элементы
    #random.shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    for item in list_items:
        markup.add(item)

    return markup

def generate_markup(answers,callback):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
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
    markup = types.InlineKeyboardMarkup()
    # Склеиваем правильный ответ с неправильными
    list_items = []
    for item in answers.split(','):
        list_items.append(item)
    # Хорошенько перемешаем все элементы
    #random.shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    i = 0
    for item in list_items:
        i += 1
        if (len(callback + str(i)) <= 2) or (callback + str(i) == '111') or (callback + str(i) == '112') or (callback + str(i) == '113') or (callback + str(i) == '264'):
         but = types.InlineKeyboardButton(text = item,callback_data = callback + str(i))
        else:
         if(len(item)<24):
          print(emoji_pattern.sub(r'', item))
          but = types.InlineKeyboardButton(text = item,callback_data = emoji_pattern.sub(r'', item))
         else:
          print(emoji_pattern.sub(r'', item))
          but =  types.InlineKeyboardButton(text = item,callback_data = emoji_pattern.sub(r'', item[:-24]))
        markup.add(but)
    if len(callback)>1:
     but = types.InlineKeyboardButton(text = "Назад🔙",callback_data = callback[:-1])
     markup.add(but)
    return markup
