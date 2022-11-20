from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField,
    SubmitField, IntegerField, SelectField,
    TextAreaField
    )
    
from wtforms.validators import DataRequired, Length


#AUTH FORMS
class LoginForm(FlaskForm):
    username = StringField('Ingrese nombre de usuario', validators=[DataRequired()])    
    password_hash = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recuerdame')
    submit =SubmitField(label='Iniciar session')

class RegisterUserForm(FlaskForm):
    username = StringField('Ingrese nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Contraseña', validators=[DataRequired()])
    submit =SubmitField(label='Registrar usuario')


class EditProfileForm(FlaskForm):
    name = StringField('Nombre real', validators=[Length(0, 64)])
    location = StringField('Locación', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mi')
    submit = SubmitField('Actualizar')


#POST 
class PostForm(FlaskForm):
    body = TextAreaField("¿En que estas pensando?", validators=[DataRequired()])
    submit = SubmitField('Publicar')


class GravatarForm(FlaskForm):
    email = StringField('Email')
    size = IntegerField('Tamaño ? ')
    default = SelectField('default ? ',
                choices = [
                    ('404', '404'),
                    ('mp', 'mp'),
                    ('identicon', 'identicon'),
                    ('monsterid', 'monsterid'),
                    ('wavatar', 'wavatar'),
                    ('retro', 'retro'),
                    ('robohash', 'robohash'),
                    ('blank', 'blank'),                    
                    ]
                )
    rating = SelectField('indicate if an image is appropriate for a certain audience',
                choices =[
                    ('g', 'g'),
                    ('pg', 'pg'),
                    ('r', 'r'),
                    ('x', 'x'),
                    ]
                )
    submit = SubmitField(label='Generar Avatar')