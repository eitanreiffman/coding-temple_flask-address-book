from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-super-secretive-hard-to-guess-key'

from . import routes