# coding=utf-8 
# @Time : 2018/8/10 16:53 
# @Author : achjiang
# @File : message_urls.py
from handlers.message import message_handler

message_urls = [
	(r'/message/message',message_handler.MessageHandler),
	(r'/message/message_websocket',message_handler.MessageWebHandler),
]