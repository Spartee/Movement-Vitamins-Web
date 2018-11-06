from project import db, bcrypt, app, images
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from datetime import datetime
from markdown import markdown
from flask import url_for
import bleach
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# Allowable HTML tags
allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'p']


class ValidationError(ValueError):
    """Class for handling validation errors during
       import of movement screening data via API
    """
    pass


class Vitamins(db.Model):

    """Movment Screening Data"""
    __tablename__ = "vitamins"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    shoulder_rotation = db.Column(db.Boolean, nullable=True)
    shoulder_flextion = db.Column(db.Boolean, nullable=True)
    ankle_mobility = db.Column(db.Boolean, nullable=True)
    supine_squat = db.Column(db.Boolean, nullable=True)
    leg_raise = db.Column(db.Boolean, nullable=True)
    overhead_squat = db.Column(db.Boolean, nullable=True)
    arms_extended_squat = db.Column(db.Boolean, nullable=True)
    foot_collapse = db.Column(db.Boolean, nullable=True)

    def __init__(self, user_id, shoulder_flextion, shoulder_rotation, ankle_mobility, supine_squat,
                 leg_raise, overhead_squat, arms_extended_squat, foot_collapse):
        self.user_id = user_id
        self.shoulder_flextion = shoulder_flextion
        self.shoulder_rotation = shoulder_rotation
        self.ankle_mobility = ankle_mobility
        self.supine_squat = supine_squat
        self.leg_raise = leg_raise
        self.overhead_squat = overhead_squat
        self.arms_extended_squat = arms_extended_squat
        self.foot_collapse = foot_collapse


    def __repr__(self):
        return '<id: {}, user_id: {}>'.format(self.id, self.user_id)

    def get_url(self):
        return url_for('recipes_api.api1_2_get_recipe', recipe_id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'shoulder_rotation': self.shoulder_rotation,
            'shoulder_flextion': self.shoulder_flextion,
            'ankle_mobility': self.ankle_mobility,
            'supine_squat': self.supine_squat,
            'leg_raise': self.leg_raise,
            'overhead_squat': self.overhead_squat,
            'arms_extended_squat': self.arms_extended_squat,
            'foot_collapse': self.foot_collapse,
            'user_id': self.user_id
        }

    def import_data(self, request):
        """Import the data for this users vitamins"""
        try:
            json_data = request.get_json()
            self.shoulder_rotation = json_data['shoulder_rotation']
            self.shoulder_flextion = json_data['shoulder_flextion']
            self.ankle_mobility = json_data['ankle_mobility']
            self.foot_collapse = json_data['foot_collapse']
            self.arms_extended_squat = json_data['arms_overhead_squat']
            self.overhead_squat = json_data['overhead_squat']
            self.leg_raise = json_data['leg_raise']
            self.supine_squat = json_data['supine_squat']
        except KeyError as e:
            raise ValidationError('Invalid recipe: missing ' + e.args[0])
        return self


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, default='user')
    screen_data = db.relationship('vitamins', backref='user', lazy='dynamic')

    def __init__(self, email, plaintext_password, email_confirmation_sent_on=None, role='user'):
        self.email = email
        self.password = plaintext_password
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
        self.role = role

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User {}>'.format(self.email)

