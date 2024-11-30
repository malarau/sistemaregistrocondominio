from flask import Blueprint, request, jsonify
from app.config.config import db_session
from app.models.models import Departamento
from sqlalchemy.exc import IntegrityError

departamento_bp = Blueprint('departamento', __name__, url_prefix='/departamentos')

@departamento_bp.route('/listar', methods=['GET'])
def listar_departamentos():
    # Listar departamentos (6)
    try:
        departamentos = db_session.query(Departamento).all()
        return jsonify([{
            'codigo_departamento': d.codigo_departamento, 
            'numero_estacionamiento': d.numero_estacionamiento
        } for d in departamentos]), 200
    finally:
        db_session.close()

@departamento_bp.route('/nuevo', methods=['POST'])
def crear_departamento():
    # Crear nuevo departamento (7)
    data = request.json
    nuevo_departamento = Departamento(
        codigo_departamento=data.get('codigo_departamento'),
        numero_estacionamiento=data.get('numero_estacionamiento')
    )
    try:
        db_session.add(nuevo_departamento)
        db_session.commit()
        return jsonify({'mensaje': 'Departamento creado exitosamente'}), 201
    except IntegrityError:
        db_session.rollback()
        return jsonify({'mensaje': 'Error: Código de departamento ya existe'}), 400
    finally:
        db_session.close()

@departamento_bp.route('/editar/<codigo_departamento>', methods=['PUT'])
def editar_departamento(codigo_departamento):
    # Editar departamento existente
    data = request.json
    try:
        departamento = db_session.query(Departamento).filter_by(codigo_departamento=codigo_departamento).first()
        if not departamento:
            return jsonify({'mensaje': 'Departamento no encontrado'}), 404

        if data.get('numero_estacionamiento') is not None:
            departamento.numero_estacionamiento = data.get('numero_estacionamiento')

        db_session.commit()
        return jsonify({'mensaje': 'Departamento actualizado exitosamente'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al actualizar: {str(e)}'}), 400
    finally:
        db_session.close()

@departamento_bp.route('/eliminar/<codigo_departamento>', methods=['DELETE'])
def eliminar_departamento(codigo_departamento):
    # Eliminar departamento
    try:
        departamento = db_session.query(Departamento).filter_by(codigo_departamento=codigo_departamento).first()
        if not departamento:
            return jsonify({'mensaje': 'Departamento no encontrado'}), 404

        db_session.delete(departamento)
        db_session.commit()
        return jsonify({'mensaje': 'Departamento eliminado exitosamente'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al eliminar: {str(e)}'}), 400
    finally:
        db_session.close()
