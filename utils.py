# -*- coding: utf-8 -*-
from SQLighter import SQLighter
from telebot import types
import random

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
    for item in list_items:
        but = types.InlineKeyboardButton(text = item,callback_data = callback + ","+item)
        print('2')
        markup.add(but)
        print('3')
    print(callback)
    return markup
