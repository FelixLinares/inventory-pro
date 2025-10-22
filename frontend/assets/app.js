// frontend/assets/app.js

// Clave donde guardamos la URL base de la API
const API = (localStorage.getItem('api_base') || '').replace(/\/+$/, '');

function $(id) { return document.getElementById(id); }
function msg(t) { alert(t); }

document.addEventListener('DOMContentLoaded', () => {
  // ---- set-api.html ----
  const apiInput = $('apiBase');
  const saveApiBtn = $('saveApi');

  if (apiInput && saveApiBtn) {
    if (API) apiInput.value = API;

    saveApiBtn.addEventListener('click', () => {
      const url = (apiInput.value || '').trim().replace(/\/+$/, '');
      if (!/^https?:\/\//i.test(url)) {
        msg('URL inválida. Debe empezar por http:// o https://');
        return;
      }
      localStorage.setItem('api_base', url);
      msg('Guardado. Ahora ve a login.');
    });
  }

  // ---- register.html ----
  const regBtn   = $('registerBtn');
  const regName  = $('adminName');
  const regEmail = $('adminEmail');
  const regPass  = $('adminPass');

  if (regBtn && regName && regEmail && regPass) {
    regBtn.addEventListener('click', async () => {
      try {
        if (!localStorage.getItem('api_base')) {
          msg('Primero configura la API en set-api.html'); return;
        }
        const name = (regName.value  || '').trim();
        const email = (regEmail.value || '').trim();
        const password = regPass.value || '';

        if (!name || !email || !password) {
          msg('Completa todos los campos'); return;
        }

        const res = await fetch(`${API}/auth/register-admin`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, email, password })
        });

        const data = await res.json().catch(() => ({}));

        if (res.ok) {
          msg('Admin creado (o ya existía). Sigue con el login.');
          window.location.href = 'login.html';
        } else {
          msg(data.detail || 'Error al registrar admin');
        }
      } catch (e) {
        console.error(e);
        msg('Error de red/JS al registrar');
      }
    });
  }

  // ---- login.html ----
  const loginBtn   = $('loginBtn');
  const loginEmail = $('loginEmail');
  const loginPass  = $('loginPass');

  if (loginBtn && loginEmail && loginPass) {
    loginBtn.addEventListener('click', async () => {
      try {
        if (!localStorage.getItem('api_base')) {
          msg('Primero configura la API en set-api.html'); return;
        }

        const email = (loginEmail.value || '').trim();
        const password = loginPass.value || '';

        if (!email || !password) {
          msg('Completa email y contraseña'); return;
        }

        const res = await fetch(`${API}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        const data = await res.json().catch(() => ({}));

        // Ajusta aquí si tu API devuelve otra forma distinta
        if (res.ok && (data.access_token || data.ok)) {
          if (data.access_token) localStorage.setItem('token', data.access_token);
          msg('Login correcto');
          // TODO: Redirige al dashboard si ya lo tienes
          // window.location.href = 'dashboard.html';
        } else {
          msg(data.detail || 'Credenciales incorrectas');
        }
      } catch (e) {
        console.error(e);
        msg('Error de red/JS al iniciar sesión');
      }
    });
  }
});
