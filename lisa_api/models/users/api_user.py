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

from lisa_api import db, api, core
from flask.ext.restplus import Resource, fields
from .user import User, user_datastore
from .api_role import role_api

user_api_read = api.model('User', {
    'id': fields.Integer(required=True, description='User id'),
    'username': fields.String(required=True, description='User username'),
    'firstname': fields.String(required=True, description='User firstname'),
    'lastname': fields.String(required=True, description='User lastname'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'active': fields.Boolean(required=True, description='User is active or not'),
    'roles': fields.Nested(role_api, description='Role assigned to the user')
})

user_api_write = api.model('User', {
    'id': fields.Integer(required=True, description='User id'),
    'username': fields.String(required=True, description='User username'),
    'firstname': fields.String(required=True, description='User firstname'),
    'lastname': fields.String(required=True, description='User lastname'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'active': fields.Boolean(required=True, description='User is active or not'),
    'roles': fields.List(fields.String, required=True, description='Role assigned to the user')
})

user_parser = api.parser()
user_parser.add_argument('id', type=str, required=False, help='User id', location='form')
user_parser.add_argument('username', type=str, required=True, help='User username', location='form')
user_parser.add_argument('firstname', type=str, required=True, help='User firstname', location='form')
user_parser.add_argument('lastname', type=str, required=True, help='User lastname', location='form')
user_parser.add_argument('email', type=str, required=True, help='User email', location='form')
user_parser.add_argument('password', type=str, required=True, help='User password', location='form')
user_parser.add_argument('active', type=bool, required=True, help='User is active or not', location='form')
user_parser.add_argument('roles', type=str, required=True, help='List of roles names splitted by coma. Roles must already exist', location='form')


@core.route('/user')
class UserList(Resource):
    '''Shows a list of all users, and lets you POST to add new users'''
    @api.marshal_list_with(user_api_read)
    def get(self):
        '''List all users'''
        return User.query.all()

    @api.doc(parser=user_parser)
    @api.marshal_with(user_api_write, code=201)
    def post(self):
        '''Create a user'''
        args = user_parser.parse_args()
        # TODO Need to check if roles exist or not
        user_datastore.create_user(username=args['username'],
                                   email=args['email'],
                                   password=args['password'],
                                   firstname=args['firstname'],
                                   lastname=args['lastname'],
                                   active=args['active'],
                                   roles=args['roles'])
        db.session.commit()
        return '', 201

    @api.doc(responses={204: 'User deleted'})
    def delete(self):
        '''Delete a given resource'''
        args = user_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user is not None:
            db.session.delete(user)
        return '', 204

    @api.doc(parser=user_parser)
    @api.marshal_with(user_api_write)
    def put(self, todo_id):
        '''Update a given resource'''
        args = user_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        # TODO Need to check if roles exist or not
        if user is not None:
            user = args
