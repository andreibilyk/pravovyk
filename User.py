# -*- coding: utf-8 -*-
class User:
    def __init__(self,phone="",verified = False):
     self.phone = phone
     self.verified = verified
    def setPhone(self, phone):
     self.phone = phone
    def setCode(self, code):
     self.code = code
