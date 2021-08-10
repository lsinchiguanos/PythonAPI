# Importamos el módulo FLASK
from flask import Flask, request, jsonify
# Importando el ORM de SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from flask_cors import CORS
from datetime import datetime

# Especificacion la utilización de Flask
app=Flask(__name__)
CORS(app, resources={r"/api/*"}, origins=['*'] , supports_credentials=True)
# Datos de conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:12345@localhost:5432/bonos'
# Desactivando las notificaciones de alteración al esquema de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Estableciendo la variable que rendizará la base de datos
db=SQLAlchemy(app)

# Tabla Clientes
class Cliente(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    dni = db.Column(db.String(15), nullable=False, unique=True)
    apellido_paterno = db.Column(db.String(150), nullable=False)
    apellido_materno = db.Column(db.String(150), nullable=False)
    primer_nombre = db.Column(db.String(150), nullable=False)
    segundo_nombre = db.Column(db.String(150), default='')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # Establece el nombre de la tabla
    def __repr__(self):
        return self.name

    # Consulta de todos los registros
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # Establece busqueda por id
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    # Función de insertar
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    # Función de eliminar
    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Tabla Establecimiento
class Establecimiento(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(15), nullable=False, unique=True)
    cupo = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Tabla Calendario
class Calendario(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    anio = db.Column(db.Integer(), nullable=False)
    mes = db.Column(db.Integer(), nullable=False)
    dia = db.Column(db.Integer(), nullable=False)
    establecimiento_id = db.Column(db.Integer(), db.ForeignKey("establecimiento.id", ondelete='SET NULL'), nullable=False)
    establecimiento_fk = db.relationship('Establecimiento', foreign_keys=[establecimiento_id], backref="my_establecimiento")
    cliente_id = db.Column(db.Integer(), db.ForeignKey("cliente.id", ondelete='SET NULL'), nullable=False)
    cliente_fk = db.relationship('Cliente', foreign_keys=[cliente_id], backref="my_cita")
    renovacion = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

# Esquemas Clientes
class ClienteSchema(Schema):
    id = fields.Integer()
    dni = fields.String()
    apellido_paterno = fields.String()
    apellido_materno = fields.String()
    primer_nombre = fields.String()
    segundo_nombre = fields.String()

# Esquemas Establecimiento
class EstablecimientoSchema(Schema):
    id = fields.Integer()
    nombre = fields.String()
    cupo = fields.Integer()

# Esquemas Calendario
class CalendarioSchema(Schema):
    id = fields.Integer()
    anio = fields.Integer()
    mes = fields.Integer()
    dia = fields.Integer()
    establecimiento_id = fields.Integer()
    cliente_id = fields.Integer()
    renovacion = fields.Integer()

# Rutas Clientes
@app.route('/api/clientes', methods=['GET'])
def get_all_clientes():
    clientes = Cliente.get_all()
    serializer = ClienteSchema(many = True)
    data = serializer.dump(clientes)
    return jsonify(data)

@app.route('/api/clientes', methods=['POST'])
def create_a_cliente():
    data = request.get_json()
    new_cliente = Cliente(
        dni = data.get('dni'),
        apellido_paterno = data.get('apellido_paterno'),
        apellido_materno = data.get('apellido_materno'),
        primer_nombre = data.get('primer_nombre'),
        segundo_nombre = data.get('segundo_nombre')
    )
    new_cliente.save()
    serializer=ClienteSchema()
    data=serializer.dump(new_cliente)
    return jsonify({"message": "Registro almacenado éxitosamente"}),201

@app.route('/api/cliente/<int:id>', methods=['GET'])
def get_cliente(id):
    search_cliente = Cliente.get_by_id(id)
    serializer = ClienteSchema()
    data = serializer.dump(search_cliente)
    return jsonify(data),200

@app.route('/api/cliente/<int:id>', methods=['PUT'])
def update_cliente(id):
    up_cliente = Cliente.get_by_id(id)
    data = request.get_json()
    up_cliente.dni = data.get('dni'),
    up_cliente.apellido_paterno = data.get('apellido_paterno'),
    up_cliente.apellido_materno = data.get('apellido_materno'),
    up_cliente.primer_nombre = data.get('primer_nombre'),
    up_cliente.segundo_nombre = data.get('segundo_nombre')
    db.session.commit()
    serializer = ClienteSchema()
    b_data = serializer.dump(up_cliente)
    return jsonify(b_data),200

@app.route('/api/cliente/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    del_cliente = Cliente.get_by_id(id)
    del_cliente.delete()
    return jsonify({"message": "Registro eliminado éxitosamente"}), 204

# Rutas Establecimientos
@app.route('/api/establecimientos', methods=['GET'])
def get_all_establecimientos():
    establecimientos = Establecimiento.get_all()
    serializer = EstablecimientoSchema(many = True)
    data = serializer.dump(establecimientos)
    return jsonify(data)

@app.route('/api/establecimientos', methods=['POST'])
def create_a_establecimiento():
    data = request.get_json()
    new_establecimiento = Establecimiento(
        nombre = data.get('nombre'),
        cupo = data.get('cupo')
    )
    new_establecimiento.save()
    serializer=EstablecimientoSchema()
    data=serializer.dump(new_establecimiento)
    return jsonify({"message": "Registro almacenado éxitosamente"}),201

@app.route('/api/establecimiento/<int:id>', methods=['GET'])
def get_establecimiento(id):
    search_establecimiento = Establecimiento.get_by_id(id)
    serializer = EstablecimientoSchema()
    data = serializer.dump(search_establecimiento)
    return jsonify(data),200

@app.route('/api/establecimiento/<int:id>', methods=['PUT'])
def update_establecimiento(id):
    up_establecimiento = Establecimiento.get_by_id(id)
    data = request.get_json()
    up_establecimiento.nombre = data.get('nombre'),
    up_establecimiento.cupo = data.get('cupo')
    db.session.commit()
    serializer = EstablecimientoSchema()
    b_data = serializer.dump(up_establecimiento)
    return jsonify(b_data),200

@app.route('/api/establecimiento/<int:id>', methods=['DELETE'])
def delete_establecimiento(id):
    del_establecimiento = Establecimiento.get_by_id(id)
    del_establecimiento.delete()
    return jsonify({"message": "Registro eliminado éxitosamente"}), 204

# Rutas Calendario
@app.route('/api/calendarios', methods=['GET'])
def get_all_calendarios():
    calendarios = Calendario.get_all()
    serializer = CalendarioSchema(many = True)
    data = serializer.dump(calendarios)
    return jsonify(data)

@app.route('/api/calendarios', methods=['POST'])
def create_a_calendario():
    data = request.get_json()
    new_calendario = Calendario(
        anio = data.get('anio'),
        mes = data.get('mes'),
        dia = data.get('dia'),
        establecimiento_id = data.get('establecimiento_id'),
        cliente_id = data.get('cliente_id'),
        renovacion = data.get('renovacion')
    )
    new_calendario.save()
    serializer=CalendarioSchema()
    data=serializer.dump(new_calendario)
    return jsonify({"message": "Registro almacenado éxitosamente"}),201

@app.route('/api/calendario/<int:id>', methods=['GET'])
def get_calendario(id):
    search_calendario = Calendario.get_by_id(id)
    serializer = CalendarioSchema()
    data = serializer.dump(search_calendario)
    return jsonify(data),200

@app.route('/api/calendario/<int:id>', methods=['PUT'])
def update_calendario(id):
    up_calendario = Calendario.get_by_id(id)
    data = request.get_json()
    up_calendario.anio = data.get('anio'),
    up_calendario.mes = data.get('mes'),
    up_calendario.dia = data.get('dia'),
    up_calendario.establecimiento_id = data.get('establecimiento_id'),
    up_calendario.cliente_id = data.get('cliente_id'),
    up_calendario.renovacion = data.get('renovacion')
    db.session.commit()
    serializer = CalendarioSchema()
    b_data = serializer.dump(up_calendario)
    return jsonify(b_data),200

@app.route('/api/calendario/<int:id>', methods=['DELETE'])
def delete_calendario(id):
    del_calendario = Calendario.get_by_id(id)
    del_calendario.delete()
    return jsonify({"message": "Registro eliminado éxitosamente"}), 204

# Controladores de error
@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Contenido no existente"})

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message": "Ocurrio un problema"})

if __name__ == '__main__':
    app.run(debug=True)