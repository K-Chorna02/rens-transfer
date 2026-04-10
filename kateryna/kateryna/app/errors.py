from flask import render_template, Blueprint
from werkzeug.exceptions import InternalServerError


error_bp = Blueprint('errors', __name__)

@error_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@error_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@error_bp.app_errorhandler(InternalServerError)
def application_error(error):
    return render_template('errors/500.html'), 500

