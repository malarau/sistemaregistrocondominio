from flask import Blueprint, request, jsonify
from app.config.config import db_session
from app.models.models import Usuario

acceso_bp = Blueprint('acceso', __name__)

@acceso_bp.route('/login', methods=['POST'])
def login():
    # Control de acceso al sistema (1)
    data = request.json
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')
    
    try:
        user = db_session.query(Usuario).filter_by(usuario=usuario, contrasena=contrasena).first()
        if user:
            return jsonify({
                'mensaje': 'Inicio de sesión exitoso', 
                'tipo_usuario': user.tipo
            }), 200
        return jsonify({'mensaje': 'Credenciales incorrectas'}), 401
    finally:
        db_session.close()