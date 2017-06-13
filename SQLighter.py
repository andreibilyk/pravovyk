# -*- coding: utf-8 -*-
import psycopg2
import logging
class SQLighter:

    def __init__(self):
        self.connection = psycopg2.connect("dbname='d43gotq6lmbhn3' user='viqqyucuojusmv' host='ec2-54-83-205-71.compute-1.amazonaws.com' password='cc1458772d0f7f750214b407228469a6c6f009d1bff544a0837cbc2771eee540'")
        self.cursor = self.connection.cursor()

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            self.cursor.execute('SELECT * FROM user_interac WHERE id = %s' % str(rownum))
            return self.cursor.fetchall()[0]

    def select_row(self,answer):
        with self.connection:
            self.cursor.execute('SELECT * FROM user_interac WHERE user_answer = '+"'"+str(answer)+"'")
            return self.cursor.fetchall()[0]

    def select_file(self,answer):
        with self.connection:
            self.cursor.execute('SELECT * FROM user_interac WHERE user_answer = '+"'"+str(answer)+"'")
            info = self.cursor.fetchall()[0]
            if info[7]:
                return info[7]
            else:
                return
    def user_verified(self,phone):
     with self.connection:
         self.cursor.execute('SELECT * FROM users WHERE phone_number = '+"'"+phone+"'")
         info = self.cursor.fetchall()[0]
         if info:
             return True
         else:
             return False

    def user_verify(self,phone):
     with self.connection:
        self.cursor.execute('INSERT INTO users (phone_number,verified) VALUES (%s,True)'%phone)
        self.connection.commit()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
