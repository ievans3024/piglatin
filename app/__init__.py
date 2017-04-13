from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config


db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	db.init_app(app)
	mail.init_app(app)

	from .api import api as api_blueprint
	from .api.resources import ReadPostView, WritePostView, UserConfirmView, UserCreateView

	read_posts = ReadPostView.as_view('read_posts')
	read_post = ReadPostView.as_view('read_post')
	write_posts = WritePostView.as_view('write_posts')
	create_users = UserCreateView.as_view('create_users')
	confirm_users = UserConfirmView.as_view('confirm_users')

	api_blueprint.add_url_rule('/posts', view_func=read_posts)
	api_blueprint.add_url_rule('/posts', view_func=write_posts, methods=['POST'])
	api_blueprint.add_url_rule('/posts/<int:_id>', view_func=read_post, methods=['GET'])
	api_blueprint.add_url_rule('/posts/<int:_id>', view_func=write_posts, methods=['PUT', 'DELETE'])
	api_blueprint.add_url_rule('/users', view_func=create_users)
	api_blueprint.add_url_rule('/confirm/<token>', view_func=confirm_users)

	try:
		app.register_blueprint(api_blueprint, url_prefix='/api/v1')
	except AssertionError:
		# blueprint has already been registered
		pass

	return app
