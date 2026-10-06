<template>
  <!-- Contenedor principal que envuelve toda la pantalla de clientes -->
  <div class="clientes-container">
    
    <!-- ========================================== -->
    <!-- BARRA SUPERIOR (HEADER)                    -->
    <!-- ========================================== -->
    <header class="topbar">
      <h2>Módulo de Clientes</h2>
      <div>
        <!-- Botón dinámico: Cambia su texto entre "+ Nuevo Cliente" y "Cancelar" dependiendo de si el formulario está abierto o no -->
        <button class="btn-nuevo" @click="abrirFormularioNuevo">
          {{ mostrarFormulario ? 'Cancelar' : '+ Nuevo Cliente' }}
        </button>
        <!-- Botón para regresar a la pantalla de Login (cerrar sesión) -->
        <button class="btn-cerrar" @click="cerrarSesion">Cerrar Sesión</button>
      </div>
    </header>

    <!-- ========================================== -->
    <!-- ÁREA 1: FORMULARIO DE CLIENTES (CREAR/EDITAR)-->
    <!-- ========================================== -->
    <!-- Este panel solo aparece si la variable 'mostrarFormulario' es verdadera. -->
    <div v-if="mostrarFormulario" class="form-container" :class="{'form-edicion': modoEdicion}">
      <!-- El título cambia mágicamente para avisarnos si estamos creando uno nuevo o editando uno existente -->
      <h3>{{ modoEdicion ? 'Editar Cliente' : 'Ingreso de Cliente' }}</h3>
      
      <!-- Usamos @submit.prevent para que la página no se recargue al darle al botón de guardar -->
      <form @submit.prevent="guardarCliente" class="cliente-form">
        <div class="input-group">
          <label>Razón Social *</label>
          <input type="text" v-model="clienteForm.razon_social" required placeholder="Ej. Juan Pérez" />
        </div>
        <div class="input-group">
          <label>Teléfono</label>
          <input type="text" v-model="clienteForm.telefono" placeholder="Ej. 2255-0000" />
        </div>
        <div class="input-group">
          <label>Email</label>
          <input type="email" v-model="clienteForm.email" placeholder="correo@ejemplo.com" />
        </div>
        <!-- El botón de guardar se pinta de naranja si estamos editando -->
        <button type="submit" class="btn-guardar" :class="{'btn-actualizar': modoEdicion}">
          {{ modoEdicion ? 'Actualizar Cliente' : 'Guardar Cliente' }}
        </button>
      </form>
    </div>

    <!-- ========================================== -->
    <!-- ÁREA 2: TABLA PRINCIPAL DE CLIENTES        -->
    <!-- ========================================== -->
    <div class="table-container">
      <h3>Directorio de Clientes</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Razón Social</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <!-- Bucle 'v-for': Vue dibuja una fila <tr> por cada cliente que traemos de la base de datos -->
          <!-- También resaltamos la fila de azul si es el cliente que tenemos seleccionado viendo sus pólizas -->
          <tr v-for="cliente in clientes" :key="cliente.cliente_id" 
              :class="{'fila-seleccionada': clienteSeleccionado?.cliente_id === cliente.cliente_id}">
            <td>{{ cliente.cliente_id }}</td>
            <td>{{ cliente.razon_social }}</td>
            <td>{{ cliente.telefono || 'N/A' }}</td>
            <td>{{ cliente.email || 'N/A' }}</td>
            <td class="celda-acciones">
              <!-- Botones de acción rápida para cada cliente -->
              <button class="btn-ver" @click="verPolizas(cliente)">Ver Pólizas</button>
              <button class="btn-editar" @click="prepararEdicion(cliente)">Editar</button>
              <button class="btn-eliminar" @click="eliminarCliente(cliente.cliente_id, cliente.razon_social)">Eliminar</button>
            </td>
          </tr>
          <!-- Mensaje amistoso si la base de datos aún no tiene ningún cliente -->
          <tr v-if="clientes.length === 0">
            <td colspan="5" class="empty-state">No hay clientes registrados...</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ========================================== -->
    <!-- ÁREA 3: PANEL INFERIOR DE PÓLIZAS          -->
    <!-- ========================================== -->
    <!-- Solo se muestra cuando hacemos clic en "Ver Pólizas" de algún cliente -->
    <div v-if="clienteSeleccionado" class="polizas-container">
      <div class="topbar-polizas">
        <h3>Historial de Pólizas: <span class="resaltado">{{ clienteSeleccionado.razon_social }}</span></h3>
        <div>
          <button class="btn-nueva-poliza" @click="abrirFormularioPolizaNueva">
            {{ mostrarFormularioPoliza ? 'Cancelar Registro' : '+ Nueva Póliza' }}
          </button>
          <button class="btn-cerrar-polizas" @click="clienteSeleccionado = null">✖ Cerrar Panel</button>
        </div>
      </div>
      
      <!-- FORMULARIO DE PÓLIZAS (Oculto por defecto) -->
      <div v-if="mostrarFormularioPoliza" class="form-container form-poliza" :class="{'form-edicion-poliza': modoEdicionPoliza}">
        <h4>{{ modoEdicionPoliza ? 'Editar Póliza' : 'Registrar Póliza' }}</h4>
        <form @submit.prevent="guardarPoliza" class="poliza-form">
          <div class="input-group">
            <label>No. Póliza *</label>
            <input type="text" v-model="nuevaPoliza.poliza_numero" required />
          </div>
          <div class="input-group">
            <label>Inicio Cobertura</label>
            <input type="date" v-model="nuevaPoliza.inicio_cobertura" />
          </div>
          <div class="input-group">
            <label>Fin Cobertura</label>
            <input type="date" v-model="nuevaPoliza.fin_cobertura" />
          </div>
          <div class="input-group">
            <label>Suma Asegurada ($)</label>
            <input type="number" step="0.01" v-model="nuevaPoliza.suma_asegurada" />
          </div>
          <div class="input-group">
            <label>Prima ($)</label>
            <input type="number" step="0.01" v-model="nuevaPoliza.prima" />
          </div>
          <button type="submit" class="btn-guardar btn-guardar-poliza" :class="{'btn-actualizar': modoEdicionPoliza}">
            {{ modoEdicionPoliza ? 'Actualizar Póliza' : 'Guardar Póliza' }}
          </button>
        </form>
      </div>

      <!-- TABLA DE PÓLIZAS DEL CLIENTE SELECCIONADO -->
      <table class="tabla-polizas">
        <thead>
          <tr>
            <th>No. Póliza</th>
            <th>Inicio Cobertura</th>
            <th>Fin Cobertura</th>
            <th>Suma Asegurada</th>
            <th>Prima</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="poliza in polizas" :key="poliza.id_poliza">
            <td><strong>{{ poliza.poliza_numero }}</strong></td>
            <td>{{ poliza.inicio_cobertura || 'N/A' }}</td>
            <td>{{ poliza.fin_cobertura || 'N/A' }}</td>
            <td>${{ poliza.suma_asegurada || '0.00' }}</td>
            <td>${{ poliza.prima || '0.00' }}</td>
            <td>
              <span :class="poliza.estado === 'Activa' ? 'badge-activa' : 'badge-inactiva'">
                {{ poliza.estado || 'N/A' }}
              </span>
            </td>
            <td class="celda-acciones">
              <button class="btn-cobros" @click="abrirPagos(poliza)">Ver Cobros</button>
              <button class="btn-editar" @click="prepararEdicionPoliza(poliza)">Editar</button>
              <button class="btn-eliminar" @click="eliminarPoliza(poliza.id_poliza, poliza.poliza_numero)">Eliminar</button>
            </td>
          </tr>
          <tr v-if="polizas.length === 0">
            <td colspan="7" class="empty-state">Este cliente no tiene pólizas registradas.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ========================================== -->
    <!-- ÁREA 4: MODAL DE PLAN DE PAGOS (COBROS)    -->
    <!-- ========================================== -->
    <!-- Este panel flota por encima de toda la pantalla y oscurece el fondo (overlay) -->
    <div v-if="modalPagos" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Plan de Pagos - Póliza: <span class="resaltado">{{ polizaActiva.poliza_numero }}</span></h3>
          <button class="btn-cerrar-modal" @click="modalPagos = false">✖</button>
        </div>

        <!-- FORMULARIO DE CUOTAS -->
        <div class="form-container form-pago" :class="{'form-edicion-pago': modoEdicionCuota}">
          <h4>{{ modoEdicionCuota ? 'Editar Cuota' : 'Registrar Cuota' }}</h4>
          <form @submit.prevent="guardarCuota" class="pago-form">
            <div class="input-group">
              <label>No. Cuota</label>
              <input type="number" v-model="nuevaCuota.cuota_no" required />
            </div>
            <div class="input-group">
              <label>Vencimiento</label>
              <input type="date" v-model="nuevaCuota.vencimiento" required />
            </div>
            <div class="input-group">
              <label>Total a Pagar ($)</label>
              <input type="number" step="0.01" v-model="nuevaCuota.total" required />
            </div>
            <div class="input-group">
              <label>Saldo ($)</label>
              <input type="number" step="0.01" v-model="nuevaCuota.saldo" />
            </div>
            <div class="input-group">
              <label>Estado</label>
              <!-- Selector desplegable para evitar que el usuario escriba mal los estados -->
              <select v-model="nuevaCuota.estado" class="select-estado">
                <option value="Pendiente">Pendiente</option>
                <option value="Pagado">Pagado</option>
                <option value="Vencido">Vencido</option>
              </select>
            </div>
            <button type="submit" class="btn-guardar btn-guardar-pago" :class="{'btn-actualizar': modoEdicionCuota}">
              {{ modoEdicionCuota ? 'Actualizar Cuota' : '+ Agregar Cuota' }}
            </button>
            <button v-if="modoEdicionCuota" type="button" class="btn-cerrar btn-cancelar-pago" @click="cancelarEdicionCuota">Cancelar</button>
          </form>
        </div>

        <!-- TABLA DE CUOTAS DEL MODAL -->
        <table class="tabla-pagos">
          <thead>
            <tr>
              <th>Cuota No.</th>
              <th>Vencimiento</th>
              <th>Total</th>
              <th>Saldo</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cuota in cuotas" :key="cuota.id_plan_pago">
              <td>{{ cuota.cuota_no }}</td>
              <td>{{ cuota.vencimiento }}</td>
              <td>${{ cuota.total }}</td>
              <td>${{ cuota.saldo }}</td>
              <td>
                <!-- Asignamos clases CSS (colores) diferentes dependiendo de la palabra exacta en el estado -->
                <span :class="{'badge-pagado': cuota.estado === 'Pagado', 'badge-pendiente': cuota.estado === 'Pendiente', 'badge-vencido': cuota.estado === 'Vencido'}">
                  {{ cuota.estado }}
                </span>
              </td>
              <td class="celda-acciones">
                <button class="btn-editar" @click="prepararEdicionCuota(cuota)">Editar</button>
                <button class="btn-eliminar" @click="eliminarCuota(cuota.id_plan_pago, cuota.cuota_no)">Eliminar</button>
              </td>
            </tr>
            <tr v-if="cuotas.length === 0">
              <td colspan="6" class="empty-state">No hay cuotas registradas para esta póliza.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
