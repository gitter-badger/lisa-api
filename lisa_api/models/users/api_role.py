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
from lisa_api.lib.login import login_api

role_api = api.model('Role', {
    'id': fields.Integer(required=False, description='Role ID'),
    'name': fields.String(required=True, description='Role name (must be unique)'),
    'description': fields.String(required=True, description='Role description')
})

rolelist_parser = api.parser()
rolelist_parser.add_argument('name', type=str, required=True,
                             help='Role name (must be unique)', location='form')
rolelist_parser.add_argument('description', type=str, required=True,
                             help='Role description', location='form')

role_parser = api.parser()
role_parser.add_argument('id', type=int, required=True,
                         help='Role id', location='form')
role_parser.add_argument('name', type=str, required=True,
                         help='Role name (must be unique)', location='form')
role_parser.add_argument('description', type=str, required=True,
                         help='Role description', location='form')


@core.route('/role/<int:id>')
class RoleResource(Resource):
    """ Show a single role item and lets you modify or delete it """
    decorators = [login_api]

    @api.doc(responses={200: 'Role object', 404: 'Role not found',
                        401: 'Unauthorized access'},
             params={'id': 'The Role ID'})
    @api.marshal_with(role_api)
    def get(self, id):
        """
        This function return a single role object

        :param id: The id of the role
        :type id: int
        :returns: a role object or a 404 string + int if role not found
        :rtype: object or string + int
        """
        role = Role.query.get(id)
        if role is not None:
            return role, 200
        else:
            return 'Role not found', 404

    @api.doc(responses={204: 'Role deleted', 404: 'Role not found',
                        401: 'Unauthorized access'},
             params={'id': 'The Role ID'})
    def delete(self, id):
        """
        This function delete the given role object

        :param id: The id of the role
        :type id: int
        :returns: a 204 string + int or a 404 string + int if role is not found
        :rtype: string + int
        """
        role = Role.query.get(id)
        if role is not None:
            db.session.delete(role)
            db.session.commit()
            return 'Role has been deleted', 204
        else:
            return 'Role not found', 404

    # TODO Bug on this method, swagger send a {id} instead of the true id
    @api.doc(responses={200: 'Role updated', 404: 'Role not found',
                        401: 'Unauthorized access'},
             parser=role_parser)
    @api.marshal_with(role_api)
    def put(self, id):
        """
        This function modify a role object

        :param id: The id of the role
        :type id: int
        :returns: a 200 string + int or a 404 string + int if role is not found
        :rtype: string + int
        """
        args = role_parser.parse_args()
        role = Role.query.get(id)
        if role is not None:
            role.name = args['name']
            role.description = args['description']
            db.session.commit()
            return 'Role updated', 200
        else:
            return 'Role not found', 404


@core.route('/role')
class RoleListResource(Resource):
    """ This class return all roles and is also responsible to handle the
     creation of a role """
    decorators = [login_api]

    @api.doc(responses={200: 'Roles list', 401: 'Unauthorized access'})
    @api.marshal_list_with(role_api)
    def get(self):
        """
        This function return all role objects

        :return: a list of role objects
        :rtype: list of role objects
        """
        return Role.query.all()

    @api.doc(responses={201: 'Role added', 401: 'Unauthorized access'},
             parser=rolelist_parser)
    @api.marshal_with(role_api, code=201)
    def post(self):
        """
        This function create a role object

        :returns: a 201 string + int
        :rtype: string + int
        """
        args = rolelist_parser.parse_args()
        role = user_datastore.find_or_create_role(name=args['name'],
                                                  description=args['description'])
        db.session.commit()
        return role, 201
