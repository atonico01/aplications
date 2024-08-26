from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()# en esta instancia le decimo que db = sqlalchemy

def create_app():
    
    app = Flask(__name__)
    
    #Configuracion del Proyecto
    
    
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"
    )
    
    db.init_app(app)#aqui inicializamos la conexion a la base de datos
    
    #Registrar Blueprint
    from . import todo
    app.register_blueprint(todo.bp)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    with app.app_context():
        db.create_all()# aqui estamos haciendo que todo los modelos de la
        #base de datos migren aqui(los que no hayan hecho)
    
    return app