// Importaciones base de Vue
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// =================================================================
// 1. ZONA DE VARIABLES REACTIVAS (ESTADOS DE LA APP)
// Todo lo que envuelves en ref() Vue lo vigila, y si cambia, redibuja la pantalla.
// =================================================================

// --- Clientes ---
const clientes = ref([]) // Lista maestra donde guardamos lo que llega de la BD
const mostrarFormulario = ref(false) // Interruptor para mostrar/ocultar el panel de agregar cliente
const modoEdicion = ref(false) // Avisa si el formulario es para crear (false) o actualizar (true)
const idEdicion = ref(null) // Guarda el ID del cliente que estamos editando actualmente
const clienteForm = ref({ razon_social: '', telefono: '', email: '' }) // Plantilla vacía del formulario

// --- Pólizas ---
const clienteSeleccionado = ref(null) // Guarda todo el objeto del cliente al que le hicimos clic en "Ver Pólizas"
const polizas = ref([]) // Lista de pólizas exclusivas de ese cliente
const mostrarFormularioPoliza = ref(false)
const modoEdicionPoliza = ref(false)
const idEdicionPoliza = ref(null)
const nuevaPoliza = ref({ poliza_numero: '', inicio_cobertura: '', fin_cobertura: '', suma_asegurada: null, prima: null, estado: 'Activa' })

