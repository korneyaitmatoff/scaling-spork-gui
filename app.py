from os import path

from flask import Flask

app = Flask(__name__, template_folder=path.abspath("src/templates"))
app.config['SECRET_KEY'] = 'you-will-never-guess'

from src import routes
