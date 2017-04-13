from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config
from .api import api as api_blueprint
from .api.resources import PostView, UserView


db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	db.init_app(app)
	mail.init_app(app)

	posts_as_view = PostView.as_view('posts')
	users_as_view = UserView.as_view('users')

	api_blueprint.add_url_rule('/posts', view_func=posts_as_view, methods=['GET', 'POST'])
	api_blueprint.add_url_rule('/posts/<int:_id>', view_func=posts_as_view, methods=['GET', 'PUT', 'DELETE'])
	api_blueprint.add_url_rule('/users', view_func=users_as_view, methods=['POST'])
	api_blueprint.add_url_rule('/confirm/<token>', view_func=users_as_view, methods=['GET'])

	app.register_blueprint(api_blueprint, url_prefix='/api/v1')

	return app

