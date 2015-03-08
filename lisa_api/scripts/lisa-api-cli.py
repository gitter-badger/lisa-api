from flask.ext.script import Manager

from lisa_api import app, logger, db
from lisa_api.models.users.user import user_datastore
from flask.ext.security.utils import encrypt_password

manager = Manager(app)

@manager.command
def create_user():
    admin_role = user_datastore.find_or_create_role(name='admin',
                                                    description='Admin role')
    if user_datastore.find_user(username='lisa') is None:
        lisa_user = user_datastore.create_user(username='lisa',
                                               firstname='lisa',
                                               lastname='alive',
                                               email='lisa@lisa-project.net',
                                               password=encrypt_password('lisa'),
                                               active=True)
        user_datastore.add_role_to_user(user=lisa_user, role=admin_role)
    db.session.commit()
    logger.info("Creating user")

if __name__ == "__main__":
    manager.run()