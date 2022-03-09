import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    if not test_config:
        # load the instance config when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure instance dir exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # just say hi
    @app.route("/hello")
    def hello():
        return "hello, world!"

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
