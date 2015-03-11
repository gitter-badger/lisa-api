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

from lisa_api import db, app
from lisa_api.models.users.user import user_datastore
from flask.ext.security.utils import encrypt_password
import click


@click.group()
def user():
    pass

@user.command()
@click.argument('username', default='lisa')
@click.option('--firstname', default='lisa', help='Firstname of the user')
@click.option('--lastname', default='alive', help='Lastname of the user')
@click.option('--email', default='lisa@lisa-project.net',
              help='Email of the user')
@click.password_option(default='lisa', help='Password of the user')
def create_user(username, firstname, lastname, email, password):
    with app.app_context():
        admin_role = user_datastore.find_or_create_role(name='admin',
                                                        description='Admin role')
        if user_datastore.find_user(username=username) is None:
            lisa_user = user_datastore.create_user(username=username,
                                                   firstname=firstname,
                                                   lastname=lastname,
                                                   email=email,
                                                   password=encrypt_password(password),
                                                   active=True)
            user_datastore.add_role_to_user(user=lisa_user, role=admin_role)
        db.session.commit()
    click.echo("Creating user %s" % username)

cli = click.CommandCollection(sources=[user])

if __name__ == '__main__':
    cli()