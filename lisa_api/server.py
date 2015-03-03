from lisa_api import app, logger, db
from stevedore import extension
import models.users.api_user


class LisaApi():

    def __init__(self):
        db.create_all()
        # Setup Flask-Security
        self.logger = logger
        self.load_plugins()

    def load_plugins(self):
        # Load plugins with stevedore
        mgr = extension.ExtensionManager(
            namespace='lisa.api.plugins',
            invoke_on_load=True
        )

        self.logger.info("Loaded plugins : " + str(mgr.names()))

if __name__ == '__main__':
    LisaApi()
    app.run()