from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    usuario = Column(String, unique=True, nullable=False)
    contrasena = Column(String, nullable=False)
    tipo = Column(String)  # Discriminador para herencia

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }

class Guardia(Usuario):
    __tablename__ = 'guardias'
    id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    rut = Column(String, unique=True, nullable=False)
    nombre_completo = Column(String, nullable=False)
    estado = Column(Boolean, default=True)

    __mapper_args__ = {
        'polymorphic_identity': 'guardia'
    }

class Administrador(Usuario):
    __tablename__ = 'administradores'
    id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    # Sin campos ni nada adicional, mal planificada la cosa.

    __mapper_args__ = {
        'polymorphic_identity': 'administrador'
    }

class Departamento(Base):
    __tablename__ = 'departamentos'

    codigo_departamento = Column(String, primary_key=True)
    numero_estacionamiento = Column(Integer, unique=True, nullable=False)
    
    # Relaciones
    residentes = relationship('Residente', back_populates='departamento')
    vehiculos = relationship('Vehiculo', back_populates='departamento')
    registros_entrada = relationship('RegistroEntrada', back_populates='departamento')

class Residente(Base):
    __tablename__ = 'residentes'
    
    rut = Column(String, primary_key=True)
    nombre_completo = Column(String, nullable=False)
    departamento_id = Column(String, ForeignKey('departamentos.codigo_departamento'))
    
    # Relaciones
    departamento = relationship('Departamento', back_populates='residentes')

class Vehiculo(Base):
    __tablename__ = 'vehiculos'
    
    patente = Column(String, primary_key=True)
    departamento_id = Column(String, ForeignKey('departamentos.codigo_departamento'))
    
    # Relaciones
    departamento = relationship('Departamento', back_populates='vehiculos')

class RegistroEntrada(Base):
    __tablename__ = 'registros_entrada'
    
    id = Column(Integer, primary_key=True)
    patente = Column(String, nullable=False)
    nombre_completo = Column(String, nullable=False)
    rut = Column(String, nullable=False)
    departamento_id = Column(String, ForeignKey('departamentos.codigo_departamento'))
    es_visita = Column(Boolean, default=False)
    fecha_ingreso = Column(DateTime, default=datetime.now)
    fecha_salida = Column(DateTime, nullable=True)
    
    # Relaciones
    departamento = relationship('Departamento', back_populates='registros_entrada')