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
    shoulder_rotation = RadioField('Shoulder Rotation', choices=[("Y", "Yes"), ("N", "No"),("L", "Left"), ("R", "Right")], default='N')
    shoulder_flexion = RadioField('Shoulder Flexion', choices=[("Y", "Yes"), ("N", "No"),("L", "Left"), ("R", "Right")], default='N')
    ankle_mobility = RadioField('Ankle Mobility', choices=[("Y", "Yes"), ("N", "No"),("L", "Left"), ("R", "Right")], default='N')
    supine_squat = RadioField('Supine Squat', choices=[("Y", "Yes"), ("N", "No")], default='N')
    leg_raise = RadioField('Leg Raise', choices=[("Y", "Yes"), ("N", "No"),("L", "Left"), ("R", "Right")], default='N')
    overhead_squat = RadioField('Overhead Squat', choices=[("Y", "Yes"), ("N", "No")], default='N')
    arms_extended_squat = RadioField('Arms Extended Squat', choices=[("Y", "Yes"), ("N", "No")], default='N')
    foot_collapse = RadioField('Foot Collapse', choices=[("Y", "Yes"), ("N", "No"),("L", "Left"), ("R", "Right")], default='Y')