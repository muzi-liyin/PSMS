from flask.ext.script import Manager, Server
import main
import PSMS

manager = Manager(PSMS.app)

manager.add_command("server", Server())
@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=PSMS.app,
                db = main.db,
                Users=main.models.Users)

if __name__ == '__main__':
    manager.run()