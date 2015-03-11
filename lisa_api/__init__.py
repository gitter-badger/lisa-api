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

import pbr.version
from flask import Flask, Blueprint
from flask.ext.restplus import Api
from flask.ext.sqlalchemy import SQLAlchemy
from .lib.logger import setup_log
from .lib.conf import CONF
from .lib.login import custom_unauthorized

__version__ = pbr.version.VersionInfo(
    'lisa_api').version_string()

app = Flask(__name__)
# Setup logger
logger = setup_log(name='lisa')

# Config
config = CONF

config.add_opt(name='debug', value=True, section='api')
config.add_opt(name='secret_key', value='super-secret', section='api')
config.add_opt(name='db_type', value='mysql', section='api')
config.add_opt(name='db_user', value='lisa_api', section='api')
config.add_opt(name='db_password', value='lisapassword', section='api')
config.add_opt(name='db_name', value='lisa_api', section='api')
config.add_opt(name='db_host', value='localhost', section='api')

try:
    app.config['DEBUG'] = config.api.debug
    app.config['SECRET_KEY'] = config.api.secret_key

    if config.api.db_type == "mysql":
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            "{db_type}://{db_user}:{db_password}@{db_host}/{db_name}".format(
                db_type=config.api.db_type, db_user=config.api.db_user,
                db_password=config.api.db_password, db_host=config.api.db_host,
                db_name=config.api.db_name
            )
except AttributeError:
    logger.error("A field is missing from the configuration file")

current_api_url = '/api/1'

app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login_user.html'
app.config['SECURITY_POST_LOGIN_VIEW'] = current_api_url
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'shesalive!alive!'

# Register the API
api_v1 = Blueprint('api', __name__, url_prefix=current_api_url)
api = Api(api_v1, version='1.0', title='LISA API', description='L.I.S.A API')
api.unauthorized = custom_unauthorized
app.register_blueprint(api_v1)
logger.info("Running API version: %s" % api.version)

core = api.namespace('core', description='CORE operations')

# Create database connection object
db = SQLAlchemy(app)
