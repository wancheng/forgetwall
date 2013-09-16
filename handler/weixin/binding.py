from handler.base import BaseHandler

class Binding(BaseHandler):
	def get(self):
		weixinid = self.get_argument("weixinid")
		print weixinid
		self.render("weixin/binding.html",weixinid=weixinid)

	def post(self):
		employeeid = self.get_argument("employeeid")
		ename = self.get_argument("ename")
		weixinid = self.get_argument("weixinid")
		print employeeid
		print ename
		employees = self.db.query("SELECT * FROM employee WHERE employeeid = %s AND ename = %s",employeeid,ename)
		if not employees:
			self.render("weixin/info.html",info="error!",css="error")
		else:
			self.db.execute("UPDATE weixin_user SET employeeid = %s WHERE weixinid = %s",employeeid,weixinid)
			self.render("weixin/info.html",info="success!",css="success")
