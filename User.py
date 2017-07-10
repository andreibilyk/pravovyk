# -*- coding: utf-8 -*-
import uuid
class User:
    def __init__(self,phone="",verified = True):
     self.phone = phone
     self.verified = verified
    def setPhone(self, phone):
     self.phone = phone
    def setCode(self, code):
     self.code = code
    def setChatid(self,code):
     self.chat_id = code
