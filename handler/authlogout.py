from base import BaseHandler

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("www_forgetwall_com_user")
        self.redirect(self.get_argument("next", "/"))


