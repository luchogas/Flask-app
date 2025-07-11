from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config       
from models import db, Trabajador, RegistroHorario
from datetime import datetime, date

app = Flask(__name__)          
app.config.from_object(Config)  

db.init_app(app)                

@app.route("/")
def index():
    return "¡app flask funcionando!"

@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/entrada", methods=["GET", "POST"])  #entradaa funcionalidad 1
def registrar_entrada():
    dependencias = [
        ("D01", "Edificio Central"),
        ("D02", "Talleres"),
        ("D03", "Centro Deportivo"),
    ]

    if request.method == "POST":
        legajo = request.form["legajo"].strip()
        dni = request.form["dni"].strip()
        dependencia = request.form["dependencia"]

        trabajador = Trabajador.query.filter_by(legajo=legajo).first()
        if not trabajador or trabajador.dni[-4:] != dni:
            flash("Legajo o DNI incorrecto.")
            return redirect(url_for("registrar_entrada"))

        hoy = date.today()
        existe = RegistroHorario.query.filter_by(idtrabajador=trabajador.id, fecha=hoy, dependencia=dependencia).first()

        if existe:
            flash("Ya registraste una entrada hoy en esta dependencia.")
            return redirect(url_for("registrar_entrada"))

        nueva_entrada = RegistroHorario(
            fecha=hoy,
            horaentrada=datetime.now().time(),
            horasalida=None,
            dependencia=dependencia,
            idtrabajador=trabajador.id
        )
        db.session.add(nueva_entrada)
        db.session.commit()
        flash("Entrada registrada correctamente.")
        return redirect(url_for("registrar_entrada"))

    return render_template("entrada.html", dependencias=dependencias)


@app.route("/salida", methods=["GET", "POST"]) #salidaa funcionalidad 2
def registrar_salida():
    dependencias = [
        ("D01", "Edificio Central"),
        ("D02", "Talleres"),
        ("D03", "Centro Deportivo"),
    ]

    if request.method == "POST":
        legajo = request.form["legajo"].strip()
        dni = request.form["dni"].strip()
        dependencia = request.form["dependencia"]

        trabajador = Trabajador.query.filter_by(legajo=legajo).first()
        if not trabajador or trabajador.dni[-4:] != dni:
            flash("Legajo o DNI incorrecto.")
            return redirect(url_for("registrar_salida"))

        hoy = date.today()
        registro = RegistroHorario.query.filter_by(idtrabajador=trabajador.id, fecha=hoy, dependencia=dependencia).first()

        if not registro:
            flash("No existe entrada registrada para hoy en esta dependencia.")
            return redirect(url_for("registrar_salida"))
        if registro.horasalida:
            flash("Ya registraste una salida hoy.")
            return redirect(url_for("registrar_salida"))

        registro.horasalida = datetime.now().time()
        db.session.commit()
        nombre_dependencia = dict(dependencias).get(dependencia, dependencia)
        flash(f"Salida registrada correctamente en {nombre_dependencia}.")
        return redirect(url_for("registrar_salida"))

    return render_template("salida.html", dependencias=dependencias)

@app.route("/consulta", methods=["GET", "POST"])#consultaa funcionalidad 3
def consultar_registros():
    registros = None
    dependencias_dict = {
        "D01": "Edificio Central",
        "D02": "Talleres",
        "D03": "Centro Deportivo",
    }
    if request.method == "POST":
        legajo = request.form["legajo"].strip()
        dni = request.form["dni"].strip()
        fecha_ini = request.form["fecha_ini"]
        fecha_fin = request.form["fecha_fin"]

        trabajador = Trabajador.query.filter_by(legajo=legajo).first()
        if not trabajador or trabajador.dni[-4:] != dni:
            flash("Legajo o DNI incorrecto.")
            return render_template("consulta.html", registros=registros, dependencias_dict=dependencias_dict)

        # Paso las fechas a formato date
        try:
            fecha_ini = datetime.strptime(fecha_ini, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            flash("Debes ingresar fechas válidas.")
            return render_template("consulta.html", registros=registros, dependencias_dict=dependencias_dict)

        registros = (
            RegistroHorario.query
            .filter(
                RegistroHorario.idtrabajador == trabajador.id,
                RegistroHorario.fecha >= fecha_ini,
                RegistroHorario.fecha <= fecha_fin
            ).order_by(RegistroHorario.fecha).all()
        )
        if not registros:
            flash("No se encontraron registros en el periodo indicado.")

    return render_template("consulta.html", registros=registros, dependencias_dict=dependencias_dict)


if __name__ == "__main__":
    app.run(debug=True)