// --- Pagos y Cuotas ---
const modalPagos = ref(false) // Interruptor para mostrar la ventana negra emergente
const polizaActiva = ref(null) // La póliza a la que le estamos viendo los pagos
const cuotas = ref([]) // Las cuotas que pertenecen a esa póliza
const idPrimaActual = ref(null) // El nexo invisible entre Póliza y Cuota (la tabla Prima)
const modoEdicionCuota = ref(false)
const idEdicionCuota = ref(null)
const nuevaCuota = ref({ cuota_no: 1, vencimiento: '', total: null, saldo: null, estado: 'Pendiente' })


// =================================================================
// 2. LÓGICA DE NEGOCIO (FUNCIONES Y LLAMADAS A LA API / FASTAPI)
// =================================================================

// -------- BLOQUE: CLIENTES --------

// Trae todos los clientes desde nuestra base de datos PostgreSQL
const cargarClientes = async () => {
  try {
    const res = await fetch('http://localhost:8000/clientes/')
    if (res.ok) clientes.value = await res.json()
  } catch (error) { console.error('Error cargando clientes:', error) }
}

// Configura la pantalla para crear un cliente totalmente nuevo
const abrirFormularioNuevo = () => {
  if (mostrarFormulario.value && !modoEdicion.value) {
    mostrarFormulario.value = false // Si ya está abierto y vacío, lo cerramos
  } else {
    modoEdicion.value = false // Apagamos el modo edición por si veníamos de allí
    clienteForm.value = { razon_social: '', telefono: '', email: '' } // Limpiamos campos
    mostrarFormulario.value = true
  }
}

