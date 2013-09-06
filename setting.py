import os
from tornado.options import define,options
from handler.entry import EntryModule

define("port", default=80, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")

settings = {}
settings['blog_title'] = u"Forgetwall"
settings['template_path'] = os.path.join(os.path.dirname(__file__),"templates")
settings['static_path'] = os.path.join(os.path.dirname(__file__),"static")
settings['ui_modules'] = {"Entry":EntryModule}
settings['xsrf_cookies'] = False
settings['cookie_secret'] = "www_forgetwall_com"
settings['login_url'] = "/auth/login"
settings['debug'] = True
