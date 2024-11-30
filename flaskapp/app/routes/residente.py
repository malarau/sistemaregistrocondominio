from flask import Blueprint, request, jsonify
from app.config.config import db_session
from app.models.models import Residente, Departamento
from sqlalchemy.exc import IntegrityError

residente_bp = Blueprint('residente', __name__, url_prefix='/residentes')

@residente_bp.route('/listar', methods=['GET'])
def listar_residentes():
    # Listar Residentes (10)
    try:
        residentes = db_session.query(Residente).all()
        return jsonify([{
            'rut': r.rut, 
            'nombre_completo': r.nombre_completo,
            'departamento': r.departamento.codigo_departamento if r.departamento else None
        } for r in residentes]), 200
    finally:
        db_session.close()

@residente_bp.route('/nuevo', methods=['POST'])
def crear_residente():
    # Crear nuevo residente (11)
    data = request.json
    try:
        # Verificar si el departamento existe
        departamento = db_session.query(Departamento).filter_by(codigo_departamento=data.get('departamento_id')).first()
        if not departamento:
            return jsonify({'mensaje': 'Departamento no encontrado'}), 404

        nuevo_residente = Residente(
            rut=data.get('rut'),
            nombre_completo=data.get('nombre_completo'),
            departamento_id=data.get('departamento_id')
        )
        
        db_session.add(nuevo_residente)
        db_session.commit()
        return jsonify({'mensaje': 'Residente creado exitosamente'}), 201
    except IntegrityError:
        db_session.rollback()
        return jsonify({'mensaje': 'Error: RUT de residente ya existe'}), 400
    finally:
        db_session.close()

@residente_bp.route('/editar/<rut>', methods=['PUT'])
def editar_residente(rut):
    # Editar residente (12)
    data = request.json
    try:
        residente = db_session.query(Residente).filter_by(rut=rut).first()
        if not residente:
            return jsonify({'mensaje': 'Residente no encontrado'}), 404
        
        if data.get('nombre_completo'):
            residente.nombre_completo = data.get('nombre_completo')
        
        if data.get('departamento_id'):
            # Verificar si el departamento existe
            departamento = db_session.query(Departamento).filter_by(codigo_departamento=data.get('departamento_id')).first()
            if not departamento:
                return jsonify({'mensaje': 'Departamento no encontrado'}), 404
            residente.departamento_id = data.get('departamento_id')
        
        db_session.commit()
        return jsonify({'mensaje': 'Residente actualizado exitosamente'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al actualizar: {str(e)}'}), 400
    finally:
        db_session.close()

@residente_bp.route('/eliminar/<rut>', methods=['DELETE'])
def eliminar_residente(rut):
    # Eliminar residente (13)
    try:
        residente = db_session.query(Residente).filter_by(rut=rut).first()
        if not residente:
            return jsonify({'mensaje': 'Residente no encontrado'}), 404
        
        db_session.delete(residente)
        db_session.commit()
        return jsonify({'mensaje': 'Residente eliminado exitosamente'}), 200
    except Exception as e:
        db_session.rollback()
        return jsonify({'mensaje': f'Error al eliminar: {str(e)}'}), 400
    finally:
        db_session.close()