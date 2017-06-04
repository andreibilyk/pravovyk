# -*- coding: utf-8 -*-
import psycopg2

class SQLighter:

    def __init__(self):
        self.connection = psycopg2.connect("dbname='d43gotq6lmbhn3' user='viqqyucuojusmv' host='ec2-54-83-205-71.compute-1.amazonaws.com' password='cc1458772d0f7f750214b407228469a6c6f009d1bff544a0837cbc2771eee540'")
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM info_questions').fetchall()

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:

            return self.cursor.execute("'SELECT * FROM user_interac WHERE rowid = ?'", (rownum,)).fetchall()[0]

    def select_row(self,answer):
        with self.connection:
            return self.cursor.execute("'SELECT * FROM user_interac WHERE user_answer = ?'", (answer,)).fetchall()[0]
    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM info_questions').fetchall()
            return len(result)

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
