from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)

import routes
