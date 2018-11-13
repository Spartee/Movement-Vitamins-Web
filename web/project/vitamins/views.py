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



################
#### routes ####
################

@vitamins_blueprint.route('/')
def home_page():
    public_vitamins = Vitamin.query.filter((Vitamin.link != "")).limit(4)
    return render_template('home_page.html', public_vitamins=public_vitamins)

@vitamins_blueprint.route('/vitamins/<target_area>')
def all_vitamins(target_area='All'):
    if target_area in ['Hips', 'Ankle', 'Shoulder Flexion', 'Shoulder Rotation', 'Foot', 'Upper Body']:
        my_vitamins = Vitamin.query.filter((Vitamin.target_area == target_area))
        return render_template('all_vitamins.html', all_vitamins=my_vitamins, target_area=target_area)
    elif target_area == 'All':
        my_vitamins = Vitamin.query.filter((Vitamin.target_area != ""))
        return render_template('all_vitamins.html', all_vitamins=my_vitamins, target_area=target_area)
    else:
        flash('ERROR! Invalid target area selected.', 'error')

    return redirect(url_for('vitamins.home_page'))


@vitamins_blueprint.route('/vitamin/<vitamin_id>')
def vitamin_details(vitamin_id):
    
    vitamin = Vitamin.query.filter_by(id=vitamin_id).first_or_404()
    return render_template('vitamin_detail.html', vitamin=vitamin)
  
  





