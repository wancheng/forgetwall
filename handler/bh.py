from base import BaseHandler

class BhHandler(BaseHandler):
	def get(self):
		page = self.get_argument("page","1")
		self.render('bh/'+page+'.html')


