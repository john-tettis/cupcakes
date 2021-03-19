from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DecimalField
from wtforms.validators import InputRequired, URL, Optional


class CupcakeForm(FlaskForm):
    flavor = StringField('Flavor',[InputRequired(message='Flavor is required.')])

    size = StringField('Size',[InputRequired(message='Size is required.')])

    rating = DecimalField('Rating',[InputRequired(message='Rating is required and must be a number.')], places = 2)

    image = StringField('Image',[Optional(), URL(message = 'image  ust be a valid URL.')])