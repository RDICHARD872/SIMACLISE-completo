<template>
  <!-- Contenedor general que centra la ventana de login en medio de la pantalla con un fondo gris clásico -->
  <div class="login-container">
    <div class="login-box">
      
      <!-- SECCIÓN IZQUIERDA: LOGOTIPO Y DESCRIPCIÓN -->
      <div class="logo-section">
        <h1 class="logo-text">SiMaCliSe</h1>
        <p class="subtitle">Sistema de Manejo<br>de Clientes de Seguros</p>
      </div>

      <!-- SECCIÓN DERECHA: FORMULARIO DE ACCESO -->
      <div class="form-section">
        <!-- Campo para escribir el usuario -->
        <div class="input-group">
          <label>Usuario</label>
          <input type="text" v-model="usuario" placeholder="sandra.arenivar" />
        </div>

        <!-- Campo para la contraseña (oculta los caracteres por seguridad) -->
        <div class="input-group">
          <label>Password</label>
          <input type="password" v-model="password" placeholder="******" />
        </div>

        <!-- Casilla estética para recordar la sesión -->
        <div class="checkbox-group">
          <input type="checkbox" id="recordar" />
          <label for="recordar">Recordar Login</label>
        </div>

        <!-- Botones de acción del sistema -->
        <div class="actions">
          <!-- Al hacer clic en OK, disparamos la función 'ingresar' -->
          <button class="btn-ok" @click="ingresar">✔️ OK</button>
          <!-- Botón estético de cancelar (limpia o simula cierre) -->
          <button class="btn-cancel">❌ Cancel</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
// Importamos herramientas de Vue y del enrutador (router)
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Variables reactivas para capturar lo que el usuario escriba en los inputs
const usuario = ref('')
const password = ref('')
const router = useRouter()

// Función que maneja el evento del botón OK
const ingresar = () => {
  // Como estamos simulando el acceso inicial, saltamos directamente al módulo de clientes
  router.push('/clientes')
}
</script>

<style scoped>
/* 
  ESTILOS (CSS)
  - Diseñados para replicar la estética de una ventana de escritorio clásica de Windows.
*/
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #c9d3df;
}

.login-box {
  background: #f0f0f0;
  padding: 30px;
  border-radius: 4px;
  border: 1px solid #999;
  box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
  display: flex;
  gap: 20px;
  width: 450px;
}

.logo-section {
  border-right: 2px solid #ccc;
  padding-right: 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.logo-text { color: #2c6499; margin: 0; font-size: 26px; }
.subtitle { font-size: 11px; color: #555; margin-top: 5px; }

.form-section { flex: 1; display: flex; flex-direction: column; justify-content: center;}
.input-group { margin-bottom: 12px; display: flex; align-items: center;}
.input-group label { width: 70px; font-size: 13px; color: #333;}
.input-group input { flex: 1; padding: 4px; border: 1px solid #aaa; }

.checkbox-group { margin-bottom: 15px; font-size: 13px; margin-left: 70px; }
.actions { display: flex; gap: 15px; margin-left: 70px; }

.btn-ok, .btn-cancel { 
  background: #e0e0e0; 
  border: 1px solid #999; 
  padding: 4px 15px; 
  cursor: pointer; 
  font-size: 13px;
}
.btn-ok:hover, .btn-cancel:hover { background: #d0d0d0; }
</style>