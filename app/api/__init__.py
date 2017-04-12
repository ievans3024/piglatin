from flask import Blueprint
from ..models import User

api = Blueprint('api', __name__)

from . import users, posts
