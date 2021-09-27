from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,BooleanField,SubmitField
from wtforms.validators import Required
from ..models import User

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title of post',validators = [Required()])
    content = TextAreaField('Content of blog',validators = [Required()])
    submit = SubmitField('Post')

class UpdatePost(FlaskForm):
    title = StringField('New Title',validators=[Required()])
    content = TextAreaField('New content',validators=[Required()])
    submit = SubmitField('Post')