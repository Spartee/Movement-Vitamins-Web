# project/users_api/views.py

#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, url_for, abort, jsonify, g
from project import db, auth, auth_token, app, images
from project.models import User, Screening, Vitamin
from .decorators import no_cache, etag
from project.logic import suggest_vitamins


################
#### config ####
################

users_api_blueprint = Blueprint('user_api', __name__)


##########################
#### helper functions ####
##########################

@auth.verify_password
def verify_password(email, password):
    g.user = User.query.filter_by(email=email).first()
    if g.user.role != 'admin':
        return False
    if g.user is None:
        return False
    return g.user.is_correct_password(password)


@auth_token.verify_password
def verify_authentication_token(token, unused):
    g.user = User.verify_auth_token(token)
    return g.user is not None


########################
#### error handlers ####
########################

@users_api_blueprint.errorhandler(404)
def api_error(e):
    response = jsonify({'status': 404, 'error': 'not found (API!)', 'message': 'invalid resource URI'})
    response.status_code = 404
    return response


@users_api_blueprint.errorhandler(405)
def api_error(e):
    response = jsonify({'status': 405, 'error': 'method not supported (API!)', 'message': 'method is not supported'})
    response.status_code = 405
    return response


@users_api_blueprint.errorhandler(500)
def api_error(e):
    response = jsonify({'status': 500, 'error': 'internal server error (API!)', 'message': 'internal server error occurred'})
    response.status_code = 500
    return response


@auth.error_handler
def unauthorized():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please authenticate'})
    response.status_code = 401
    return response


@auth_token.error_handler
def unauthorized_token():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please send your authentication token'})
    response.status_code = 401
    return response


################
#### routes ####
################


@users_api_blueprint.route('/api/v1/screenings', methods=['GET'])
def api_1_get_all_screenings():
    return jsonify({'screenings': [screening.export_data() for screening in Screening.query.all()]})


@users_api_blueprint.route("/api/v1/users/latest_screening/<int:user_id>", methods=["GET"])
def api_1_get_latest_screening(user_id):
    user = User.query.get_or_404(user_id)
    screening = Screening.query.filter(Screening.user_id == user.id)[-1]
    return jsonify(screening.export_data())


@users_api_blueprint.route("/api/v1/users/suggested/<int:user_id>", methods=["GET"])    
def api_1_get_suggested(user_id):
    latest_screening = Screening.query.filter(Screening.user_id == user_id).first_or_404()
    target_areas, focus_areas, squat_tag = suggest_vitamins(latest_screening)
    my_vitamins = Vitamin.query.filter((Vitamin.target_area.in_(target_areas)))
    vitamin_data = [vitamin.export_data() for vitamin in my_vitamins]
    return jsonify({"vitamin_data": vitamin_data, "target_areas": target_areas, "focus_areas": focus_areas, "squat_tag": squat_tag})



@users_api_blueprint.route('/api/v1/users/new_screening/<int:user_id>', methods=['POST'])
def api_1_new_screening(user_id):
    screening = Screening(user_id, "N","N","N","N","N","N","N","Y")
    screening.import_data(request)
    target_areas, focus_areas, squat_tag = suggest_vitamins(screening)
    db.session.add(screening)
    db.session.commit()
    my_vitamins = Vitamin.query.filter((Vitamin.target_area.in_(target_areas)))
    vitamin_data = [vitamin.export_data() for vitamin in my_vitamins]
    return jsonify({"vitamin_data": vitamin_data, "target_areas": target_areas, "focus_areas": focus_areas, "squat_tag": squat_tag})


'''
@users_api_blueprint.route('/api/v1/users/<int:vitamin_id>', methods=['GET'])
def api_1_get_vitamin(vitamin_id):
    return jsonify(Vitamin.query.get_or_404(vitamin_id).export_data())
 '''