# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from flask import request, flash
from flask_security.forms import LoginForm, _datastore
from wtforms import StringField, PasswordField, SubmitField
from flask_security.utils import get_message, verify_and_update_password


class ExtendedLoginForm(LoginForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = request.args.get('next', '')

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        if self.username.data.strip() == '':
            flash(get_message('USER_NOT_PROVIDED'), category='error')
            self.username.errors.append(get_message('EMAIL_NOT_PROVIDED')[0])
            return False

        if self.password.data.strip() == '':
            flash(get_message('PASSWORD_NOT_PROVIDED'), category='error')
            self.password.errors.append(get_message('PASSWORD_NOT_PROVIDED')[0])
            return False

        self.user = _datastore.find_user(username=self.username.data)

        if self.user is None:
            flash(get_message('USER_DOES_NOT_EXIST'), category='error')
            self.username.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
            return False
        if not self.user.password:
            flash(get_message('PASSWORD_NOT_SET'), category='error')
            self.password.errors.append(get_message('PASSWORD_NOT_SET')[0])
            return False
        if not verify_and_update_password(self.password.data, self.user):
            flash(get_message('INVALID_PASSWORD'), category='error')
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False
        if not self.user.is_active():
            flash(get_message('DISABLED_ACCOUNT'), category='error')
            self.username.errors.append(get_message('DISABLED_ACCOUNT')[0])
            return False
        return True

