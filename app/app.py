from flask import Flask
from app.ext import configuration, database, commands
from app.blueprints import views

app = Flask(__name__)
configuration.init_app(app)
database.init_app(app)
commands.init_app(app)
views.init_app(app)

if (__name__ == '__main__'):
    app.run()
