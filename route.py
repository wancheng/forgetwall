from handler.home import HomeHandler
from handler.archive import ArchiveHandler
from handler.feed import FeedHandler
from handler.entry import EntryHandler
from handler.compose import ComposeHandler
from handler.registe import RegisteHandler
from handler.authlogin import AuthLoginHandler
from handler.authlogout import AuthLogoutHandler
from handler.weixin.binding import Binding
from handler.bh import BhHandler
from handler.weixin.weixin import WeixinHandler
import handler.admin.auth
import handler.admin.wx
import handler.dispatcher
import handler.weixin.job

routes = [
	(r"/", HomeHandler),
	(r"/archive", ArchiveHandler),
	(r"/feed", FeedHandler),
	(r"/entry/([^/]+)", EntryHandler),
	(r"/compose", ComposeHandler),
	(r"/auth/login", AuthLoginHandler),
	(r"/auth/logout", AuthLogoutHandler),
	(r"/registe",RegisteHandler),
	(r"/bh",BhHandler),
	(r"/admin/login",handler.admin.auth.LoginHandler),
	#(r"/admin/index",handler.admin.auth.IndexHandler),
	#(r"/admin/wx_index",handler.admin.wx.IndexHandler),
	("/[a-z_/]*.html",handler.dispatcher.DispatcherHandler),
	("/admin/wx/[a-z]*.htm",handler.admin.wx.WXHandler),
	(r"/weixin/binding",Binding),
	("/weixin/[a-z]*.htm",handler.weixin.job.JobHandler),
	(r"/weixin",WeixinHandler)
]

