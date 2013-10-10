from handler.base import BaseHandler

class JobHandler(BaseHandler):
	def get(self):
		jobid = self.get_argument("id")
		job = self.db.query("SELECT * FROM job WHERE id = %s",jobid)
		if not job:
			self.write("error")
		else:
			self.render("weixin/job.html",job=job)
