# project/recipes/forms.py


from flask_wtf import Form
from wtforms import StringField, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_pagedown.fields import PageDownField
from project import images


class AddRecipeForm(Form):
    recipe_title = StringField('Recipe Title', validators=[DataRequired()])
    recipe_description = StringField('Recipe Description', validators=[DataRequired()])
    recipe_public = BooleanField('Public Recipe', default="")
    recipe_dairy_free = BooleanField('Dairy-Free Recipe', default="")
    recipe_soy_free = BooleanField('Soy-Free Recipe', default="")
    recipe_type = RadioField('Recipe Type', validators=[DataRequired()],
                             choices=[('Breakfast', 'Breakfast Recipe'),
                                      ('Lunch', 'Lunch Recipe'),
                                      ('Dinner', 'Dinner Recipe'),
                                      ('Dessert', 'Dessert Recipe'),
                                      ('Side Dish', 'Side Dish Recipe'),
                                      ('Drink', 'Drink Recipe')],
                             default='Dinner')
    recipe_rating = RadioField('Recipe Rating', validators=[DataRequired()],
                               choices=[('1', 'Rating 1'),
                                        ('2', 'Rating 2'),
                                        ('3', 'Rating 3'),
                                        ('4', 'Rating 4'),
                                        ('5', 'Rating 5'),
                                        ('6', 'Rating 6'),
                                        ('7', 'Rating 7'),
                                        ('8', 'Rating 8'),
                                        ('9', 'Rating 9'),
                                        ('10', 'Rating 10')],
                               default='5')
    recipe_image = FileField('Recipe Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    recipe_ingredients = PageDownField('Recipe Ingredients', validators=[DataRequired()], render_kw={"rows": 12, "cols": 100})
    recipe_steps = PageDownField('Recipe Steps', validators=[DataRequired()], render_kw={"rows": 12, "cols": 100})
    recipe_inspiration = StringField('Recipe Inspiration', validators=[DataRequired()])


class EditRecipeForm(Form):
    recipe_title = StringField('Recipe Title', validators=[])
    recipe_description = StringField('Recipe Description', validators=[])
    recipe_public = BooleanField('Public Recipe', default="")
    recipe_dairy_free = BooleanField('Dairy-Free Recipe', default="")
    recipe_soy_free = BooleanField('Soy-Free Recipe', default="")
    recipe_type = RadioField('Recipe Type', validators=[],
                             choices=[('Breakfast', 'Breakfast Recipe'),
                                      ('Lunch', 'Lunch Recipe'),
                                      ('Dinner', 'Dinner Recipe'),
                                      ('Dessert', 'Dessert Recipe'),
                                      ('Side Dish', 'Side Dish Recipe'),
                                      ('Drink', 'Drink Recipe')],
                             default='Dinner')
    recipe_rating = RadioField('Recipe Rating', validators=[DataRequired()],
                               choices=[('1', 'Rating 1'),
                                        ('2', 'Rating 2'),
                                        ('3', 'Rating 3'),
                                        ('4', 'Rating 4'),
                                        ('5', 'Rating 5'),
                                        ('6', 'Rating 6'),
                                        ('7', 'Rating 7'),
                                        ('8', 'Rating 8'),
                                        ('9', 'Rating 9'),
                                        ('10', 'Rating 10')],
                               default='5')
    recipe_image = FileField('Recipe Image', validators=[FileAllowed(images, 'Images only!')])
    recipe_ingredients = PageDownField('Recipe Ingredients', validators=[], render_kw={"rows": 12, "cols": 100})
    recipe_steps = PageDownField('Recipe Steps', validators=[], render_kw={"rows": 12, "cols": 100})
    recipe_inspiration = StringField('Recipe Inspiration', validators=[DataRequired()])
