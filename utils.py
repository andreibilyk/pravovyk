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
    callback = 'main'
    print(callback)
    markup = types.InlineKeyboardMarkup()
    # Склеиваем правильный ответ с неправильными
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
                                   "]+", flags=re.UNICODE)
    list_items = []
    for item in answers.split(','):
        list_items.append(item)
    # Хорошенько перемешаем все элементы
    #random.shuffle(list_items)
    # Заполняем разметку перемешанными элементами

    for item in list_items:
        but = types.InlineKeyboardButton(text = item,callback_data = callback + ","+emoji_pattern.sub(r'', item))
        print(callback + ","+emoji_pattern.sub(r'', item))
        markup.add(but)
        print('3')

    return markup
