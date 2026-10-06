from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, engine, Base
import models
import schemas

# Crea las tablas automáticamente en PostgreSQL si aún no existen (respaldado por SQLAlchemy)
models.Base.metadata.create_all(bind=engine)

# Inicializamos la aplicación FastAPI con un título y versión
app = FastAPI(title="SIMACLISE API", version="1.0")

# ==========================================
# CONFIGURACIÓN DE CORS
# ==========================================
# Permite que el Frontend (que corre en el puerto 5173 de Vue) pueda comunicarse con este Backend sin bloqueos de seguridad
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta raíz para verificar rápidamente que la API está encendida
@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido a la API de SIMACLISE"}

# Ruta de diagnóstico para comprobar que PostgreSQL responde correctamente a las consultas
@app.get("/test-db")
def probar_base_datos(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        if result == 1:
            return {"mensaje": "¡Conexión exitosa a la base de datos PostgreSQL!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar a la base de datos: {str(e)}")


# ==========================================
# RUTAS DE CLIENTES (CRUD COMPLETO)
# ==========================================

# 1. Registrar un cliente nuevo en la base de datos
@app.post("/clientes/", response_model=schemas.ClienteResponse)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# 2. Listar todos los clientes guardados (con paginación opcional)
@app.get("/clientes/", response_model=list[schemas.ClienteResponse])
def leer_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
    return clientes

# 3. Actualizar los datos de un cliente existente mediante su ID
@app.put("/clientes/{cliente_id}", response_model=schemas.ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente_actualizado: schemas.ClienteCreate, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.cliente_id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Reemplazamos los campos viejos con la nueva información recibida
    for key, value in cliente_actualizado.model_dump().items():
        setattr(cliente, key, value)
        
    db.commit()
    db.refresh(cliente)
    return cliente

# 4. Eliminar un cliente (y en cascada sus pólizas y pagos gracias a la configuración de la BD)
@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.cliente_id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(cliente)
    db.commit()
    return {"mensaje": "Cliente eliminado correctamente"}


# ==========================================
# RUTAS DE PÓLIZAS (CRUD COMPLETO)
# ==========================================

# 1. Registrar una nueva póliza vinculada a un cliente específico
@app.post("/polizas/", response_model=schemas.PolizaResponse)
def crear_poliza(poliza: schemas.PolizaCreate, db: Session = Depends(get_db)):
    db_poliza = models.Poliza(**poliza.model_dump())
    db.add(db_poliza)
    db.commit()
    db.refresh(db_poliza)
    return db_poliza

# 2. Consultar el historial de pólizas que pertenecen a un cliente en concreto
@app.get("/clientes/{cliente_id}/polizas/", response_model=list[schemas.PolizaResponse])
def leer_polizas_de_cliente(cliente_id: int, db: Session = Depends(get_db)):
    polizas = db.query(models.Poliza).filter(models.Poliza.id_cliente == cliente_id).all()
    return polizas

# 3. Actualizar los datos de una póliza existente
@app.put("/polizas/{poliza_id}", response_model=schemas.PolizaResponse)
def actualizar_poliza(poliza_id: int, poliza_actualizada: schemas.PolizaCreate, db: Session = Depends(get_db)):
    poliza = db.query(models.Poliza).filter(models.Poliza.id_poliza == poliza_id).first()
    if not poliza:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    
    for key, value in poliza_actualizada.model_dump().items():
        setattr(poliza, key, value)
        
    db.commit()
    db.refresh(poliza)
    return poliza

# 4. Eliminar una póliza del sistema
@app.delete("/polizas/{poliza_id}")
def eliminar_poliza(poliza_id: int, db: Session = Depends(get_db)):
    poliza = db.query(models.Poliza).filter(models.Poliza.id_poliza == poliza_id).first()
    if not poliza:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    
    db.delete(poliza)
    db.commit()
    return {"mensaje": "Póliza eliminada"}


# ==========================================
# RUTAS DE PLAN DE PAGOS, PRIMAS Y CUOTAS
# ==========================================

# 1. Crear la estructura financiera base (Prima) asociada a una póliza
@app.post("/primas/", response_model=schemas.PrimaResponse)
def crear_prima(prima: schemas.PrimaCreate, db: Session = Depends(get_db)):
    db_prima = models.Prima(**prima.model_dump())
    db.add(db_prima)
    db.commit()
    db.refresh(db_prima)
    return db_prima

# 2. Registrar una cuota individual dentro del plan de pagos
@app.post("/pagos/", response_model=schemas.PlanPagosResponse)
def crear_cuota(cuota: schemas.PlanPagosCreate, db: Session = Depends(get_db)):
    db_cuota = models.PlanPagos(**cuota.model_dump())
    db.add(db_cuota)
    db.commit()
    db.refresh(db_cuota)
    return db_cuota

# 3. Consultar las cuotas de una póliza cruzando las tablas relacionales (Poliza -> Prima -> Plan_Pagos)
@app.get("/polizas/{poliza_id}/pagos/", response_model=list[schemas.PlanPagosResponse])
def leer_pagos_de_poliza(poliza_id: int, db: Session = Depends(get_db)):
    prima = db.query(models.Prima).filter(models.Prima.id_poliza == poliza_id).first()
    if not prima:
        return [] # Si la póliza no tiene prima financiera creada, devolvemos una lista vacía
    cuotas = db.query(models.PlanPagos).filter(models.PlanPagos.id_prima == prima.id_prima).all()
    return cuotas

# 4. Actualizar los montos o el estado (Pendiente, Pagado, Vencido) de una cuota
@app.put("/pagos/{pago_id}", response_model=schemas.PlanPagosResponse)
def actualizar_cuota(pago_id: int, cuota_actualizada: schemas.PlanPagosCreate, db: Session = Depends(get_db)):
    cuota = db.query(models.PlanPagos).filter(models.PlanPagos.id_plan_pago == pago_id).first()
    if not cuota:
        raise HTTPException(status_code=404, detail="Cuota no encontrada")
    
    for key, value in cuota_actualizada.model_dump().items():
        setattr(cuota, key, value)
        
    db.commit()
    db.refresh(cuota)
    return cuota

# 5. Eliminar una cuota específica del plan de pagos
@app.delete("/pagos/{pago_id}")
def eliminar_cuota(pago_id: int, db: Session = Depends(get_db)):
    cuota = db.query(models.PlanPagos).filter(models.PlanPagos.id_plan_pago == pago_id).first()
    if not cuota:
        raise HTTPException(status_code=404, detail="Cuota no encontrada")
    
    db.delete(cuota)
    db.commit()
    return {"mensaje": "Cuota eliminada"}