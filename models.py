from todor import db

#importamos db que es casi una clase

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    # contruimos primer modelo, id es una db.column, primary_key
    #username es otra db.column, es unico, maximo 20 caracteres, no puede ser nulo
    #password es otra db.column. no puede ser falsa
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    #definimos un contructor de nuestro modelo User(usuario)
    # a continuacion definimos una funcion que lo presente y
    # nos lo retorne
    
    def __repr__(self):
        return f'<User: {self.username} >'
        
    
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    desc = db.Column(db.Text)
    state = db.Column(db.Boolean, default = False)
    
    def __init__(self, created_by, title, desc, state = False ):
        self.created_by = created_by
        self.title = title
        self.desc = desc
        self.state = state
        
        
    def __repr__(self):
        return f'<Todo: {self.title} >'
    # definimos la clase Todo en db.model. id es una columna ,integer y primary key     
    #created by es otra columna, y nos da el autor gracias a la clase Foreingkey
    # que la busca en la clase User de la otra tabla de usuario, es un integer
    # y es el user.id(la clase User al traerla de otra tabla viene en minuscula, user)
    # una descripcion de tarea, pueden ser muchas. y el state que por default sera
    # siempre falso, hasta que sea completado. el valor sera booleano                