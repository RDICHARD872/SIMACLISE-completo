from pydantic import BaseModel
from typing import Optional
from datetime import date

# =====================================================================
# ESQUEMAS DE CLIENTES
# Validamos los campos de texto, contacto y datos generales del asegurado
# =====================================================================

class ClienteCreate(BaseModel):
    razon_social: str                  # Nombre o razón social obligatorios
    telefono: Optional[str] = None     # Opcionales marcados con Optional y valor por defecto null
    fax: Optional[str] = None
    celular: Optional[str] = None
    email: Optional[str] = None
    grupo: Optional[str] = None
    actividad: Optional[str] = None

class ClienteResponse(ClienteCreate):
    cliente_id: int                    # Hereda todo lo anterior y le suma el ID autoincremental que genera la BD
    
    class Config:
        from_attributes = True         # Permite que Pydantic lea los datos directamente desde los modelos de SQLAlchemy


# =====================================================================
# ESQUEMAS DE PÓLIZAS
# Controlan los datos del contrato de seguro y sus fechas de cobertura
# =====================================================================

class PolizaCreate(BaseModel):
    id_cliente: int                    # ID del cliente dueño de esta póliza (llave foránea)
    poliza_numero: str                 # Número o código del contrato de póliza
    inicio_cobertura: Optional[date] = None
    fin_cobertura: Optional[date] = None
    suma_asegurada: Optional[float] = None
    prima: Optional[float] = None      # Monto total de la prima de seguro
    estado: Optional[str] = "Activa"   # Por defecto nace activa a menos que se indique lo contrario

class PolizaResponse(PolizaCreate):
    id_poliza: int                     # ID único de la póliza generado por la BD
    
    class Config:
        from_attributes = True


# =====================================================================
# ESQUEMAS DE PLAN DE PAGOS, PRIMAS Y CUOTAS
# Gestionan la estructura financiera y el desglose de los cobros
# =====================================================================

# Esquema para las cuotas individuales del plan de pagos
class PlanPagosCreate(BaseModel):
    id_prima: int                      # ID de la prima financiera a la que pertenece esta cuota
    cuota_no: int                      # Número de cuota (ej: 1, 2, 3...)
    vencimiento: date                  # Fecha límite de pago
    total: float                       # Monto total de la cuota
    saldo: float                       # Saldo pendiente de pago
    estado: str = "Pendiente"          # Estados posibles lógicos: Pendiente, Pagado, Vencido

class PlanPagosResponse(PlanPagosCreate):
    id_plan_pago: int                  # ID único de la cuota en la BD
    
    class Config:
        from_attributes = True

# Esquema para la tabla Prima (el puente financiero entre la Póliza y sus Cuotas)
class PrimaCreate(BaseModel):
    id_poliza: int                     # Póliza a la que se le asigna el valor financiero
    valor: float                       # Valor total de la prima

class PrimaResponse(PrimaCreate):
    id_prima: int                      # ID único de la prima
    
    class Config:
        from_attributes = True