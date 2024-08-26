from flask import (Blueprint, render_template, request, url_for, redirect, flash, session, g )
    

from werkzeug.security import generate_password_hash, check_password_hash


from .models import User
from todor import db 
# importamos de models el modelo y User y tambien el objeto db desde todor

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User(username, generate_password_hash(password))
        
        error = None
        
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        
        else:
            error = f'El usuario {username} ya esta creado'
            
        flash(error)
        
    
       
    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #validar los datos
        # creamos un objeto usuario, user
        user = User.query.filter_by(username = username).first()
        
        error = None
        
        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'
            
            #si user es none(nombre incorrecto, o check_password_hash no correcto)          
        
        # Iniciar sesion
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect (url_for('todo.index'))
        flash(error)
    return render_template('auth/login.html')
# Hasta ahora hemos iniciado sesion pero, si salimos,
#o navegamos fuera no mantendra la session, para que se mantenga haremos
# lo siguiente.

@bp.before_app_request# ejecutaremos este bp antes de cada consulta
#para saber si hay sesion iniciada
def load_logged_in_user():
    user_id = session.get('user_id')#obtenemos el user_id
    
    if user_id is None:
        g.user = None
    
    else:
        g.user = User.query.get_or_404(user_id)
        
        
# cerrar sesion

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# podemos entrar a lista de tareas escribiendo la url sin
# iniciar sesion. Para evitar eso, importamos la funcion functools

import functools

def login_required(view):
    @functools.wraps(view)
    def wraped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wraped_view

# definimos una funcion que requiere haber iniciado sesion en login, en la vista
# con un decorador aplicamos la functools.wrap(view) para atrape o envuelva, los datos
# de la vista ((**kwargs)datos cualquiera). Atrapamos a g.user y si es none, nos redi-
# recciona a (url_for('auth/login')) para introducir datos de inicio sesion.
# nos retorna la vista con los datos introducidos(**kwargs).
# por ultimo nos retorna los datos a la funcion wraped_view, que nos
#demandaba los datos. AHORA IMPORTAMOS LA FUNCION A LA PAGINA todo.py