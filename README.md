# 🛡️ SIMACLISE (Sistema de Manejo de Clientes de Seguros)

Reingeniería moderna de un sistema legacy de seguros. Este proyecto migra la lógica y el almacenamiento de una plataforma propietaria a un stack tecnológico moderno, robusto y de alto rendimiento.

---

## 🚀 Tecnologías y Lenguajes Utilizados

- **Backend**: Python 3.10+ / FastAPI (API REST asíncrona de alto rendimiento).
- **Base de Datos**: PostgreSQL 15+ (Gestor relacional con integridad referencial y borrado en cascada).
- **ORM**: SQLAlchemy (Mapeo objeto-relacional en Python).
- **Frontend**: Vue.js 3 (Composition API) + Vite (Interfaz web reactiva y moderna).
- **Validación de Datos**: Pydantic V2.

---

## 📂 Estructura del Repositorio

```text
simaclise_app/
│
├── backend/            # Servidor FastAPI, modelos, esquemas y rutas API
│   ├── main.py         # Punto de entrada y endpoints del sistema
│   ├── models.py       # Modelos relacionales de SQLAlchemy (PostgreSQL)
│   ├── schemas.py      # Contratos de validación de datos con Pydantic
│   ├── database.py     # Conexión y sesión de base de datos
│   └── requirements.txt# Dependencias de Python
│
├── frontend/           # Interfaz de usuario en Vue.js 3
│   ├── src/
│   │   ├── views/      # Vistas principales (LoginView.vue, ClientesView.vue)
│   │   └── ...
│   └── package.json    # Dependencias de Node.js
│
└── database/
    └── schema.sql      # Script SQL de respaldo con la estructura relacional

📋 ¿Qué se ha implementado? (Módulos del Sistema)
Módulo de Autenticación (Simulado): Pantalla de acceso estética inspirada en el software clásico de escritorio con redirección segura al sistema.

Módulo de Clientes (CRUD Completo): Directorio interactivo para registrar, consultar, actualizar y eliminar información de asegurados (Razón Social, Teléfono, Email, Actividad).

Módulo de Pólizas: Historial dinámico vinculado en tiempo real por cada cliente, permitiendo dar de alta contratos de seguros, fechas de cobertura, sumas aseguradas y primas.

Módulo de Plan de Pagos / Cobros (Modal): Ventana flotante automatizada que gestiona la estructura de primas y fraccionamiento de cuotas (número de cuota, vencimientos, totales, saldos y estados semánticos: Pendiente, Pagado, Vencido).

⚙️ Programas y Requisitos Previos
Antes de clonar e iniciar el proyecto, asegúrate de tener instalado en tu computadora:

Python (Versión 3.10 o superior)

Node.js (Versión 18 o superior con npm)

PostgreSQL (Servidor de base de datos activo)

Visual Studio Code (O tu editor de código preferido)

🛠️ Guía de Instalación y Puesta en Marcha
1. Configurar la Base de Datos en PostgreSQL
Abre tu cliente de PostgreSQL (pgAdmin o terminal).

Crea una base de datos vacía llamada simaclise_db:

SQL
CREATE DATABASE simaclise_db;
(Opcional) Si deseas restaurar la estructura base, puedes ejecutar el script ubicado en database/schema.sql.

2. Configurar y Levantar el Backend (FastAPI)
Abre una terminal y sitúate en la carpeta backend/:

Bash
cd backend
Crea y activa tu entorno virtual:

Bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
Instala las dependencias del servidor:

Bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic
Crea un archivo .env dentro de la carpeta backend/ con tus credenciales de PostgreSQL:

Code snippet
DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/simaclise_db
Inicia el servidor de desarrollo del backend:

Bash
uvicorn main:app --reload
(El servidor correrá en http://localhost:8000. Puedes verificar la documentación automática en http://localhost:8000/docs).

3. Configurar y Levantar el Frontend (Vue.js)
Abre una nueva terminal independiente y sitúate en la carpeta frontend/:

Bash
cd frontend
Instala los paquetes de Node.js:

Bash
npm install
Inicia el servidor de interfaz web con Vite:

Bash
npm run dev
(La aplicación web estará disponible en http://localhost:5173).

👥 Uso del Sistema
Entra a http://localhost:5173.

Haz clic en el botón "✔️ OK" en la pantalla de inicio de sesión.

Administra clientes, despliega sus pólizas en el panel inferior, añade cuotas y gestiona sus cobros con total fluidez.


---

### ¿Cómo queda tu estructura para GitHub?
Con este `README.md` y la carpeta de esquema SQL incluida, tu repositorio reflejará