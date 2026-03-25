from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired,FileSize,FileAllowed
from wtforms import PasswordField, SubmitField, SelectField, StringField
from wtforms.validators import DataRequired



class UploadForm(FlaskForm):
    file_field = FileField(
        'Upload File', validators=[
            FileRequired(),
            FileAllowed(['csv', 'xlsx'], message='CSV and Excel files only!'),
            FileSize(1024**2,message='Your file is too big.')
            ]
            )
    destination = SelectField('Select Destination Dataset',validators=[
    DataRequired()
    ],
    choices=[
    ('activities', 'Activities'),
    ('organisations', 'Organisations'),
    ('meetings', 'Meetings'),
]
    )
    submit = SubmitField('Upload')
    
class TestForm(FlaskForm):
    file_field = FileField('Upload File',validators=[FileRequired(),FileAllowed(['csv', 'xlsx'], message='CSV and Excel files only!'),FileSize(1024**2,message='Your file is too big.')])
    test_field = SelectField('Select Option', choices=[('option1','Option 1'),('option2','Option 2')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = SelectField('Remember Me', choices=[('yes','Yes'),('no','No')])
    submit = SubmitField('Login')