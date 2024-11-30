from flask import Flask
from app.models.models import Base, Guardia, Administrador, Residente, Vehiculo, Departamento
from app.config.config import SessionLocal, engine
# Blueprints
from app.routes.acceso import acceso_bp
from app.routes.guardia import guardia_bp
from app.routes.departamento import departamento_bp
from app.routes.residente import residente_bp
from app.routes.vehiculo import vehiculo_bp
from app.routes.registro_actividad import registro_actividad_bp
from app.routes.ping import ping_bp

def create_app():
    app = Flask(__name__)
    
    # Crear todas las tablas definidas en los modelos
    Base.metadata.create_all(bind=engine)

    # Cargar los datos iniciales
    load_initial_data()

    # Blueprints
    #
    # Acceso
    app.register_blueprint(acceso_bp)
    # Guardia
    app.register_blueprint(guardia_bp)
    # Departamento
    app.register_blueprint(departamento_bp)
    # Residente
    app.register_blueprint(residente_bp)
    # Vehículo
    app.register_blueprint(vehiculo_bp)
    # Registro de actividad
    app.register_blueprint(registro_actividad_bp)

    # Ping
    app.register_blueprint(ping_bp)
    
    return app

def load_initial_data():
    session = SessionLocal()

    try:
        # Insertar un Administrador si no existe
        if not session.query(Administrador).filter(Administrador.tipo == 'administrador').first():
            admin = Administrador(
                usuario='admin',
                contrasena='admin',  # Asegúrate de encriptar la contraseña si es necesario
                tipo='administrador'
            )
            session.add(admin)
            session.commit()

        # Insertar un Guardia si no existe
        if not session.query(Guardia).first():
            guardia = Guardia(
                usuario='guardia1',
                contrasena='guardia1',
                tipo='guardia',
                rut='12345678-9',
                nombre_completo='Guardia Uno'
            )
            session.add(guardia)
            session.commit()

        # Insertar 2 Departamentos con un Residente y un Vehículo
        if not session.query(Departamento).first():
            depto1 = Departamento(codigo_departamento="A100", numero_estacionamiento=1)
            depto2 = Departamento(codigo_departamento="A200", numero_estacionamiento=2)

            # Agregar a la sesión para que se inserten los departamentos
            session.add(depto1)
            session.add(depto2)
            #session.commit()  # Commit aquí para tener los IDs de los departamentos

            # Insertar Residentes
            residente1 = Residente(
                rut="11111111-1", nombre_completo="Residente 1", departamento_id=depto1.codigo_departamento
            )
            residente2 = Residente(
                rut="22222222-2", nombre_completo="Residente 2", departamento_id=depto2.codigo_departamento
            )
            # Insertar Vehículos
            vehiculo1 = Vehiculo(
                patente="PATENTE1", departamento_id=depto1.codigo_departamento
            )
            vehiculo2 = Vehiculo(
                patente="PATENTE2", departamento_id=depto2.codigo_departamento
            )

            session.add(residente1)
            session.add(residente2)
            session.add(vehiculo1)
            session.add(vehiculo2)
            session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error al cargar datos iniciales: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    app = create_app()
    
    # Configuraciones adicionales del servidor
    app.run(debug=True, host='0.0.0.0', port=5000)
