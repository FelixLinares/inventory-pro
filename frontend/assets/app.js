(function(){
  function $(sel){ return document.querySelector(sel); }
  function pick(ids){ for(const id of ids){ const el=document.getElementById(id); if(el) return el; } return null; }
  function toast(msg){ alert(msg); }

  function getApiBase(){
    const b = localStorage.getItem("api_base") || "";
    return (b || "").replace(/\/+$/,"");
  }

  async function postJSON(url, data){
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    const txt = await r.text();
    let json = {};
    try{ json = txt ? JSON.parse(txt) : {}; } catch(e){ json = { raw: txt }; }
    if(!r.ok){ const detail = json?.detail || r.statusText || "Error"; throw new Error(`${r.status} ${detail}`); }
    return json;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const base = getApiBase();

    // ------- set-api.html -------
    const apiInput = pick(["apiBase","api_base","apiURL"]);
    const saveApiBtn = $("#saveApi") || document.querySelector('[data-action="save-api"]');
    if(apiInput && saveApiBtn){
      if(!apiInput.value && base) apiInput.value = base;
      saveApiBtn.addEventListener("click", (e)=>{
        e.preventDefault();
        const v = (apiInput.value||"").trim().replace(/\/+$/,"");
        if(!v.startsWith("http")){ toast("Coloca una URL válida (http/https)"); return; }
        localStorage.setItem("api_base", v);
        toast("API guardada: " + v);
      });
    }

    // ------- register.html -------
    const regBtn = $("#registerBtn") || document.querySelector('[data-action="register-admin"]');
    if(regBtn){
      const nameEl = pick(["adminName","name","regName"]);
      const emailEl= pick(["adminEmail","email","regEmail"]);
      const passEl = pick(["adminPass","password","regPassword"]);
      regBtn.addEventListener("click", async (e)=>{
        e.preventDefault();
        if(!getApiBase()){ toast("Primero guarda la URL de la API en /set-api.html"); return; }
        if(!nameEl || !emailEl || !passEl){ toast("No encuentro los campos del formulario."); return; }
        const payload = { name: nameEl.value.trim(), email: emailEl.value.trim(), password: passEl.value };
        if(!payload.name || !payload.email || !payload.password){ toast("Completa nombre, email y contraseña."); return; }
        regBtn.disabled = true; const old = regBtn.textContent; regBtn.textContent = "Guardando...";
        try{
          const out = await postJSON(getApiBase()+"/auth/register-admin", payload);
          toast("Administrador creado. Ahora inicia sesión.");
          window.location.href = "login.html";
        }catch(err){
          toast("No se pudo registrar: " + err.message + "\n(¿Ya existe un usuario? Entonces usa Iniciar sesión.)");
        }finally{
          regBtn.disabled = false; regBtn.textContent = old;
        }
      });
    }

    // ------- login.html -------
    const loginBtn = $("#loginBtn") || document.querySelector('[data-action="login"]');
    if(loginBtn){
      const emailEl= pick(["loginEmail","email"]);
      const passEl = pick(["loginPass","password"]);
      loginBtn.addEventListener("click", async (e)=>{
        e.preventDefault();
        if(!getApiBase()){ toast("Primero guarda la URL de la API en /set-api.html"); return; }
        if(!emailEl || !passEl){ toast("No encuentro los campos de login."); return; }
        const payload = { email: emailEl.value.trim(), password: passEl.value };
        loginBtn.disabled = true; const old = loginBtn.textContent; loginBtn.textContent = "Ingresando...";
        try{
          const out = await postJSON(getApiBase()+"/auth/login", payload);
          localStorage.setItem("token", out.access_token);
          toast("Ingreso correcto.");
          window.location.href = "dashboard.html";
        }catch(err){
          toast("No se pudo iniciar sesión: " + err.message);
        }finally{
          loginBtn.disabled = false; loginBtn.textContent = old;
        }
      });
    }
  });
})();
