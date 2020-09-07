from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from shorturl import WEBSITE_DOMAIN

def validate_URL(form, field):
    """
    Validates the provided URL against a few criterias:
        1. 4 <= URL size <= 3000
        2. Doesn't contain spaces
        3. Contain the correct amount of dots, at least 2
        4. URL starts with a ., regardless with or without the https:// scheme prefix
        5. URL starts with a /, regardless with or without the https:// scheme prefix
        6. URL ends with a .
        7. URL same as the WEBSITE_DOMAIN
    """

    if len(field.data) < 4 or len(field.data) > 3000:
        # URL isn't the right size, stop chain
        # * We don't have to raise an another ValidationError, because we would duplicate the error message
        return

    if ' ' in field.data:
        raise ValidationError(message='Invalid URL')

    if field.data.count('.') < 1:
        raise ValidationError(message='Invalid URL')

    if field.data.lower().startswith('http://.') or field.data.lower().startswith('https://.') or field.data.lower().startswith('.'):
        raise ValidationError(message='Invalid URL')

    if field.data.lower().startswith('http:///') or field.data.lower().startswith('https:///') or field.data.lower().startswith('/'):
        raise ValidationError(message='Invalid URL')

    if field.data.lower().endswith('.'):
        raise ValidationError(message='Invalid URL')

    if WEBSITE_DOMAIN in field.data.lower():
        raise ValidationError(message='Invalid URL')
        

class URLForm(FlaskForm):
    url = StringField(validators=[DataRequired(), Length(min=4, max=3000, message='The provided URL\'s size isn\'t correct'), validate_URL])
    submit = SubmitField('Shorten this URL')