// Configura el formulario, pero rellenándolo con los datos de un cliente existente
const prepararEdicion = (cliente) => {
  modoEdicion.value = true
  idEdicion.value = cliente.cliente_id
  clienteForm.value = { razon_social: cliente.razon_social, telefono: cliente.telefono, email: cliente.email }
  mostrarFormulario.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' }) // Sube la pantalla suavemente para que veas el formulario
}

// Envía la orden al servidor: si es nuevo usa POST, si es editar usa PUT.
const guardarCliente = async () => {
  try {
    // Magia condicional: armamos la URL y el método correcto dependiendo de si estamos editando o creando
    const url = modoEdicion.value ? `http://localhost:8000/clientes/${idEdicion.value}` : 'http://localhost:8000/clientes/'
    const metodo = modoEdicion.value ? 'PUT' : 'POST'

    const res = await fetch(url, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(clienteForm.value) // Transformamos nuestro objeto de Vue a JSON para que Python lo entienda
    })
    
    if (res.ok) {
      // Limpieza post-guardado
      clienteForm.value = { razon_social: '', telefono: '', email: '' }
      mostrarFormulario.value = false
      modoEdicion.value = false
      cargarClientes() // Refrescamos la tabla para ver el cambio instantáneo
      
      // Detalle UX: Si editamos al cliente del cual estábamos viendo sus pólizas, actualizamos su nombre en el título inferior
      if (clienteSeleccionado.value && clienteSeleccionado.value.cliente_id === idEdicion.value) {
        clienteSeleccionado.value.razon_social = clienteForm.value.razon_social
      }
    }
  } catch (error) { console.error('Error al guardar cliente:', error) }
}

// Elimina el cliente tras pedir confirmación (para evitar desastres por clic accidental)
const eliminarCliente = async (id, nombre) => {
  if (confirm(`¿Estás completamente seguro de eliminar a "${nombre}"? Esta acción borrará todas sus pólizas y pagos.`)) {
    try {
      const res = await fetch(`http://localhost:8000/clientes/${id}`, { method: 'DELETE' })
      if (res.ok) {
        cargarClientes()
        // Si borramos al cliente activo, ocultamos el panel de pólizas para no dejarlo huérfano
        if (clienteSeleccionado.value && clienteSeleccionado.value.cliente_id === id) clienteSeleccionado.value = null
      }
    } catch (error) { console.error('Error al eliminar:', error) }
  }
}

