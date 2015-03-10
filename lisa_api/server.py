from lisa_api import app, logger, db, current_api_url
from stevedore import extension
import models.users.api_user
from flask.ext.security import login_required
from flask import redirect


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

@app.route("/")
@login_required
def index():
    return redirect(location=current_api_url)


if __name__ == '__main__':
    LisaApi()
    app.run()
