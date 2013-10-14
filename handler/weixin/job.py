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
		jobid = self.get_argument("jobid")
		sql = "INSERT INTO job_candidate (jobid,weixinid,resume) VALUES (%s,'%s','%s')" % (jobid,weixinid,resume)
		logging.error(sql)
		self.db.execute(sql)
		self.write("success")

	"""
		jobid = self.get_argument("id")
		job = self.db.query("SELECT * FROM job WHERE id = %s",jobid)
		if not job:
			self.write("error")
		else:
			self.render("weixin/job.html",job=job)
	"""
