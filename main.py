import webapp2
import os
import jinja2
import re
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))	

class Article(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return render_str("home.html", p = self)

class MainPage(Handler):
	def get(self):
		articles = db.GqlQuery("SELECT * FROM Article ORDER BY created DESC limit 10")
		self.render("home.html", articles = articles)

# 	def post(self):
# 		have_error = False
# 		user = self.request.get("username")
# 		passw = self.request.get("pass")
# 		vpassw = self.request.get("vpass")
# 		mail = self.request.get("mail")

# 		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
# 		PASS_RE = re.compile(r"^.{3,20}$")
# 		MAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

# 		params = dict(username = user,
# 					email = mail)

# 		def validUser(user):
# 			return USER_RE.match(user)

# 		def validPass(passw):
# 			return PASS_RE.match(passw)

# 		def validMail(mail):
# 			return MAIL_RE.match(mail)

# 		if not validUser(user):
# 			params['err_username'] = 'Not a valid Username'
# 			have_error = True

# 		if not validPass(passw):
# 			params['err_verify'] = 'Not a valid Password'
# 			have_error = True

# 		if not validMail(mail):
# 			have_error = True

# 		if have_error:
# 			self.render("index.html", **params)

# 		if not have_error:
# 			self.redirect("/welcome?username=" + user) 
			
# class WelcomePage(Handler):
# 	def get(self):
# 		username = self.request.get("username")
# 		self.render("welcome.html", user = username)

class AddArticle(Handler):
	def get(self):
		self.render("article.html")	

	def post(self):
		title = self.request.get('title')
		content = self.request.get('content')

		if title and content:
			a = Article(title = title, content = content.replace("\n","<br>"))
			a.put()

			articles = db.GqlQuery("SELECT * FROM Article ORDER BY created DESC limit 10")
			self.redirect('/blog')
		else:
			error = "Enter Both"
			self.render("article.html", error = error)


app = webapp2.WSGIApplication([('/blog', MainPage),
							   ('/add', AddArticle)
							   ], debug=True)
