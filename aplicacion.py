import os 
import hashlib
from datetime import datetime

from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user,login_required

from flask_moment import Moment

from forms import (
    LoginForm, RegisterUserForm,
    EditProfileForm, PostForm
    )
from utils.utils import Permisions
from utils.permissions import permission_required



app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

login_manager= LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    from models.user import User
    return User.query.get(int(id))    

login_manager.login_view ='login'

@app.route('/', methods=['GET','POST'])
def index():    
    # if current_user.username != 'Guest':        
    #     print(current_user.role)    
                
    from models.post import Post
    form = PostForm()
    if request.method=='POST':
        if current_user.can(Permisions.WRITE) and form.validate_on_submit():
            print(current_user._get_current_object())
            print(current_user._get_current_object().id)
            post = Post(
                body=form.body.data,
                timestamp=datetime.utcnow(),
                user_id = current_user._get_current_object().id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template(
            'index.html',
            form=form,
            posts=posts,
            WRITE = Permisions.WRITE,
            ADMIN = Permisions.ADMIN
        )


db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)


@app.route('/dashboard')
@login_required
def dashboard_view():
    return render_template('dashboard.html', data=[])


from models.user import User

@app.route('/register', methods =['GET','POST'])
def register():
    form = RegisterUserForm()
    if request.method =='POST' and form.validate_on_submit():        
        new_user = User(username=form.username.data, email=form.email.data)        
        new_user.set_password(form.password_hash.data)      
        new_user.role_id=1                  
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        print('Algo ha ocurrido')
        return render_template('auth/register.html', form= form)

    return render_template('auth/register.html', form= form)


@app.route('/login', methods=['GET', 'POST'])
def login():  
    print('what1')  
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()   
    if request.method == 'POST' and form.validate_on_submit():        
        user = User.query.filter_by(username=form.username.data).first()        
        if user is None or not user.check_password(form.password_hash.data):
            flash('Usuario o contraseña son incorrectos')
            return redirect(url_for('login'))
        print('Logeado con exito csmre')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('auth/login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    print('Has cerrado session')
    return redirect(url_for('index'))


#USER VIEWS
@app.route('/usuario/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('auth/user_profile.html', user=user)

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    
    if request.method=='POST' and  form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Tu perfil se actualizó correctamente.')
        return redirect(url_for('.user', username=current_user.username))

    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('auth/edit_profile.html', form=form)

# @app.route('/create_user')


#Ruta para ingresar un usuario x defecto
@app.route('/insert')
def insert():
    u = User(username="jesusu", email="jesus@gmail.com")
    u.set_password("radamantys")
    db.session.add(u)
    db.session.commit()
    return "UsuarioAdmin insertado"


##EDIT POST
@app.route('/post/edit-post/<int:id>', methods=['GET','POST'])
def edit_post(id):    
    from models.post import Post
    form = PostForm()    
    post = Post.query.filter_by(id=id).first()
    if request.method == 'POST' and form.validate_on_submit():
        if post:
            post.body = form.body.data
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('No existe este post.')
            return redirect(url_for('index'))
    form.body.data = post.body 
    return render_template('post/edit_post.html', form=form)


def gravatar(email="hola@gmail.com", size=100, default="identicon", rating="x"):
    url = "https://secure.gravatar.com/avatar"
    hash = hashlib.md5(email.encode("utf-8")).hexdigest()
    return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
        url=url, hash=hash, size=size, default=default, rating=rating
    )
    
from forms import GravatarForm
@app.route("/gravatar", methods=['GET', 'POST'])
def dibujar():
    avt = gravatar(size=256)
    form  = GravatarForm()
    if request.method == "POST" and form.validate_on_submit():
        print(form.data)
        avt = gravatar(
            email= form.email.data,
            size=form.size.data,
            default=form.default.data
            )
        return render_template('avatar.html',avatar=avt, form=form)
    return render_template("avatar.html", avatar=avt, form=form)


# RUTAS DE ADMINISTRADOR
@app.route('/admin')
def dashboard_admin():
    return render_template('admin/admin_dashboard.html')

@app.route('/admin/user_list', methods=['GET'])
def user_list_admin():
    usuarios = User.query.all()

    return render_template('admin/user_list.html', usuarios = usuarios)

@app.route('/admin/delete_user/<int:id>', methods=['GET','POST','DELETE'])
@permission_required(Permisions.ADMIN)
def delete_user(id):
    print(request.data)
    usuario = User.query.filter_by(id = id).first()
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        print('usuario eliminado!')
        return redirect(url_for('user_list_admin'))
    print('Ha ocurrido un error')
    return redirect(url_for('user_list_admin'))

