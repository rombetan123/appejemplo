from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

# Crear la app Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '32Rr_66062626')
database_url = os.getenv('DATABASE_URL')
if not database_url:
    # Fallback local
    database_url = 'postgresql://postgres:Rr_66062626@localhost/mitienda'

# 2) Configura SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3) Fuerza SSL/TLS (ojo: necesario solo si tu URL no incluye sslmode)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'sslmode': 'require'}
}

db = SQLAlchemy(app)

# Modelos
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nom_categoria = db.Column(db.String(100), nullable=False)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_ud_usuario = db.Column(db.Integer, primary_key=True)
    nom_usuario = db.Column(db.String(50), nullable=False)
    ape_usuario = db.Column(db.String(50), nullable=False)
    pasword = db.Column(db.String(128))

# Flask-Admin
admin = Admin(app, name='Panel Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Usuario, db.session))
admin.add_view(ModelView(Categoria, db.session))
admin.add_view(ModelView(Producto, db.session))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inicio/")
def inicio():
    return render_template("index.html")

@app.route('/productos')
def productos():
    return render_template('plantilla1.html')

@app.route('/servicios')
def servicios():
    return render_template('plantilla2.html')

@app.route('/ventas')
def ventas():
    productos = Producto.query.all()
    return render_template('ventas.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)