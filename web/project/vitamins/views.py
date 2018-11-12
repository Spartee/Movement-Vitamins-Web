# project/vitamins/views.py

#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, url_for, flash, abort, jsonify
from flask_login import current_user, login_required
from project import db, images, app
from project.models import Vitamin, User
from .forms import AddVitaminsForm, EditVitaminsForm
from random import random
from twilio.rest import TwilioRestClient


################
#### config ####
################

vitamins_blueprint = Blueprint('vitamins', __name__)
"""TODO: change this views to reflect forms created in this folder"""

##########################
#### helper functions ####
##########################

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')


def get_all_vitamins_with_users():
    # SQL: SELECT * FROM vitamins JOIN users ON vitamins.user_id = users.id;
    return db.session.query(Vitamin, User).join(User).all()



################
#### routes ####
################

@vitamins_blueprint.route('/')
def public_vitamins():
    all_public_vitamins = Vitamin.query.filter(Vitamin.link != "").limit(4)
    return render_template('public_vitamins.html', public_vitamins=all_public_vitamins)


@vitamins_blueprint.route('/abc')
def public_vitamins2():
    return '<h1>Hello world!</h1>'


@vitamins_blueprint.route('/vitamins/<target_area>')
def all_vitamins(target_area='All'):
    if target_area in ['hips', 'back', 'shoulders', 'abs']:
        my_vitamins = Vitamin.query.filter((Vitamin.target_area == target_area))
        return render_template('all_vitamins.html', user_vitamins=my_vitamins, target_area=target_area)
    elif target_area == 'All':
        my_vitamins = Vitamin.query()
        return render_template('all_vitamins.html', user_vitamins=my_vitamins, target_area=target_area)
    else:
        flash('ERROR! Invalid target area selected.', 'error')

    return redirect(url_for('vitamins.public_vitamins'))


@vitamins_blueprint.route('/vitamin/<vitamin_id>')
def vitamin_details(recipe_id):
    
    vitamin = Recipe.query.filter_by(id=vitamin_id).first_or_404()
    return render_template('vitamin_detail.html', vitamin=vitamin)




