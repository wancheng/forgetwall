from handler.base import BaseHandler
import logging

JOBLINK_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[gh_7383b5599c17]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[link]]></MsgType>
<Title><![CDATA[%s]]></Title>
<Description><![%s]]></Description>
<Url><![CDATA[%s]]></Url>
<MsgId>1234567890123456</MsgId>
</xml> 
"""

class IndexHandler(BaseHandler):
	def get(self):
		self.render("admin/wx_index.html")

	def post(self):
		self.write("post")

class WXHandler(BaseHandler):
	def get(self):
		jobs = self.db.query("SELECT * FROM job order by id LIMIT 5")
		self.render(self.request.uri[1:],jobs=jobs)

	def post(self):
		method = self.get_argument("method")
		if method == "addJob":
			addJob(self)
		self.write("post")
		
	def addJob(self):
		sql = "INSERT INTO job (title,city,department,ability,education,experience) VALUES ( '%s','%s','%s','%s','%s','%s' )" % (self.get_argument("title"),self.get_argument("city"),self.get_argument("department"),self.get_argument("ability"),self.get_argument("education"),self.get_argument("experience"))
		logging.error(sql)
		self.db.execute(sql)
