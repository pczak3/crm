from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    Bootstrap(app)

    with app.app_context():
        # import parts of our application
        from . import routes, models
        return app
