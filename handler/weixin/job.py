from handler.base import BaseHandler
import logging

class JobHandler(BaseHandler):
	def get(self):
		method = self.get_argument("method")
		weixinid = self.get_argument("weixinid")
		if method == "list":
			jobs = self.db.query("SELECT * FROM job ORDER BY ID LIMIT 10")
			self.render("weixin/jobs.htm",jobs=jobs,weixinid=weixinid)
		elif method == "info":
			id = self.get_argument("id")
			job = self.db.get("SELECT * FROM job WHERE id = %s",int(id))
			self.render("weixin/job.htm",job=job,weixinid=weixinid)
		else:
			self.write("ERROR")
	def post(self):
		weixinid = self.get_argument("weixinid")
		resume = self.get_argument("resume")
		logging.error(weixinid)
		logging.error(resume)
		self.write("success")

	"""
		jobid = self.get_argument("id")
		job = self.db.query("SELECT * FROM job WHERE id = %s",jobid)
		if not job:
			self.write("error")
		else:
			self.render("weixin/job.html",job=job)
	"""
