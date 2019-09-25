from webapp import app,db
from flask import render_template,flash,redirect,escape,url_for,request
from mysql.connector import connection
from webapp.auth.forms import LoginForm, InscriptionForm,ResetPasswordRequestForm,ResetPasswordForm
from flask_login import current_user,login_user,logout_user,login_required
from webapp.models import User
from werkzeug.urls import url_parse
from webapp.auth.email import send_password_reset_email


@app.route ("/")
@app.route ("/index",methods=['GET','POST'])
@login_required
def index():
    user = {'username' : 'BOBO'}

    postes = [
        {
            'auteur' :{'username': 'oussama'},
             'body': 'pas de sypas le git '
        },
        {
            'auteur': {'username': 'Paul'},
            'body': 'Il suffit de configurer '

        },
        {
            'auteur': {'username': 'Mohemed'},
            'body': 'gls ledr '

        }
    ]


    return render_template('index.html',title="Page d'accueil", user=user,postes=postes)
##return valider(this);"##



def bd():
    cnx= connection.MySQLConnection(user='root', password='',
                                    host='127.0.0.1', database='annuaire')
    cursor=cnx.cursor()
    data = ("Select * from personne ")
    cursor.execute(data)
    liste = cursor.fetchall()
    cnx.close()
    return  liste

@app.route ("/table")
@login_required

def table():
    resultat=bd()
    resultat=resultat*5

    return render_template('table.html',resultat=resultat)

@app.route('/inscription',methods=['GET','POST'])
@app.endpoint('inscription')
def inscription():
    if current_user.is_authenticated :
        flash('Faut se deconnecter ')
        return redirect(url_for('index'))

    form = InscriptionForm()
    print('before')
    if form.validate_on_submit():
        print('ok')
        us = User(username=form.username.data,email=form.email.data )
        us.set_password(form.password.data)
        db.session.add(us)
        db.session.commit()


        flash('Utilisateur M.'+format(us.username)+' est ajouté avec succés')
        return redirect(url_for('login'))
    #flash('Erreur')
    return  render_template('inscription.html' ,title='CONNEXION',form=form)

@app.route('/user/<username>')
def profile (username):
    return '{}\'s profile'.format(escape(username))

"""with app.test_request_context():

    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login',next='/'))
    print(url_for('profile',username='oussama'))"""

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username= form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login ou mot de passe invalide')
            return redirect(url_for('login'))
        login_user(user,remember=form.remeber_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page=url_for('index')
        return  redirect(next_page)
    return  render_template('login.html',title='CONNEXION',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset_password_request',methods=['GET','POST'])
def reset_password_request():

    if current_user.is_authenticated :
        flash('Faut se deconnecter ')
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user :
            send_password_reset_email(user)
            flash('Consultez votre mail  et suivez les instructions ')
            return redirect(url_for('login'))
    return render_template('reset_password_request.html',form=form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated :
        flash('Faut se deconnecter ')
        return redirect(url_for('index'))

    user=User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Votre mot de passe à bien été reinitialisé')
        return redirect(url_for('login'))
    return render_template( 'formulaire_reset_password.html',form=form)
