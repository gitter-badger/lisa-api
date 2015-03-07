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

__version__ = pbr.version.VersionInfo(
    'lisa_api').version_string()

app = Flask(__name__)

# Config

config = CONF

# Setup logger
logger = setup_log(name='lisa')

config.add_opt('DEBUG', True)
config.add_opt('SECRET_KEY', 'super-secret')
config.add_opt('DATABASE_USER', 'lisa_api')
config.add_opt('DATABASE_PASSWORD', 'lisa_password')
config.add_opt('DATABASE_NAME', 'lisa_api')
config.add_opt('DATABASE_HOST', 'localhost')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://lisa_api:lisapassword@localhost/lisa_api'


api_v1 = Blueprint('api', __name__, url_prefix='/api/1')
api = Api(api_v1, version='1.0', title='LISA API', description='L.I.S.A API',
)
logger.info("Running version: %s" % api.version)

app.register_blueprint(api_v1)

# Create database connection object
db = SQLAlchemy(app)

core = api.namespace('core', description='CORE operations')
