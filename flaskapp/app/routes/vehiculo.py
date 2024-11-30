from flask import Blueprint, request, jsonify
from app.config.config import db_session
from app.models.models import Vehiculo, Departamento
from sqlalchemy.exc import IntegrityError

vehiculo_bp = Blueprint('vehiculo', __name__, url_prefix='/vehiculos')

@vehiculo_bp.route('/listar', methods=['GET'])
def listar_vehiculos():
    # Listar vehículos (14)
    try:
        vehiculos = db_session.query(Vehiculo).all()
        return jsonify([{
            'patente': v.patente, 
            'departamento': v.departamento.codigo_departamento if v.departamento else None
        } for v in vehiculos]), 200
    finally:
        db_session.close()

@vehiculo_bp.route('/nuevo', methods=['POST'])
def asignar_vehiculo():
    # Asignar nuevo vehículo (15)
    data = request.json
    try:
        # Verificar si el departamento existe
        departamento = db_session.query(Departamento).filter_by(codigo_departamento=data.get('departamento_id')).first()
        if not departamento:
            return jsonify({'mensaje': 'Departamento no encontrado'}), 404

        nuevo_vehiculo = Vehiculo(
            patente=data.get('patente'),
            departamento_id=data.get('departamento_id')
        )
        
        db_session.add(nuevo_vehiculo)
        db_session.commit()
        return jsonify({'mensaje': 'Vehículo asignado exitosamente'}), 201
    except IntegrityError:
        db_session.rollback()
        return jsonify({'mensaje': 'Error: Patente de vehículo ya existe'}), 400
    finally:
        db_session.close()

@vehiculo_bp.route('/editar/<patente>', methods=['PUT'])
def editar_vehiculo(patente):
    # Editar Vehículo (16)
    data = request.json
    try:
        vehiculo = db_session.query(Vehiculo).filter_by(patente=patente).first()
        if not vehiculo:
            return jsonify({'mensaje': 'Vehículo no encontrado'}), 404
        
        if data.get('departamento_id'):
            # Verificar si el departamento existe
            departamento = db_session.query(Departamento).filter_by(codigo_departamento=data.get('departamento_id')).first()
            if not departamento:
                return jsonify({'mensaje': 'Departamento no encontrado'}), 404
            vehiculo.departamento_id = data.get('departamento_id')
        
        db_session.commit()
        return jsonify({'mensaje': 'Vehículo actualizado exitosamente'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al actualizar: {str(e)}'}), 400
    finally:
        db_session.close()

@vehiculo_bp.route('/eliminar/<patente>', methods=['DELETE'])
def eliminar_vehiculo(patente):
    # Eliminar vehículo (17)
    try:
        vehiculo = db_session.query(Vehiculo).filter_by(patente=patente).first()
        if not vehiculo:
            return jsonify({'mensaje': 'Vehículo no encontrado'}), 404
        
        db_session.delete(vehiculo)
        db_session.commit()
        return jsonify({'mensaje': 'Vehículo eliminado exitosamente'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al eliminar: {str(e)}'}), 400
    finally:
        db_session.close()