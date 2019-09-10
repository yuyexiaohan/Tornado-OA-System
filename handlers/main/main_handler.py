# coding=utf-8

from handlers.base.base_handler import BaseHandler


class MainHandler(BaseHandler):
	def get(self):
		self.write('main.html')
		# self.render('main.html')
