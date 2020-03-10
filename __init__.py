from flask import Flask
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = 'fbaubfaibiuab21312/f'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'lyx09241021/?'
app.config['MYSQL_DATABASE_DB'] = 'TeachSystem'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.config.from_object(Config)
#api = Blueprint('api',__name__)
login = LoginManager(app)


