from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from database import Base

# =====================================================================
# MODELO: CLIENTES
# Mapea la tabla 'clientes' en PostgreSQL con los datos de contacto y actividad.
# =====================================================================
class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id = Column("cliente_id", Integer, primary_key=True, index=True)
    razon_social = Column("razon_social", String(200), nullable=False) # Nombre o empresa obligatorios
    telefono = Column("telefono", String(50))
    fax = Column("fax", String(50))
    celular = Column("celular", String(50))
    email = Column("email", String(100))
    grupo = Column("grupo", String(100))
    actividad = Column("actividad", String(200))


# =====================================================================
# MODELO: PÓLIZAS
# Mapea la tabla 'poliza' y establece la relación de pertenencia con un cliente.
# =====================================================================
class Poliza(Base):
    __tablename__ = "poliza"

    id_poliza = Column("id_poliza", Integer, primary_key=True, index=True)
    
    # Llave foránea que apunta al cliente dueño. 
    # 'ondelete="CASCADE"' asegura que si borras al cliente, sus pólizas se borran automáticamente.
    id_cliente = Column("id_cliente", Integer, ForeignKey("clientes.cliente_id", ondelete="CASCADE"))
    
    poliza_numero = Column("poliza_numero", String(50), nullable=False)
    inicio_cobertura = Column("inicio_cobertura", Date)
    fin_cobertura = Column("fin_cobertura", Date)
    suma_asegurada = Column("suma_asegurada", Numeric(15,2)) # Usamos Numeric para precisión monetaria exacta
    prima = Column("prima", Numeric(15,2))
    estado = Column("estado", String(50))


# =====================================================================
# MODELO: PRIMA (ESTRUCTURA FINANCIERA)
# Tabla puente que almacena el valor financiero de la prima asociada a una póliza.
# =====================================================================
class Prima(Base):
    __tablename__ = "prima"

    id_prima = Column("id_prima", Integer, primary_key=True, index=True)
    
    # Llave foránea vinculada a la póliza correspondiente
    id_poliza = Column("id_poliza", Integer, ForeignKey("poliza.id_poliza", ondelete="CASCADE"))
    
    valor = Column("valor", Numeric(15,2))


# =====================================================================
# MODELO: PLAN DE PAGOS (CUOTAS)
# Mapea la tabla 'plan_pagos' para controlar el fraccionamiento y cobro de cuotas.
# =====================================================================
class PlanPagos(Base):
    __tablename__ = "plan_pagos"

    id_plan_pago = Column("id_plan_pago", Integer, primary_key=True, index=True)
    
    # Llave foránea vinculada a la tabla Prima de la cual se desglosan las cuotas
    id_prima = Column("id_prima", Integer, ForeignKey("prima.id_prima", ondelete="CASCADE"))
    
    cuota_no = Column("cuota_no", Integer)       # Número de cuota (1, 2, 3...)
    vencimiento = Column("vencimiento", Date)    # Fecha límite de pago
    total = Column("total", Numeric(15,2))       # Monto total de la cuota
    saldo = Column("saldo", Numeric(15,2))       # Saldo pendiente
    estado = Column("estado", String(50))        # Estado (Pendiente, Pagado, Vencido)