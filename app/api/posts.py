from flask import jsonify, request
from . import api
from .. import db
from ..models import Post, User
from .authorization import auth, user_confirmed

@api.route('/posts', methods=['GET'])
def posts_list():
	posts = Post.query.all()
	return jsonify([i.serialize for i in posts])

@api.route('/posts/<int:id>', methods=['GET'])
def posts_get(id):
	'''Get post by id'''
	post = Post.query.get(id)

	if not post:
		return make_response('Invalide post ID', 409)

	return jsonify(post.serialize)

@api.route('/posts', methods=['POST'])
@auth.login_required
@user_confirmed
def posts_create():
	auth = request.authorization
	user = User.query.filter_by(email=auth.username).first()
	request_data = request.get_json()
	post = Post(request_data['original'], user.id)
	db.session.add(post)
	db.session.commit()
	return jsonify(post.serialize)

@api.route('/posts/<int:id>', methods=['PUT'])
@auth.login_required
@user_confirmed
def posts_update(id):
	post = Post.query.get(id)

	# Post Exists
	if not post:
		return make_response('Invalide post ID', 409)

	# User is the owner of the post
	if post.user_id != user.id:
		return make_response('Unauthorized', 401)

	request_data = request.get_json()
	post.original = request_data['original']
	post.set_translation(request_data['original'])

	db.session.commit()

	return jsonify(post.serialize)


@api.route('/posts/<int:id>', methods=['DELETE'])
@auth.login_required
@user_confirmed
def posts_delete(id):
	# Get the current user
	auth = request.authorization
	user = User.query.filter_by(email=auth.username).first()

	post = Post.query.get(id)

	# User is the owner of the post
	if post.user_id != user.id:
		return make_response('Unauthorized', 401)

	db.session.delete(post)
	db.session.commit()

	return jsonify({'result': True})
