from flask_security.forms import LoginForm
from wtforms import StringField


class ExtendedLoginForm(LoginForm):
    username = StringField('Username')
