from handler.base import BaseHandler
import logging

class IndexHandler(BaseHandler):
	def get(self):
		self.render("admin/wx_index.html")

	def post(self):
		self.write("post")

class WXHandler(BaseHandler):
	def get(self):
		method = self.get_argument("method")
		if method == "list":
			myvar = self.db.query("SELECT * FROM job order by id")
		elif method == "info":
			id = self.get_argument("id")
			sql = "select employee.cfname,employee.cname,job_candidate.resume from employee,job_candidate,job,weixin_user where job_candidate.jobid=job.id and job_candidate.weixinid=weixin_user.weixinid and weixin_user.employeeid=employee.employeeid and job.id = %s" % int(id)
			logging.error(sql)
			myvar = self.db.get("SELECT * FROM job WHERE id = %s",int(id))
			myvar.resumes = self.db.get(sql)
			if not myvar.resumes:
				myvar.resumes = {}
			logging.error(myvar)
		self.render(self.request.path[1:],myvar=myvar)

	def post(self):
		method = self.get_argument("method")
		if method == "addJob":
			sql = "INSERT INTO job (title,city,department,ability,education,experience) VALUES ( '%s','%s','%s','%s','%s','%s' )" % (self.get_argument("title"),self.get_argument("city"),self.get_argument("department"),self.get_argument("ability"),self.get_argument("education"),self.get_argument("experience"))
			self.db.execute(sql)
			self.redirect("jobs.htm")
