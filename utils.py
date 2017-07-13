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
    print(callback)
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
         print(callback + item[:-(24-len(callback))])
         but = types.InlineKeyboardButton(text = item,callback_data = callback + str(i))
        else:
         print("errorr rorrrrr")
         but = types.InlineKeyboardButton(text = item,callback_data = callback + item[:-(24-len(callback))])
        print(callback + str(i))
        markup.add(but)
    if len(callback)>1:
     but = types.InlineKeyboardButton(text = "Назад🔙",callback_data = callback[:-1])
     markup.add(but)
    return markup
