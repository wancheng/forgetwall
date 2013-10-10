from handler.base import BaseHandler
import logging

class JobHandler(BaseHandler):
	def get(self):
		method = self.get_argument("method")
		if method == "list":
			jobs = self.db.query("SELECT * FROM job ORDER BY ID LIMIT 10")
			url = self.request.uri[1:-12]
			logging.error(url)
			self.render("weixin/jobs.htm",jobs=jobs)
		elif method == "info":
			id = self.get_argument("id")
			job = self.db.get("SELECT * FROM job WHERE id = %s",int(id))
			self.render("weixin/job.htm",job=job)
		else:
			self.write("ERROR")

	"""
		jobid = self.get_argument("id")
		job = self.db.query("SELECT * FROM job WHERE id = %s",jobid)
		if not job:
			self.write("error")
		else:
			self.render("weixin/job.html",job=job)
	"""
