from flask_wtf import FlaskForm
from  wtforms import  StringField ,PasswordField ,BooleanField ,SubmitField
from wtforms.validators import   DataRequired, Email,EqualTo

class LoginForm (FlaskForm):
    username = StringField ('Utilisateur ', validators= [DataRequired()])
    password = PasswordField('Mot de passe ', validators=[DataRequired()])
    remeber_me = BooleanField('Se rappeler de moi ')
    submit = SubmitField ('Me connecter')

class InscriptionForm (FlaskForm):
    username = StringField ('Utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    email =  StringField ('Mail', validators=[DataRequired(), Email()])
    submit = SubmitField ('Inscription ')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Envoyer ')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField('Retaper votre mot de passe', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reinitialiser le mot de passe ')