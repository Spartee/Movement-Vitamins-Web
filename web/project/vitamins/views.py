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


################
#### routes ####
################

@vitamins_blueprint.route('/')
def home_page():
    return render_template('home_page.html')


@vitamins_blueprint.route('/edit/<vitamin_id>', methods=['GET', 'POST'])
@login_required
def edit_vitamin(vitamin_id):
    """TODO: change this view to allow editing vitamins"""
    # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
    # sent to the form.  This will cause AddRecipeForm to not see the file data.
    # Flask-WTF handles passing form data to the form, so not parameters need to be included.
    form = EditVitaminsForm()
    recipe = Recipe.query.filter_by(id=vitamin_id).first_or_404()
    '''
    if not recipe.user_id == current_user.id:
        flash('Error! Incorrect permissions to edit this recipe.', 'error')
        return redirect(url_for('recipes.public_recipes'))

    if request.method == 'POST':
        if form.validate_on_submit():
            update_counter = 0

            if form.recipe_title.data is not None and form.recipe_title.data != recipe.recipe_title:
                flash('DEBUG: Updating recipe.recipe_title to {}.'.format(form.recipe_title.data), 'debug')
                update_counter += 1
                recipe.recipe_title = form.recipe_title.data

            if form.recipe_description.data is not None and form.recipe_description.data != recipe.recipe_description:
                flash('DEBUG: Updating recipe.recipe_description to {}.'.format(form.recipe_description.data), 'debug')
                update_counter += 1
                recipe.recipe_description = form.recipe_description.data

            if form.recipe_public.data != recipe.is_public:
                flash('DEBUG: Updating recipe.is_public to {}.'.format(form.recipe_public.data), 'debug')
                update_counter += 1
                recipe.is_public = form.recipe_public.data

            if form.recipe_dairy_free.data != recipe.dairy_free_recipe:
                flash('DEBUG: Updating recipe.dairy_free_recipe to {}.'.format(form.recipe_dairy_free.data), 'debug')
                update_counter += 1
                recipe.dairy_free_recipe = form.recipe_dairy_free.data

            if form.recipe_soy_free.data != recipe.soy_free_recipe:
                flash('DEBUG: Updating recipe.soy_free_recipe to {}.'.format(form.recipe_soy_free.data), 'debug')
                update_counter += 1
                recipe.soy_free_recipe = form.recipe_soy_free.data

            if form.recipe_type.data != recipe.recipe_type:
                flash('DEBUG: Updating recipe.recipe_type to {}.'.format(form.recipe_type.data), 'debug')
                update_counter += 1
                recipe.recipe_type = form.recipe_type.data

            if form.recipe_rating.data != str(recipe.rating):
                flash('DEBUG: Updating recipe.rating from {} to {}.'.format(str(recipe.rating), form.recipe_rating.data), 'debug')
                update_counter += 1
                recipe.rating = form.recipe_rating.data

            if form.recipe_image.has_file():
                flash('DEBUG: Updating recipe.image_filename to {}.'.format(form.recipe_image.data), 'debug')
                update_counter += 1
                filename = images.save(request.files['recipe_image'])
                recipe.image_filename = filename
                recipe.image_url = images.url(filename)

            if form.recipe_ingredients.data != recipe.ingredients:
                flash('DEBUG: Updating recipe.ingredients to {}.'.format(form.recipe_ingredients.data), 'debug')
                update_counter += 1
                recipe.ingredients = form.recipe_ingredients.data

            if form.recipe_steps.data != recipe.recipe_steps:
                flash('DEBUG: Updating recipe.recipe_steps to {}.'.format(form.recipe_steps.data), 'debug')
                update_counter += 1
                recipe.recipe_steps = form.recipe_steps.data

            if form.recipe_inspiration.data is not None and form.recipe_inspiration.data != recipe.inspiration:
                flash('DEBUG: Updating recipe.inspiration to {}.'.format(form.recipe_inspiration.data), 'debug')
                update_counter += 1
                recipe.inspiration = form.recipe_inspiration.data

            if update_counter > 0:
                db.session.add(recipe)
                db.session.commit()
                flash('Recipe has been updated for {}.'.format(recipe.recipe_title), 'success')
            else:
                flash('No updates made to the recipe ({}). Please update at least one field.'.format(recipe.recipe_title), 'error')

            return redirect(url_for('recipes.recipe_details', recipe_id=recipe_id))
        else:
            flash_errors(form)
            flash('ERROR! Recipe was not edited.', 'error')

    return render_template('edit_recipe.html', form=form, recipe=recipe)
    '''
    return "To be completed"

@users_blueprint.route('/movement_screenings')
@login_required
def admin_view_users():
    if current_user.role != 'admin':
        abort(403)
    else:
        users = User.query.order_by(User.id).all()
        return render_template('movement_screenings.html', users=users)
    return redirect(url_for('users.login'))


