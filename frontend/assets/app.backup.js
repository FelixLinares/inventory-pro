const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const API_BASE=()=>localStorage.getItem("API_BASE")||""; let TOKEN=localStorage.getItem("TOKEN")||"";

async function fetchRetry(url,opts={},retries=3,delay=800){
  try{ const r=await fetch(url,opts); if(!r.ok) throw new Error("HTTP "+r.status); return r }
  catch(e){ if(retries<=0) throw e; await new Promise(res=>setTimeout(res,delay)); return fetchRetry(url,opts,retries-1,delay*1.5) }
}
function authHeaders(){ const h={"Content-Type":"application/json"}; if(TOKEN) h.Authorization="Bearer "+TOKEN; return h }
async function api(path,method="GET",body=null){
  const r=await fetchRetry(API_BASE()+path,{method,headers:authHeaders(),body:body?JSON.stringify(body):null}); return r.json();
}
function ensureApiSet(){ if(!API_BASE()){ location.href="set-api.html"; return false } return true }
function setSessionInfo(u){ localStorage.setItem("USER",JSON.stringify(u)); $("#session-email")?.replaceChildren(document.createTextNode(u.email)) }

async function handleLogin(){
  if(!ensureApiSet()) return; const email=$("#email").value.trim(), password=$("#password").value.trim();
  const res=await api("/auth/login","POST",{name:"",email,password}); TOKEN=res.access_token; localStorage.setItem("TOKEN",TOKEN);
  const me=await api("/me"); setSessionInfo(me); location.href="dashboard.html";
}
async function handleRegister(){
  if(!ensureApiSet()) return; const name=$("#name").value.trim(), email=$("#email").value.trim(), password=$("#password").value.trim();
  await api("/auth/register","POST",{name,email,password}); alert("Usuario admin creado. Ahora inicia sesión."); location.href="login.html";
}

const views={
  products: async ()=>{
    const data=await api("/api/products");
    const rows=data.map(p=>`<tr><td>${p.id}</td><td>${p.code}</td><td>${p.name}</td><td>${p.category_id??""}</td><td>${p.min_stock}</td></tr>`).join("");
    $("#view").innerHTML=`<div class="card"><h2>Productos</h2>
      <table class="table"><thead><tr><th>ID</th><th>Código</th><th>Nombre</th><th>Categoría</th><th>Stock mínimo</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  },
  warehouses: async ()=>{
    const data=await api("/api/warehouses");
    const rows=data.map(w=>`<tr><td>${w.id}</td><td>${w.name}</td></tr>`).join("");
    $("#view").innerHTML=`<div class="card"><h2>Bodegas</h2>
      <table class="table"><thead><tr><th>ID</th><th>Nombre</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  },
  movements: async ()=>{
    $("#view").innerHTML=`<div class="card"><h2>Movimientos</h2>
      <div class="row">
        <div class="col"><input id="m_product" placeholder="ID producto"></div>
        <div class="col"><input id="m_warehouse" placeholder="ID bodega"></div>
        <div class="col"><select id="m_type"><option value="in">Entrada</option><option value="out">Salida</option></select></div>
        <div class="col"><input id="m_qty" type="number" placeholder="Cantidad"></div>
        <div class="col"><input id="m_note" placeholder="Nota"></div>
        <div class="col"><button id="m_save">Registrar</button></div>
      </div>
      <div class="notice">Este MVP registra y afecta stock. El listado de movimientos se ampliará.</div>
    </div>`;
    $("#m_save").onclick=async ()=>{
      const body={product_id:+$("#m_product").value, warehouse_id:+$("#m_warehouse").value, type:$("#m_type").value, qty:+$("#m_qty").value, note:$("#m_note").value};
      await api("/api/movements","POST",body); alert("Movimiento registrado");
    }
  },
  reports: async ()=>{
    const data=await api("/api/reports/stock_matrix"); const whSet=new Set(); data.forEach(r=>Object.keys(r.by_warehouse).forEach(k=>whSet.add(k)));
    const headers=[...whSet].sort(); const head=`<tr><th>ID</th><th>Código</th><th>Nombre</th>${headers.map(h=>`<th>${h}</th>`).join("")}<th>Total</th></tr>`;
    const rows=data.map(r=>`<tr><td>${r.product_id}</td><td>${r.code}</td><td>${r.name}</td>${headers.map(h=>`<td>${r.by_warehouse[h]??0}</td>`).join("")}<td><span class="badge">${r.total}</span></td></tr>`).join("");
    $("#view").innerHTML=`<div class="card"><h2>Reporte de existencias</h2>
      <div class="row">
        <div class="col"><a class="badge" href="${API_BASE()}/api/export/stock.csv" target="_blank">Descargar CSV</a></div>
        <div class="col"><a class="badge" href="${API_BASE()}/api/export/stock.xlsx" target="_blank">Descargar Excel</a></div>
      </div>
      <table class="table"><thead>${head}</thead><tbody>${rows}</tbody></table></div>`;
  },
  admin: async ()=>{
    $("#view").innerHTML=`<div class="card"><h2>Administración</h2>
      <p class="kicker">Crear usuarios, reset de contraseña.</p>
      <div class="row">
        <div class="col"><input id="a_name" placeholder="Nombre"></div>
        <div class="col"><input id="a_email" placeholder="Email"></div>
        <div class="col"><input id="a_pass" type="password" placeholder="Contraseña"></div>
        <div class="col">
          <select id="a_admin"><option value="false">Usuario</option><option value="true">Admin</option></select>
        </div>
        <div class="col"><button id="a_create">Crear</button></div>
      </div>
      <div class="notice">Importar existencias: sube un Excel con columnas: <b>code</b>, <b>warehouse</b>, <b>qty</b>.</div>
      <input type="file" id="imp" accept=".xlsx"/>
      <div class="footer">Solo el primer registro abierto. Luego, solo admin crea usuarios.</div>
    </div>`;
    $("#a_create").onclick=async ()=>{
      const body={name:$("#a_name").value,email:$("#a_email").value,password:$("#a_pass").value,is_admin:$("#a_admin").value==="true"};
      await api("/api/admin/users","POST",body); alert("Usuario creado");
    };
    $("#imp").onchange=async (e)=>{
      const f=e.target.files[0]; if(!f) return;
      const fd=new FormData(); fd.append("file",f);
      const r=await fetchRetry(API_BASE()+"/api/import/stock",{method:"POST",body:fd,headers:{Authorization:"Bearer "+TOKEN}});
      alert("Importado");
    };
  }
};
function mountDashboard(){
  if(!ensureApiSet()) return; if(!localStorage.getItem("TOKEN")){ location.href="login.html"; return }
  const links=$$(".sidebar a"); links.forEach(a=>a.onclick=e=>{ e.preventDefault(); links.forEach(x=>x.classList.remove("active")); a.classList.add("active"); const view=a.dataset.view; if(views[view]) views[view]() });
  const first=links[0]; if(first) first.click();
}
window.__app={ handleLogin, handleRegister, mountDashboard };
