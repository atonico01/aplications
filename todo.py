from flask import Blueprint, render_template, request, redirect, url_for, g



from todor.auth import login_required

from .models import Todo, User

from todor import db



# ya contruido el template le damos funcion, hacemos 
# algunas importaciones
bp = Blueprint('todo', __name__, url_prefix='/todo')

@bp.route('/list')
@login_required
def index():
    todos = Todo.query.all() # creamos una variable que recuperará
    # todos los todos. Habra que recorrer el codigo con un bucle for
    return render_template('todo/index.html', todos = todos)

@bp.route('/create', methods =('GET' , 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        todo = Todo(g.user.id, title, desc)
        
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo.index'))
    return render_template('todo/create.html')

#creamos la parte de editar o listar en todo.property

def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo

@bp.route('/update/<int:id>', methods=('GET' , 'POST'))
@login_required
def update(id):
    
    todo = get_todo(id)# obtenemos todos los todo
    
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.state = True if request.form.get('state') == 'on' else False
        # recuperamos los todo arriba, y con el condicional podemos modificar
        # los valores recuperados del formulario. En el todo.state, le indi_
        # camos que sera True si request.form.get('state') == 'on' en el template update,
        # o sera False
        
        db.session.commit()
        return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo = todo)

#Eliminar tareas

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))
    