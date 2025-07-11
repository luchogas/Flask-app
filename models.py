from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Trabajador(db.Model):
    __tablename__ = 'trabajador' #nombre de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    legajo = db.Column(db.String(20), unique=True, nullable=False)
    horas = db.Column(db.Integer, nullable=False)
    funcion = db.Column(db.String(100), nullable=False)

    # Relación uno  a muchos: un trabajador puede tener muchos registros de horario
    registros = db.relationship("RegistroHorario", backref="trabajador", lazy=True)

class RegistroHorario(db.Model):
    __tablename__ = "registrohorario"
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    horaentrada = db.Column(db.Time)
    horasalida = db.Column(db.Time)
    dependencia = db.Column(db.String)
    idtrabajador = db.Column(db.Integer, db.ForeignKey("trabajador.id"))  # Relación con Trabajador