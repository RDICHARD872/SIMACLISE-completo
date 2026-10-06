-- =====================================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS - SIMACLISE (VERSIÓN COMPLETA)
-- Motor: PostgreSQL
-- Arquitectura: Sistema Relacional Multi-Nivel con Integridad Referencial
-- =====================================================================

-- =====================================================================
-- 1. TABLAS CATÁLOGO / INDEPENDIENTES
-- Estas tablas no dependen de ninguna otra. Sirven como "listas desplegables" 
-- estandarizadas para evitar que los usuarios escriban cosas distintas 
-- (ej. "El Salvador" vs "ESA" vs "El Salv.").
-- =====================================================================

-- Catálogos Geográficos y Tipos Básicos
CREATE TABLE Pais (
    ID_Pais SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Tipo_Direccion (
    ID_Tipo SERIAL PRIMARY KEY,
    Tipo VARCHAR(100) NOT NULL -- Ej: "Casa", "Oficina", "Sucursal"
);

CREATE TABLE Tipo_Documentos (
    ID_Tipo SERIAL PRIMARY KEY,
    Descripcion VARCHAR(150) NOT NULL -- Ej: "DUI", "NIT", "Pasaporte"
);

-- TABLA MAESTRA: CLIENTES
-- El núcleo del sistema. Guarda la información base del asegurado.
CREATE TABLE Clientes (
    Cliente_ID SERIAL PRIMARY KEY,
    Razon_Social VARCHAR(200) NOT NULL,
    Telefono VARCHAR(50),
    Fax VARCHAR(50),
    Celular VARCHAR(50),
    Email VARCHAR(100),
    Grupo VARCHAR(100),
    Actividad VARCHAR(200)
);

-- Catálogos para la Ficha de Contactos Empresariales
CREATE TABLE Tipo_Contacto (
    ID_Tipo SERIAL PRIMARY KEY,
    Descripcion VARCHAR(100) NOT NULL -- Ej: "Representante Legal", "Contador"
);

CREATE TABLE Area (
    ID_Area SERIAL PRIMARY KEY,
    Descripcion VARCHAR(100) NOT NULL
);

CREATE TABLE Departamento_Empresa (
    ID_Departamento SERIAL PRIMARY KEY,
    Descripcion VARCHAR(100) NOT NULL -- Ej: "Recursos Humanos", "Finanzas"
);

CREATE TABLE Cargo (
    ID_Cargo SERIAL PRIMARY KEY,
    Descripcion VARCHAR(100) NOT NULL -- Ej: "Gerente General", "Asistente"
);

CREATE TABLE Profesion (
    ID_Profesion SERIAL PRIMARY KEY,
    Descripcion VARCHAR(100) NOT NULL -- Ej: "Ingeniero", "Abogado"
);

-- Catálogos del Ecosistema de Seguros
CREATE TABLE Aseguradora (
    ID_Aseguradora SERIAL PRIMARY KEY,
    Nombre VARCHAR(150) NOT NULL -- Las compañías que emiten las pólizas
);

CREATE TABLE Ramo (
    ID_Ramo SERIAL PRIMARY KEY,
    Descripcion VARCHAR(150) NOT NULL -- Ej: "Automotores", "Vida", "Incendio"
);

CREATE TABLE Tipo_Poliza (
    ID_Tipo SERIAL PRIMARY KEY,
    Descripcion VARCHAR(150) NOT NULL -- Ej: "Individual", "Colectiva"
);

CREATE TABLE Asociado (
    ID_Asociado SERIAL PRIMARY KEY,
    Nombre VARCHAR(150) NOT NULL -- Intermediarios o corredores asociados
);

-- Catálogos de Finanzas y Pagos
CREATE TABLE Medio_Pago (
    ID_Medio_Pago SERIAL PRIMARY KEY,
    Descripcion VARCHAR(100) NOT NULL -- Ej: "Cheque", "Transferencia", "Tarjeta"
);

CREATE TABLE Forma_Pago (
    ID_Forma_Pago SERIAL PRIMARY KEY,
    Forma VARCHAR(100) NOT NULL -- Ej: "Mensual", "Anual", "Trimestral"
);

CREATE TABLE Gastos_Iniciales (
    ID_Gastos_Iniciales SERIAL PRIMARY KEY,
    Descripcion VARCHAR(150),
    Valor DECIMAL(10,2) -- Cargos extra fijos por emisión de póliza
);


-- =====================================================================
-- 2. TABLAS CON DEPENDENCIAS DE 1ER NIVEL
-- Estas tablas necesitan que existan los catálogos anteriores o el Cliente
-- para poder guardar un registro válido.
-- =====================================================================

-- Departamentos o Estados (Depende de País)
CREATE TABLE Departamento_Geo (
    ID_Departamento SERIAL PRIMARY KEY,
    ID_Pais INT,
    Nombre VARCHAR(100) NOT NULL,
    -- SET NULL: Si borramos el país, el departamento se queda, pero su ID_Pais queda vacío.
    FOREIGN KEY (ID_Pais) REFERENCES Pais(ID_Pais) ON DELETE SET NULL
);

-- Documentos de identidad del cliente
CREATE TABLE Documentos (
    Documento_ID SERIAL PRIMARY KEY,
    Cliente_ID INT,
    Tipo_ID INT,
    Numero_Documento VARCHAR(100),
    Observaciones TEXT,
    -- CASCADE: Si el cliente desaparece, sus documentos se borran automáticamente.
    FOREIGN KEY (Cliente_ID) REFERENCES Clientes(Cliente_ID) ON DELETE CASCADE,
    FOREIGN KEY (Tipo_ID) REFERENCES Tipo_Documentos(ID_Tipo) ON DELETE SET NULL
);

-- Libreta de contactos asociados a un cliente empresarial
CREATE TABLE Contactos (
    ID_Contacto SERIAL PRIMARY KEY,
    ID_Cliente INT,
    ID_Tipo INT,
    ID_Area INT,
    ID_Departamento INT,
    ID_Cargo INT,
    ID_Profesion INT,
    Nombre VARCHAR(100) NOT NULL,
    Apellidos VARCHAR(100) NOT NULL,
    Telefonos VARCHAR(50),
    Movil VARCHAR(50),
    Fax VARCHAR(50),
    Email VARCHAR(100),
    Jefe_Inmediato VARCHAR(150),
    Fecha_Nacimiento DATE,
    Observaciones TEXT,
    FOREIGN KEY (ID_Cliente) REFERENCES Clientes(Cliente_ID) ON DELETE CASCADE,
    -- Las siguientes llaves conectan con los catálogos empresariales
    FOREIGN KEY (ID_Tipo) REFERENCES Tipo_Contacto(ID_Tipo),
    FOREIGN KEY (ID_Area) REFERENCES Area(ID_Area),
    FOREIGN KEY (ID_Departamento) REFERENCES Departamento_Empresa(ID_Departamento),
    FOREIGN KEY (ID_Cargo) REFERENCES Cargo(ID_Cargo),
    FOREIGN KEY (ID_Profesion) REFERENCES Profesion(ID_Profesion)
);


-- =====================================================================
-- 3. TABLAS CON DEPENDENCIAS DE 2DO NIVEL
-- Dependen de las tablas de 1er nivel.
-- =====================================================================

-- Municipios o Ciudades (Dependen del Departamento Geográfico)
CREATE TABLE Municipio (
    ID_Municipio SERIAL PRIMARY KEY,
    ID_Departamento INT,
    Nombre VARCHAR(100) NOT NULL,
    FOREIGN KEY (ID_Departamento) REFERENCES Departamento_Geo(ID_Departamento) ON DELETE SET NULL
);


-- =====================================================================
-- 4. TABLAS CON DEPENDENCIAS DE 3ER NIVEL
-- Las direcciones conectan al cliente con la estructura geográfica completa 
-- (País -> Departamento -> Municipio).
-- =====================================================================
CREATE TABLE Direcciones (
    ID_Direccion SERIAL PRIMARY KEY,
    ID_Cliente INT,
    ID_Tipo INT,
    ID_Pais INT,
    ID_Departamento INT,
    ID_Municipio INT,
    Direccion TEXT,
    Ciudad VARCHAR(100),
    Referencias TEXT,
    Zona VARCHAR(50),
    Codigo_Postal VARCHAR(20),
    FOREIGN KEY (ID_Cliente) REFERENCES Clientes(Cliente_ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Tipo) REFERENCES Tipo_Direccion(ID_Tipo),
    FOREIGN KEY (ID_Pais) REFERENCES Pais(ID_Pais),
    FOREIGN KEY (ID_Departamento) REFERENCES Departamento_Geo(ID_Departamento),
    FOREIGN KEY (ID_Municipio) REFERENCES Municipio(ID_Municipio)
);


-- =====================================================================
-- 5. MÓDULO CORE: PÓLIZAS, PRIMAS Y PLAN DE PAGOS
-- Este es el motor financiero del sistema. Todo se conecta en cascada:
-- Cliente -> Poliza -> Prima -> Plan_Pagos (Cuotas).
-- =====================================================================

-- Contrato principal de Seguro
CREATE TABLE Poliza (
    ID_Poliza SERIAL PRIMARY KEY,
    ID_Cliente INT,
    ID_Aseguradora INT,
    ID_Ramo INT,
    ID_Tipo_Poliza INT,
    ID_Asociado INT,
    ID_Medio_Pago INT,
    ID_Forma_Pago INT,
    ID_Gastos_Iniciales INT,
    ID_Pago_Especial INT, 
    Poliza_Numero VARCHAR(50) NOT NULL,
    Observaciones TEXT,
    Inicio_Cobertura DATE,
    Fin_Cobertura DATE,
    Suma_Asegurada DECIMAL(15,2),
    Deducible DECIMAL(15,2),
    Aviso VARCHAR(100),
    Prima DECIMAL(15,2),
    Gastos_Fraccionados DECIMAL(10,2),
    IVA DECIMAL(10,2),
    Total DECIMAL(15,2),
    Numero_Pagos INT,
    Comision DECIMAL(5,2),
    Estado VARCHAR(50),
    FOREIGN KEY (ID_Cliente) REFERENCES Clientes(Cliente_ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_Aseguradora) REFERENCES Aseguradora(ID_Aseguradora),
    FOREIGN KEY (ID_Ramo) REFERENCES Ramo(ID_Ramo),
    FOREIGN KEY (ID_Tipo_Poliza) REFERENCES Tipo_Poliza(ID_Tipo),
    FOREIGN KEY (ID_Asociado) REFERENCES Asociado(ID_Asociado),
    FOREIGN KEY (ID_Medio_Pago) REFERENCES Medio_Pago(ID_Medio_Pago),
    FOREIGN KEY (ID_Forma_Pago) REFERENCES Forma_Pago(ID_Forma_Pago),
    FOREIGN KEY (ID_Gastos_Iniciales) REFERENCES Gastos_Iniciales(ID_Gastos_Iniciales)
);

-- Estructura Financiera Puente (Desglose de montos de la póliza)
CREATE TABLE Prima (
    ID_Prima SERIAL PRIMARY KEY,
    ID_Poliza INT,
    ID_Asociado INT,
    ID_Medio_Pago INT,
    ID_Forma_Pago INT,
    ID_Gastos_Iniciales INT,
    ID_Pago_Especial INT,
    Poliza_Numero VARCHAR(50),
    Observaciones TEXT,
    Inicio_Cobertura DATE,
    Fin_Cobertura DATE,
    Suma_Asegurada DECIMAL(15,2),
    Deducible DECIMAL(15,2),
    Aviso VARCHAR(100),
    Prima DECIMAL(15,2),
    Gastos_Fraccionados DECIMAL(10,2),
    IVA DECIMAL(10,2),
    Total DECIMAL(15,2),
    Numero_Pagos INT,
    Comision DECIMAL(5,2),
    Valor DECIMAL(15,2),
    FOREIGN KEY (ID_Poliza) REFERENCES Poliza(ID_Poliza) ON DELETE CASCADE,
    FOREIGN KEY (ID_Asociado) REFERENCES Asociado(ID_Asociado),
    FOREIGN KEY (ID_Medio_Pago) REFERENCES Medio_Pago(ID_Medio_Pago),
    FOREIGN KEY (ID_Forma_Pago) REFERENCES Forma_Pago(ID_Forma_Pago),
    FOREIGN KEY (ID_Gastos_Iniciales) REFERENCES Gastos_Iniciales(ID_Gastos_Iniciales)
);

-- Tabla de Cuotas (Generadas a partir de la Prima)
CREATE TABLE Plan_Pagos (
    ID_Plan_Pago SERIAL PRIMARY KEY,
    ID_Prima INT,
    Estado VARCHAR(50),  -- Ej: "Pendiente", "Pagado", "Vencido"
    Cuota_No INT,        -- Orden de la cuota (1 de 12, 2 de 12, etc.)
    Prima DECIMAL(15,2),
    Gastos DECIMAL(10,2),
    IVA DECIMAL(10,2),
    Total DECIMAL(15,2), -- Lo que el cliente debe pagar finalmente
    Documento_Fiscal VARCHAR(100),
    Aviso VARCHAR(100),
    Pagador VARCHAR(150),
    Vencimiento DATE,    -- Fecha límite de pago
    Saldo DECIMAL(15,2), -- Útil para abonos parciales
    FOREIGN KEY (ID_Prima) REFERENCES Prima(ID_Prima) ON DELETE CASCADE
);