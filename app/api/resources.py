from flask import jsonify, request, abort
from flask.views import MethodView
from flask_mail import Message
from .. import db, mail
from ..models import Post, User
from .authorization import auth, confirm_token, generate_confirmation_token, user_confirmed


def send_mail_with_token(email, token):
    """Send email with the confirmation token"""
    msg = Message()
    msg.add_recipient(email)
    msg.subject = 'Account Verification'
    msg.sender = "Pig Latin <admin@piglatin.com>"
    msg.body = 'Token Verification: ' + token
    mail.send(msg)


class PostView(MethodView):

    def get(self, _id=None):
        """Get posts"""
        # /posts and /posts/<int:_id>
        if _id is None:
            posts = Post.query.all()
            return jsonify([i.serialize for i in posts])
        else:
            post = Post.query.get(_id)
            if not post:
                abort(404)
            return jsonify(post.serialize)

    @auth.login_required
    @user_confirmed
    def post(self):
        # /posts
        authorization = request.authorization
        user = User.query.filter_by(email=authorization.username).first()
        request_data = request.get_json()
        post = Post(request_data['original'], user.id)
        db.session.add(post)
        db.session.commit()
        return jsonify(post.serialize)

    @auth.login_required
    @user_confirmed
    def put(self, _id):
        # /posts/<int:_id>
        post = Post.query.get(id)

        authorization = request.authorization
        user = User.query.filter_by(email=authorization.username).first()

        # Post Exists
        if not post:
            abort(404)

        # User is the owner of the post
        if post.user_id != user.id:
            abort(401)

        request_data = request.get_json()
        post.original = request_data['original']
        post.set_translation(request_data['original'])

        db.session.commit()

        return jsonify(post.serialize)

    @auth.login_required
    @user_confirmed
    def delete(self, _id):
        # /posts/<int:_id>
        # Get the current user
        authorization = request.authorization
        user = User.query.filter_by(email=authorization.username).first()

        post = Post.query.get(id)

        if not post:
            abort(404)

        # User is the owner of the post
        if post.user_id != user.id:
            abort(401)

        db.session.delete(post)
        db.session.commit()

        return jsonify({'result': True})


class UserView(MethodView):

    @auth.login_required
    def get(self, token):
        # /confirm/token
        try:
            email = confirm_token(token)
        except:
            abort(401)
        else:
            user = User.query.filter_by(email=email).first()

            if user.confirmed:
                return jsonify({'status': 'already confirmed'})
            else:
                user.confirm()
                db.session.add(user)
                db.session.commit()

            return jsonify(user.serialize)

    def post(self):
        # /users
        """Create a new user"""
        request_data = request.get_json()

        user = User(request_data['email'], request_data['password'])
        try:
            db.session.add(user)
            db.session.commit()
        except:
            abort(409)

        token = generate_confirmation_token(user.email)

        send_mail_with_token(user.email, token)

        return jsonify(user.serialize)
