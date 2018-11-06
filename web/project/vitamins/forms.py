# project/vitamins/forms.py


from flask_wtf import Form
from wtforms import StringField, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_pagedown.fields import PageDownField
from project import images


class AddVitaminsForm(Form):
    """TODO: finish this form"""
    shoulder_rotation = BooleanField('Shoulder_rotation', default="")


class EditVitaminsForm(Form):
    """TODO: finish this form, should be identical to the one above"""
    shoulder_rotation = BooleanField('Shoulder_rotation', default="")
