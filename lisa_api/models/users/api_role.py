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
from .user import Role, user_datastore

role_api = api.model('Role', {
    'name': fields.String(required=True, description='Role name'),
    'description': fields.String(required=True, description='User password')
})

role_parser = api.parser()
role_parser.add_argument('task', type=str, required=True, help='The task details', location='form')

@core.route('/role')
class RoleList(Resource):
    '''Shows a list of all roles, and lets you POST to add new roles'''
    @api.marshal_list_with(role_api)
    def get(self):
        '''List all roles'''
        return Role.query.all()

    @api.doc(parser=role_parser)
    @api.marshal_with(role_api, code=201)
    def post(self):
        '''Create a role'''
        args = role_parser.parse_args()
        user_datastore.create_role(name=args['name'],
                                   description=args['description'])
        db.session.commit()
        return '', 201
