# project/recipes/views.py

#################
#### imports ####
#################

from flask import render_template, Blueprint, request, redirect, url_for, flash, abort, jsonify
from flask_login import current_user, login_required
from project import db, images, app
from project.models import Recipe, User
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


def get_all_recipes_with_users():
    # SQL: SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;
    return db.session.query(Recipe, User).join(User).all()


def send_new_recipe_text_message(user_email, recipe_title):
    client = TwilioRestClient(app.config['ACCOUNT_SID'], app.config['AUTH_TOKEN'])
    message = client.messages.create(
        body="Kennedy Family Recipes... {} added a new recipe: {}".format(user_email, recipe_title),  # Message body, if any
        to=app.config['ADMIN_PHONE_NUMBER'],
        from_=app.config['TWILIO_PHONE_NUMBER']
    )
    # flash('Text message sent to {}: {}'.format(app.config['ADMIN_PHONE_NUMBER'], message.body), 'success')
    return


################
#### routes ####
################

@recipes_blueprint.route('/')
def public_recipes():
    all_public_recipes = Recipe.query.filter(Recipe.is_public == True, Recipe.image_url != None).order_by(Recipe.rating.desc()).limit(4)
    return render_template('public_recipes.html', public_recipes=all_public_recipes)


@recipes_blueprint.route('/abc')
def public_recipes2():
    return '<h1>Hello world!</h1>'


@recipes_blueprint.route('/recipes/<recipe_type>')
def user_recipes(recipe_type='All'):
    if recipe_type in ['Breakfast', 'Lunch', 'Dinner', 'Dessert', 'Side Dish', 'Drink']:
        if current_user.is_authenticated:
            my_recipes = Recipe.query.filter(((Recipe.user_id == current_user.id) & (Recipe.recipe_type == recipe_type)) | ((Recipe.is_public == True) & (Recipe.recipe_type == recipe_type)))
        else:
            my_recipes = Recipe.query.filter((Recipe.is_public == True) & (Recipe.recipe_type == recipe_type))
        return render_template('user_recipes.html', user_recipes=my_recipes, recipe_type=recipe_type)
    elif recipe_type == 'All':
        if current_user.is_authenticated:
            my_recipes = Recipe.query.filter((Recipe.user_id == current_user.id) | (Recipe.is_public == True))
        else:
            my_recipes = Recipe.query.filter(Recipe.is_public == True)
        return render_template('user_recipes.html', user_recipes=my_recipes, recipe_type=recipe_type)
    else:
        flash('ERROR! Invalid recipe type selected.', 'error')

    return redirect(url_for('recipes.public_recipes'))


@recipes_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
    # sent to the form.  This will cause AddRecipeForm to not see the file data.
    # Flask-WTF handles passing form data to the form, so not parameters need to be included.
    form = AddRecipeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = images.save(request.files['recipe_image'])
            url = images.url(filename)
            new_recipe = Recipe(form.recipe_title.data,
                                form.recipe_description.data,
                                current_user.id,
                                form.recipe_public.data,
                                filename,
                                url,
                                form.recipe_type.data,
                                form.recipe_rating.data,#  or None,
                                form.recipe_ingredients.data,
                                form.recipe_steps.data,
                                form.recipe_inspiration.data,
                                form.recipe_dairy_free.data,
                                form.recipe_soy_free.data)
            db.session.add(new_recipe)
            db.session.commit()
            if 'ACCOUNT_SID' in app.config and not app.config['TESTING']:
                new_user = User.query.filter_by(id=new_recipe.user_id).first()
                send_new_recipe_text_message(new_user.email, new_recipe.recipe_title)
            flash('New recipe, {}, added!'.format(new_recipe.recipe_title), 'success')
            return redirect(url_for('recipes.user_recipes', recipe_type='All'))
        else:
            flash_errors(form)
            flash('ERROR! Recipe was not added.', 'error')

    return render_template('add_recipe.html', form=form)


@recipes_blueprint.route('/recipe/<recipe_id>')
def recipe_details(recipe_id):
    # recipe_with_user = db.session.query(Recipe, User).join(User).filter(Recipe.id == recipe_id).first_or_404()
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()

    if recipe.is_public:
        return render_template('recipe_detail.html', recipe=recipe)
    else:
        if current_user.is_authenticated and recipe.user_id == current_user.id:
            return render_template('recipe_detail.html', recipe=recipe)
        else:
            flash('Error! Incorrect permissions to access this recipe.', 'error')

    return redirect(url_for('recipes.public_recipes'))


@recipes_blueprint.route('/delete/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()

    if not recipe.user_id == current_user.id:
        flash('Error! Incorrect permissions to delete this recipe.', 'error')
        return redirect(url_for('recipes.public_recipes'))

    db.session.delete(recipe)
    db.session.commit()
    flash('{} was deleted.'.format(recipe.recipe_title), 'success')
    return redirect(url_for('recipes.user_recipes', recipe_type='All'))


@recipes_blueprint.route('/edit/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
    # sent to the form.  This will cause AddRecipeForm to not see the file data.
    # Flask-WTF handles passing form data to the form, so not parameters need to be included.
    form = EditRecipeForm()
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()

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


