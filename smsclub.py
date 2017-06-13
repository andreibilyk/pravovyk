# -*- coding: utf-8 -*-

import pycurl, requests
from io import StringIO
"""
    @author SMS CLUB
    @url www.smsclub.mobi
    @copyright 2017
"""

"""
    works on python2.7.x (and above) with libriary pycurl (sudo apt-get install python-pycurl)
"""
class SMSer:
 def __init__(self):
  self.login = '380731681919'  #string User ID (phone number)
  self.alphaName = 'gsm1'    #string, sender id (alpha-name) (as long as your alpha-name is not spelled out, it is necessary to use it)
  self.password = '44876ba'

 def send_text(self,abonent,text):
  print("2")
  xml = "<?xml version='1.0' encoding='utf-8'?><request_sendsms><username><![CDATA["+self.login+"]]></username><password><![CDATA["+self.password+"]]></password><from><![CDATA["+self.alphaName+"]]></from><to><![CDATA["+abonent+"]]></to><text><![CDATA["+text+"]]></text></request_sendsms>"
  b = StringIO()
  c = pycurl.Curl()
  c.setopt(c.URL, 'https://gate.smsclub.mobi/xml/')
  c.setopt(c.HTTPHEADER, ['Content-type: text/xml; charset=utf-8'])
  c.setopt(c.POSTFIELDS,xml)
  c.setopt(c.POST, 1)
  c.setopt(pycurl.WRITEFUNCTION, b.write)
  c.perform()
  response = b.getvalue()
  c.close()
  print (response)