// -------- BLOQUE: PÓLIZAS --------

// Abre el panel inferior y busca las pólizas amarradas a este cliente en particular
const verPolizas = async (cliente) => {
  clienteSeleccionado.value = cliente
  mostrarFormularioPoliza.value = false // Cerramos el formulario si estaba abierto
  modoEdicionPoliza.value = false
  try {
    const res = await fetch(`http://localhost:8000/clientes/${cliente.cliente_id}/polizas/`)
    if (res.ok) polizas.value = await res.json()
  } catch (error) { console.error(error) }
}

// Prepara el panel de pólizas para ingresar una nueva
const abrirFormularioPolizaNueva = () => {
  if (mostrarFormularioPoliza.value && !modoEdicionPoliza.value) {
    mostrarFormularioPoliza.value = false
  } else {
    modoEdicionPoliza.value = false
    nuevaPoliza.value = { poliza_numero: '', inicio_cobertura: '', fin_cobertura: '', suma_asegurada: null, prima: null, estado: 'Activa' }
    mostrarFormularioPoliza.value = true
  }
}

// Rellena el formulario de pólizas con datos existentes para actualizar
const prepararEdicionPoliza = (poliza) => {
  modoEdicionPoliza.value = true
  idEdicionPoliza.value = poliza.id_poliza
  nuevaPoliza.value = { ...poliza } // Desestructuramos para clonar el objeto rápido
  mostrarFormularioPoliza.value = true
}

