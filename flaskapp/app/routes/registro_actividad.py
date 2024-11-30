from flask import Blueprint, request, jsonify
from app.config.config import db_session
from app.models.models import RegistroEntrada, Departamento
from datetime import datetime

registro_actividad_bp = Blueprint('registro_actividad', __name__, url_prefix='/registro-actividad')

@registro_actividad_bp.route('/ingreso', methods=['POST'])
def registrar_ingreso():
    # Registrar actividad de ingreso (18)
    data = request.json
    try:
        # Verificar si el departamento existe
        departamento = db_session.query(Departamento).filter_by(codigo_departamento=data.get('departamento_id')).first()
        if not departamento:
            return jsonify({'mensaje': 'Departamento no encontrado'}), 404

        nuevo_registro = RegistroEntrada(
            patente=data.get('patente'),
            nombre_completo=data.get('nombre_completo'),
            rut=data.get('rut'),
            departamento_id=data.get('departamento_id'),
            es_visita=data.get('es_visita', False),
            fecha_ingreso=datetime.now()
        )
        
        db_session.add(nuevo_registro)
        db_session.commit()
        return jsonify({'mensaje': 'Ingreso registrado exitosamente'}), 201
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al registrar ingreso: {str(e)}'}), 400
    finally:
        db_session.close()

@registro_actividad_bp.route('/salida/<int:registro_id>', methods=['PUT'])
def registrar_salida(registro_id):
    # Registrar actividad de salida (19)
    try:
        registro = db_session.query(RegistroEntrada).filter_by(id=registro_id).first()
        if not registro:
            return jsonify({'mensaje': 'Registro de entrada no encontrado'}), 404
        
        registro.fecha_salida = datetime.now()
        
        db_session.commit()
        return jsonify({'mensaje': 'Salida registrada exitosamente'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al registrar salida: {str(e)}'}), 400
    finally:
        db_session.close()

@registro_actividad_bp.route('/listar', methods=['GET'])
def listar_registros_entrada():
    # Listar registros de actividad de ingreso (20)
    try:
        registros = db_session.query(RegistroEntrada).all()
        return jsonify([{
            'id': r.id,
            'patente': r.patente, 
            'nombre_completo': r.nombre_completo,
            'rut': r.rut,
            'departamento': r.departamento.codigo_departamento if r.departamento else None,
            'es_visita': r.es_visita,
            'fecha_ingreso': r.fecha_ingreso.isoformat() if r.fecha_ingreso else None,
            'fecha_salida': r.fecha_salida.isoformat() if r.fecha_salida else None
        } for r in registros]), 200
    finally:
        db_session.close()