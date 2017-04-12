from flask import make_response
from . import api

@api.errorhandler(401)
def unauthorized(e):
    return make_response(jsonify({'result': 'Unauthorized'}), 401)

@api.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'result': 'Page not found'}), 404)

@api.errorhandler(409)
def resource_conflict(e):
    return make_response(jsonify({'result': 'Conflict'}), 409)

@api.errorhandler(500)
def internal_herror(e):
    return make_response(jsonify({'result': 'Internal Error'}), 500)
