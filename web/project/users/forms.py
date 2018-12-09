# project/users/forms.py


from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])


class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])


class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])


class NewScreening(Form):
    shoulder_rotation = RadioField('Shoulder Rotation', choices=[("Y", "Y"), ("N", "N"),("L", "L"), ("R", "R")])
    shoulder_flexion = RadioField('Shoulder Flexion', choices=[("Y", "Y"), ("N", "N"),("L", "L"), ("R", "R")])
    ankle_mobility = RadioField('Ankle Mobility', choices=[("Y", "Y"), ("N", "N"),("L", "L"), ("R", "R")])
    supine_squat = RadioField('Supine Squat', choices=[("Y", "Y"), ("N", "N")])
    leg_raise = RadioField('Leg Raise', choices=[("Y", "Y"), ("N", "N"),("L", "L"), ("R", "R")])
    overhead_squat = RadioField('Overhead Squat', choices=[("Y", "Y"), ("N", "N")])
    arms_extended_squat = RadioField('Arms Extended Squat', choices=[("Y", "Y"), ("N", "N")])
    foot_collapse = RadioField('Foot Collapse', choices=[("Y", "Y"), ("N", "N"),("L", "L"), ("R", "R")])