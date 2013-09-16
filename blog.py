#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import re
import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
from handler.base import *
from route import routes
from setting import settings

class Application(tornado.web.Application):
	def __init__(self):
		tornado.web.Application.__init__(self, routes, **settings)

		# Have one global connection to the blog DB across all handlers
		self.db = torndb.Connection(
			host=options.mysql_host, database=options.mysql_database,
			user=options.mysql_user, password=options.mysql_password)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
