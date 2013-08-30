#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os.path
import re
import time
import torndb
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import logging
import hashlib
import xml.etree.ElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", HomeHandler),
			(r"/archive", ArchiveHandler),
			(r"/feed", FeedHandler),
			(r"/entry/([^/]+)", EntryHandler),
			(r"/compose", ComposeHandler),
			(r"/auth/login", AuthLoginHandler),
			(r"/auth/logout", AuthLogoutHandler),
			(r"/registe",RegisteHandler),
			(r"/bh",BhHandler),
			(r"/weixin",WeixinHandler)
		]
		settings = dict(
			blog_title=u"Forgetwall",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			ui_modules={"Entry": EntryModule},
			xsrf_cookies=False,
			cookie_secret="www_forgerwall_com",
			login_url="/auth/login",
			debug=True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)

		# Have one global connection to the blog DB across all handlers
		self.db = torndb.Connection(
			host=options.mysql_host, database=options.mysql_database,
			user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("www_forgetwall_com_user")
        if not user_id: return None
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))


class HomeHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT a.*,b.name FROM entries AS a, authors AS b WHERE a.author_id = b.id ORDER BY a.published "
                                "DESC LIMIT 5")
        self.render("home.html", entries=entries)

class RegisteHandler(BaseHandler):
	def get(self):
		open_registe = self.db.query("SELECT mvalue FROM maps WHERE mkey = 'registe'")
		if open_registe == "off":
			self.redirect("/")
		self.render("registe.html")
	def post(self):
		name = self.get_argument("name")
		password = self.get_argument("password")
		email = self.get_argument("email")
		self.db.execute("INSERT INTO authors (name,password,email) VALUES (%s,%s,%s)"
				,name,password,email)
		self.redirect("/auth/login")


class EntryHandler(BaseHandler):
	def get(self, slug):
		entry = self.db.get("SELECT a.*,b.name FROM entries AS a ,authors AS b WHERE a.author_id = b.id AND slug = %s", slug)
		if not entry: raise tornado.web.HTTPError(404)
		author = self.db.get("SELECT * FROM authors WHERE id = %s",int(entry.author_id))
		entry.username = author.name
		self.render("entry.html", entry=entry)


class ArchiveHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC")
        self.render("archive.html", entries=entries)


class FeedHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 10")
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)


class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        entry = None
        if id:
            entry = self.db.get("SELECT * FROM entries WHERE id = %s", int(id))
        self.render("compose.html", entry=entry)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = self.get_argument("html")
        # html = markdown.markdown(text)
        if id:
            entry = self.db.get("SELECT * FROM entries WHERE id = %s", int(id))
            if not entry: raise tornado.web.HTTPError(404)
            slug = entry.slug
            self.db.execute(
                "UPDATE entries SET title = %s, markdown = %s, html = %s "
                "WHERE id = %s", title, text, html, int(id))
        else:
            slug = unicodedata.normalize("NFKD", title).encode(
                "ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())
            if not slug: slug = "entry"
            while True:
                e = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
                if not e: break
                slug += "-2"
            self.db.execute(
                "INSERT INTO entries (author_id,title,slug,markdown,html,"
                "published) VALUES (%s,%s,%s,%s,%s,UTC_TIMESTAMP())",
                self.current_user.id, title, slug, text, html)
        self.redirect("/entry/" + slug)


# class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
class AuthLoginHandler(BaseHandler):
	def get(self):
		if self.current_user:
			self.redirect(self.reverse_url('/'))
		else:
			self.render('login.html')
	
	def post(self):
		name = self.get_argument("name")
		password = self.get_argument("password")
		author = self.db.get("SELECT * FROM authors WHERE name = %s AND password = %s",
			name,password)
		if not author:
			self.redirect("/")
		else:
			author_id = author["id"]
			print author_id
			self.set_secure_cookie("www_forgetwall_com_user", str(author_id))
			self.redirect(self.get_argument("next", "/"))

class BhHandler(BaseHandler):
	def get(self):
		page = self.get_argument("page","1")
		self.render('bh/'+page+'.html')

class WeixinHandler(BaseHandler):
	def get(self):
		signature = self.get_argument("signature")
		timestamp = self.get_argument("timestamp")
		nonce = self.get_argument("nonce")
		echostr = self.get_argument("echostr")
		if verification(self) and echostr is not None:
			self.write(echostr)
		else:
			self.write("access fail")

	def post(self):
		if verification(self):
			data = self.request.body
			logging.error("==data=:\n"+data)
			msg = parse_msg(data)
			if user_subscribe_event(msg):
				helpinfo = help_info(msg)
				logging.error("help:\n"+helpinfo)
				self.write(help_info(msg))
			elif is_text_msg(msg):
				content = msg['Content']
				if content == u'?' or content == u'？':
					self.write(help_info(msg))
				else:
					# books = search_book(content)
					# return rmsg
					self.write(response_text_msg(msg,"I'm sorry!"))
		self.write('message processing fail')



class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("www_forgetwall_com_user")
        self.redirect(self.get_argument("next", "/"))


class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)
	
def verification(self):
    signature = self.get_argument('signature')
    timestamp = self.get_argument('timestamp')
    nonce = self.get_argument('nonce')
    token = "wancheng"
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    if hashstr == signature:
        return True
    return False

def user_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

HELP_TPL = \
u"""
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
</Articles>
</xml>
"""
NEWSHEAD_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>%d</ArticleCount>
<Articles>
"""

NEWSITEM_TPL = \
u"""
<item>
<Title><![CDATA[%s]]></Title> 
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
"""

NEWSFOOT_TPL = \
u"""
</Articles>
</xml> 
"""
def help_info(msg):
    newshead = NEWSHEAD_TPL % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),6)
    item1 = NEWSITEM_TPL % ("点击进入...","t","http://www.forgetwall.com/static/img/index.png","http://www.forgetwall.com/bh?page=1")   
    item2 = NEWSITEM_TPL % ("当创新理念成为传统风范","","http://www.forgetwall.com/static/img/a.png","http://www.baidu.com")
    item3 = NEWSITEM_TPL % ("成就卓越 卓越成就","","http://www.forgetwall.com/static/img/3.png","http://www.baidu.com")
    item4 = NEWSITEM_TPL % ("无限成长 成长无限","","http://www.forgetwall.com/static/img/4.png","http://www.baidu.com")
    item5 = NEWSITEM_TPL % ("至真信赖 信赖至真","","http://www.forgetwall.com/static/img/5.png","http://www.baidu.com")
    item6 = NEWSITEM_TPL % ("欢迎加入我们","","http://www.forgetwall.com/static/img/a.png","http://www.baidu.com")
    return newshead+item1+item2+item3+item4+item5+item6+NEWSFOOT_TPL

TEXT_MSG_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""

def response_text_msg(msg, content):
    s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'], 
        str(int(time.time())), content)
    return s

def parse_msg(rawmsgstr):
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def is_text_msg(msg):
    return msg['MsgType'] == 'text'

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