const guardarPoliza = async () => {
  try {
    // Armamos los datos asegurando que los campos vacíos no rompan la base de datos (pasamos null o 0)
    const payload = {
      id_cliente: clienteSeleccionado.value.cliente_id, // Amarre vital
      poliza_numero: nuevaPoliza.value.poliza_numero,
      inicio_cobertura: nuevaPoliza.value.inicio_cobertura || null,
      fin_cobertura: nuevaPoliza.value.fin_cobertura || null,
      suma_asegurada: nuevaPoliza.value.suma_asegurada || 0,
      prima: nuevaPoliza.value.prima || 0,
      estado: nuevaPoliza.value.estado
    }
    
    const url = modoEdicionPoliza.value ? `http://localhost:8000/polizas/${idEdicionPoliza.value}` : 'http://localhost:8000/polizas/'
    const metodo = modoEdicionPoliza.value ? 'PUT' : 'POST'

    const res = await fetch(url, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (res.ok) {
      nuevaPoliza.value = { poliza_numero: '', inicio_cobertura: '', fin_cobertura: '', suma_asegurada: null, prima: null, estado: 'Activa' }
      mostrarFormularioPoliza.value = false
      modoEdicionPoliza.value = false
      verPolizas(clienteSeleccionado.value) // Refrescamos tabla de pólizas
    }
  } catch (error) { console.error(error) }
}

const eliminarPoliza = async (id, numero) => {
  if (confirm(`¿Eliminar la póliza "${numero}" y todos sus pagos vinculados?`)) {
    try {
      const res = await fetch(`http://localhost:8000/polizas/${id}`, { method: 'DELETE' })
      if (res.ok) verPolizas(clienteSeleccionado.value)
    } catch (error) { console.error(error) }
  }
}

// -------- BLOQUE: PLAN DE PAGOS (CUOTAS) --------

// Abre la ventana negra emergente (Modal) y consulta las cuotas de esa póliza
const abrirPagos = async (poliza) => {
  polizaActiva.value = poliza
  modalPagos.value = true
  modoEdicionCuota.value = false
  nuevaCuota.value = { cuota_no: 1, vencimiento: '', total: null, saldo: null, estado: 'Pendiente' }
  await cargarCuotas(poliza.id_poliza)
}

const cargarCuotas = async (idPoliza) => {
  try {
    const res = await fetch(`http://localhost:8000/polizas/${idPoliza}/pagos/`)
    if (res.ok) {
      cuotas.value = await res.json()
      // Si la póliza ya tiene cuotas, capturamos su "id_prima" para usarlo al guardar futuras cuotas
      if (cuotas.value.length > 0) idPrimaActual.value = cuotas.value[0].id_prima
      else idPrimaActual.value = null
    }
  } catch (error) { console.error(error) }
}

const prepararEdicionCuota = (cuota) => {
  modoEdicionCuota.value = true
  idEdicionCuota.value = cuota.id_plan_pago
  nuevaCuota.value = { ...cuota }
}

const cancelarEdicionCuota = () => {
  modoEdicionCuota.value = false
  // Inteligencia de UX: Si cancelamos, preparamos el formulario para la SIGUIENTE cuota sumándole 1 a la última registrada
  const proximoNo = cuotas.value.length > 0 ? cuotas.value[cuotas.value.length - 1].cuota_no + 1 : 1
  nuevaCuota.value = { cuota_no: proximoNo, vencimiento: '', total: null, saldo: null, estado: 'Pendiente' }
}

const guardarCuota = async () => {
  try {
    let idPrima = idPrimaActual.value
    
    // Rutina de rescate: Si es la PRIMERA cuota y no existe "Prima" en la BD, la creamos al vuelo invisiblemente.
    if (!idPrima) {
      const resPrima = await fetch('http://localhost:8000/primas/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_poliza: polizaActiva.value.id_poliza, valor: polizaActiva.value.prima || 0 })
      })
      const primaData = await resPrima.json()
      idPrima = primaData.id_prima
      idPrimaActual.value = idPrima
    }

    const payload = {
      id_prima: idPrima,
      cuota_no: nuevaCuota.value.cuota_no,
      vencimiento: nuevaCuota.value.vencimiento,
      total: nuevaCuota.value.total || 0,
      saldo: nuevaCuota.value.saldo || 0,
      estado: nuevaCuota.value.estado
    }

    const url = modoEdicionCuota.value ? `http://localhost:8000/pagos/${idEdicionCuota.value}` : 'http://localhost:8000/pagos/'
    const metodo = modoEdicionCuota.value ? 'PUT' : 'POST'

    const res = await fetch(url, {
      method: metodo,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    
    if (res.ok) {
      cancelarEdicionCuota() // Usamos cancelar como atajo para resetear el form
      cargarCuotas(polizaActiva.value.id_poliza)
    }
  } catch (error) { console.error(error) }
}

const eliminarCuota = async (id, numero) => {
  if (confirm(`¿Eliminar la cuota No. ${numero}?`)) {
    try {
      const res = await fetch(`http://localhost:8000/pagos/${id}`, { method: 'DELETE' })
      if (res.ok) cargarCuotas(polizaActiva.value.id_poliza)
    } catch (error) { console.error(error) }
  }
}

// Cierra sesión volviendo a la ruta raíz (Login)
const cerrarSesion = () => router.push('/')

// =================================================================
// 3. CICLO DE VIDA
// onMounted ejecuta código automáticamente apenas la página termina de cargar
// =================================================================
onMounted(() => {
  cargarClientes() // Traemos los clientes para que la tabla no esté vacía al entrar
})
</script>

<style scoped>
/*
  ESTILOS (CSS)
  - 'scoped' significa que los estilos de aquí no afectarán a otras pantallas o componentes de Vue.
  - La mayoría de clases usan flexbox para mantener los botones y formularios alineados y ordenados.
*/

/* --- GENERAL --- */
.clientes-container { padding: 30px; font-family: sans-serif; }
.topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
h2 { margin: 0; color: #2c6499; }
h3 { margin-top: 0; color: #444; font-size: 16px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
h4 { margin-top: 0; color: #444; font-size: 14px; margin-bottom: 15px; }

/* --- BOTONES GLOBALES --- */
.btn-nuevo { background: #28a745; color: white; border: none; padding: 6px 12px; cursor: pointer; border-radius: 4px; margin-right: 10px; }
.btn-nuevo:hover { background: #218838; }
.btn-cerrar { background: #666; color: white; border: none; padding: 6px 12px; cursor: pointer; border-radius: 4px; }
.btn-cerrar:hover { background: #444; }

/* --- DISEÑO DE FORMULARIOS --- */
.form-container { background: #fff; padding: 20px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #ddd; margin-bottom: 20px; }
/* Borde naranja para distinguir visualmente cuando estamos editando algo y no creándolo */
.form-edicion { border-left: 4px solid #fd7e14; background: #fff8f3; }
.cliente-form, .poliza-form, .pago-form { display: flex; flex-wrap: wrap; gap: 15px; align-items: flex-end; }
.input-group { display: flex; flex-direction: column; }
.input-group label { font-size: 12px; color: #555; margin-bottom: 4px; font-weight: bold; }
.input-group input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 180px; }
.select-estado { padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 120px; }
.btn-guardar { background: #007bff; color: white; border: none; padding: 9px 15px; cursor: pointer; border-radius: 4px; height: fit-content; }
.btn-guardar:hover { background: #0069d9; }
.btn-actualizar { background: #fd7e14; }
.btn-actualizar:hover { background: #e86c02; }

/* --- DISEÑO DE TABLAS --- */
.table-container { background: white; padding: 20px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #ddd; margin-bottom: 20px; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #eee; }
th { background-color: #f4f6f9; font-weight: bold; color: #333; }
tr:hover { background-color: #f9f9f9; }
.empty-state { text-align: center; color: #888; font-style: italic; }

/* --- BOTONES DENTRO DE LAS TABLAS (CRUD) --- */
.celda-acciones { display: flex; gap: 5px; }
.btn-ver { background: #17a2b8; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; font-size: 12px; }
.btn-ver:hover { background: #138496; }
.btn-editar { background: #fd7e14; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; font-size: 12px; }
.btn-editar:hover { background: #e86c02; }
.btn-eliminar { background: #dc3545; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; font-size: 12px; }
.btn-eliminar:hover { background: #c82333; }
.fila-seleccionada { background-color: #e0ebf5 !important; }

/* --- ESTILOS ESPECÍFICOS DEL PANEL DE PÓLIZAS --- */
.polizas-container { background: #eef2f5; padding: 20px; border-radius: 6px; border: 1px solid #c9d3df; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05); }
.topbar-polizas { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.resaltado { color: #d9534f; }
.btn-cerrar-polizas { background: transparent; color: #dc3545; border: 1px solid #dc3545; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 12px; }
.btn-cerrar-polizas:hover { background: #dc3545; color: white; }
.btn-nueva-poliza { background: #28a745; color: white; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; margin-right: 10px; font-size: 12px; }
.btn-nueva-poliza:hover { background: #218838; }
.form-poliza { border-left: 4px solid #17a2b8; }
.form-edicion-poliza { border-left: 4px solid #fd7e14; background: #fff8f3; }
.tabla-polizas th { background-color: #dde4ec; }
/* Píldoras de colores para el estado de la póliza */
.badge-activa { background: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
.badge-inactiva { background: #6c757d; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
.btn-cobros { background: #ffc107; color: #333; border: none; padding: 5px 10px; cursor: pointer; border-radius: 4px; font-size: 12px; font-weight: bold;}
.btn-cobros:hover { background: #e0a800; }

/* --- ESTILOS ESPECÍFICOS DEL MODAL (VENTANA EMERGENTE) DE PAGOS --- */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: white; padding: 25px; border-radius: 8px; width: 800px; max-width: 90%; max-height: 90vh; overflow-y: auto; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
.btn-cerrar-modal { background: none; border: none; font-size: 20px; cursor: pointer; color: #888; }
.btn-cerrar-modal:hover { color: #dc3545; }
.form-pago { border-left: 4px solid #ffc107; background: #fffcf2; }
.form-edicion-pago { border-left: 4px solid #fd7e14; background: #fff8f3; }
.btn-cancelar-pago { margin-bottom: 2px; }
.pago-form .input-group input { width: 110px; }
.tabla-pagos th { background-color: #fdf2cd; }
/* Píldoras de colores semánticos para indicar si debes dinero o no */
.badge-pagado { background: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
.badge-pendiente { background: #ffc107; color: #333; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
.badge-vencido { background: #dc3545; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
</style>