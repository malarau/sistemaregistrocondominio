from flask import Blueprint, request, jsonify
from app.config.config import db_session
from app.models.models import Guardia
from sqlalchemy.exc import IntegrityError

guardia_bp = Blueprint('guardia', __name__, url_prefix='/guardias')

@guardia_bp.route('/listar', methods=['GET'])
def listar_guardias():
    # Listar guardias (2)
    try:
        guardias = db_session.query(Guardia).all()
        return jsonify([{
            'rut': g.rut, 
            'nombre_completo': g.nombre_completo, 
            'estado': g.estado
        } for g in guardias]), 200
    finally:
        db_session.close()

@guardia_bp.route('/nuevo', methods=['POST'])
def nuevo_guardia():
    # Añadir nuevo guardia (3)
    data = request.json
    nuevo_guardia = Guardia(
        usuario=data.get('usuario'),
        contrasena=data.get('contrasena'),
        rut=data.get('rut'),
        nombre_completo=data.get('nombre_completo'),
        estado=data.get('estado', True)
    )
    try:
        db_session.add(nuevo_guardia)
        db_session.commit()
        return jsonify({'mensaje': 'Guardia añadido exitosamente'}), 201
    except IntegrityError:
        db_session.rollback()
        return jsonify({'mensaje': 'Error: RUT o usuario ya existe'}), 400
    finally:
        db_session.close()

@guardia_bp.route('/editar/<rut>', methods=['PUT'])
def editar_guardia(rut):
    # Editar guardia existente (4)
    data = request.json
    try:
        guardia = db_session.query(Guardia).filter_by(rut=rut).first()
        if not guardia:
            return jsonify({'mensaje': 'Guardia no encontrado'}), 404
        
        if data.get('nombre_completo'):
            guardia.nombre_completo = data.get('nombre_completo')
        if data.get('estado') is not None:
            guardia.estado = data.get('estado')
        
        db_session.commit()
        return jsonify({'mensaje': 'Guardia actualizado exitosamente'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al actualizar: {str(e)}'}), 400
    finally:
        db_session.close()

@guardia_bp.route('/eliminar/<rut>', methods=['DELETE'])
def eliminar_guardia(rut):
    # Eliminar guardia (5)
    try:
        guardia = db_session.query(Guardia).filter_by(rut=rut).first()
        if not guardia:
            return jsonify({'mensaje': 'Guardia no encontrado'}), 404
        
        db_session.delete(guardia)
        db_session.commit()
        return jsonify({'mensaje': 'Guardia eliminado exitosamente'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al eliminar: {str(e)}'}), 400
    finally:
        db_session.close()