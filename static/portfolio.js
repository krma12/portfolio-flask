// =============================================================
// portfolio.js — interactividad del portfolio
//   1. Idiomas (EN / ES)
//   2. Terminal interactiva (consulta la API real: GET /proyectos)
//   3. Filtros por tecnología
//   4. Vista JSON de los proyectos
// Sin librerías: JavaScript puro.
// =============================================================

(function () {
  "use strict";

  // ---------------------------------------------------------------
  // 1. IDIOMAS
  // Cada texto de la página tiene data-i18n="clave". Aquí están las
  // traducciones; al cambiar de idioma se reemplaza el texto de cada
  // elemento. Las descripciones de proyectos vienen de la base de datos
  // (descripcion / descripcion_es) y se muestran con CSS según <html lang>.
  // ---------------------------------------------------------------
  const TEXTOS = {
    en: {
      "skip": "Skip to content",
      "nav.about": "About", "nav.skills": "Skills", "nav.projects": "Projects", "nav.contact": "Contact", "nav.cta": "Let's talk",
      "hero.eyebrow": "Open to new opportunities",
      "hero.title": "Hi, I'm <span class=\"highlight\">Hugo Maldonado</span> — I build with Python, data and AI.",
      "hero.text": "AI engineering student preparing to specialize in cybersecurity. I learn by building real projects, from web apps to computer vision.",
      "hero.work": "View my work", "hero.contact": "Get in touch",
      "term.hint": "Type a command and press Enter, or use the buttons below.",
      "about.tag": "About me", "about.title": "A little about my story",
      "about.p1": "I'm studying Artificial Intelligence Engineering and building my skills through hands-on projects: a Flask task manager, a Space Invaders clone, a data analysis of crime incidence in Mexico, and a real-time face filter with OpenCV.",
      "about.p2": "My goal is to combine AI with cybersecurity and become a specialist in that field. Right now I'm working through Python for data, then machine learning.",
      "about.p3": "Before code, I studied veterinary medicine, lived in the Mexican Caribbean and New York, opened a restaurant and became a bilingual interpreter.",
      "about.link": "Read the full story in my logbook ↗",
      "stats.projects": "Projects", "stats.tools": "Tools & concepts in my projects", "stats.areas": "Areas: web, data, vision, security",
      "skills.tag": "What I do", "skills.title": "Skills & tools", "skills.sub": "The tools I've used in my projects so far.",
      "sk1.t": "Python & Data", "sk1.p": "Python, NumPy, Pandas and Jupyter for data cleaning and exploratory analysis.",
      "sk2.t": "Computer Vision", "sk2.p": "OpenCV and Mediapipe for real-time face detection and augmented reality filters.",
      "sk3.t": "Web Backend", "sk3.p": "Flask, SQLite and SQLAlchemy, REST APIs and Jinja2 templates, plus object-oriented design.",
      "sk4.t": "Tools & Games", "sk4.p": "Git and GitHub for version control, plus Pygame for game development.",
      "sk5.t": "Cybersecurity", "sk5.p": "Kali Linux and isolated home labs for certification practice, and security-minded APIs.",
      "sk6.t": "Languages", "sk6.p": "Native Spanish and professional English (bilingual interpreter). Learning Portuguese, French, Arabic and German.",
      "projects.tag": "My work", "projects.title": "Featured projects", "projects.sub": "Things I've built, with the code on GitHub.",
      "projects.live": "Live site ↗",
      "projects.empty": "No projects yet — add your first one through the API and it'll show up here automatically.",
      "projects.none": "No projects with this technology yet.",
      "view.cards": "Cards", "filter.all": "All",
      "json.note": "{n} of {total} projects",
      "contact.title": "Let's build something together",
      "contact.sub": "Have a project in mind or just want to say hi? I'd love to hear from you.",
      "contact.email": "Email me", "contact.alt": "or email me directly at",
      "form.name": "Name", "form.email": "Email", "form.message": "Message",
      "form.name_ph": "Your name", "form.message_ph": "What's on your mind?", "form.send": "Send message",
      "footer": "Built with Flask, HTML & CSS.",
      "lang.button": "ES", "lang.label": "Cambiar a español",
    },
    es: {
      "skip": "Saltar al contenido",
      "nav.about": "Sobre mí", "nav.skills": "Habilidades", "nav.projects": "Proyectos", "nav.contact": "Contacto", "nav.cta": "Hablemos",
      "hero.eyebrow": "Abierto a nuevas oportunidades",
      "hero.title": "Hola, soy <span class=\"highlight\">Hugo Maldonado</span> — construyo con Python, datos e IA.",
      "hero.text": "Estudiante de Ingeniería en IA preparándome para especializarme en ciberseguridad. Aprendo construyendo proyectos reales, desde apps web hasta visión por computadora.",
      "hero.work": "Ver mis proyectos", "hero.contact": "Contáctame",
      "term.hint": "Escribe un comando y presiona Enter, o usa los botones de abajo.",
      "about.tag": "Sobre mí", "about.title": "Un poco de mi historia",
      "about.p1": "Estudio Ingeniería en Inteligencia Artificial y desarrollo mis habilidades con proyectos prácticos: un gestor de tareas con Flask, una versión de Space Invaders, un análisis de la incidencia delictiva en México y un filtro facial en tiempo real con OpenCV.",
      "about.p2": "Mi meta es combinar la IA con la ciberseguridad y especializarme en ese campo. Ahora mismo estoy con Python para datos y después sigue machine learning.",
      "about.p3": "Antes del código estudié veterinaria, viví en el Caribe mexicano y en Nueva York, abrí un restaurante y me volví intérprete bilingüe.",
      "about.link": "Lee la historia completa en mi bitácora ↗",
      "stats.projects": "Proyectos", "stats.tools": "Herramientas y conceptos en mis proyectos", "stats.areas": "Áreas: web, datos, visión, seguridad",
      "skills.tag": "Lo que hago", "skills.title": "Habilidades y herramientas", "skills.sub": "Las herramientas que he usado en mis proyectos hasta ahora.",
      "sk1.t": "Python y datos", "sk1.p": "Python, NumPy, Pandas y Jupyter para limpieza de datos y análisis exploratorio.",
      "sk2.t": "Visión por computadora", "sk2.p": "OpenCV y Mediapipe para detección facial en tiempo real y filtros de realidad aumentada.",
      "sk3.t": "Backend web", "sk3.p": "Flask, SQLite y SQLAlchemy, APIs REST y plantillas Jinja2, además de diseño orientado a objetos.",
      "sk4.t": "Herramientas y juegos", "sk4.p": "Git y GitHub para control de versiones, y Pygame para desarrollo de videojuegos.",
      "sk5.t": "Ciberseguridad", "sk5.p": "Kali Linux y laboratorios caseros aislados para practicar rumbo a certificaciones, y APIs diseñadas con seguridad.",
      "sk6.t": "Idiomas", "sk6.p": "Español nativo e inglés profesional (intérprete bilingüe). Aprendiendo portugués, francés, árabe y alemán.",
      "projects.tag": "Mi trabajo", "projects.title": "Proyectos destacados", "projects.sub": "Lo que he construido, con el código en GitHub.",
      "projects.live": "Ver en vivo ↗",
      "projects.empty": "Aún no hay proyectos: agrega el primero desde la API y aparecerá aquí automáticamente.",
      "projects.none": "Todavía no hay proyectos con esta tecnología.",
      "view.cards": "Tarjetas", "filter.all": "Todos",
      "json.note": "{n} de {total} proyectos",
      "contact.title": "Construyamos algo juntos",
      "contact.sub": "¿Tienes un proyecto en mente o solo quieres saludar? Me encantaría saber de ti.",
      "contact.email": "Escríbeme", "contact.alt": "o escríbeme directo a",
      "form.name": "Nombre", "form.email": "Correo", "form.message": "Mensaje",
      "form.name_ph": "Tu nombre", "form.message_ph": "¿Qué tienes en mente?", "form.send": "Enviar mensaje",
      "footer": "Hecho con Flask, HTML y CSS.",
      "lang.button": "EN", "lang.label": "Switch to English",
    },
  };

  // localStorage puede fallar (modo privado, cookies bloqueadas): siempre con try/catch
  function leer(clave) { try { return localStorage.getItem(clave); } catch (e) { return null; } }
  function guardar(clave, valor) { try { localStorage.setItem(clave, valor); } catch (e) {} }

  let idioma = leer("lang") || ((navigator.language || "en").toLowerCase().startsWith("es") ? "es" : "en");
  const t = (clave) => (TEXTOS[idioma] && TEXTOS[idioma][clave]) || TEXTOS.en[clave] || clave;

  function aplicarIdioma(nuevo) {
    idioma = nuevo === "es" ? "es" : "en";
    document.documentElement.lang = idioma;
    document.querySelectorAll("[data-i18n]").forEach((el) => { el.textContent = t(el.dataset.i18n); });
    document.querySelectorAll("[data-i18n-html]").forEach((el) => { el.innerHTML = t(el.dataset.i18nHtml); });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => { el.placeholder = t(el.dataset.i18nPlaceholder); });
    const boton = document.getElementById("langToggle");
    if (boton) { boton.textContent = t("lang.button"); boton.setAttribute("aria-label", t("lang.label")); }
    pintarFiltros();
    if (vistaJson) mostrarJson();
  }

  // ---------------------------------------------------------------
  // 3. FILTROS (se definen antes porque el idioma también los repinta)
  // Cada categoría agrupa varias tecnologías de la base de datos.
  // ---------------------------------------------------------------
  const CATEGORIAS = [
    { id: "python",   en: "Python",          es: "Python",                 incluye: ["python"] },
    { id: "vision",   en: "Computer Vision", es: "Visión por computadora", incluye: ["opencv", "mediapipe"] },
    { id: "web",      en: "Web",             es: "Web",                    incluye: ["flask", "html", "css", "javascript", "rest api", "sqlalchemy", "sqlite", "leaflet"] },
    { id: "data",     en: "Data",            es: "Datos",                  incluye: ["pandas", "numpy", "jupyter"] },
    { id: "security", en: "Security",        es: "Seguridad",              incluye: ["cybersecurity", "kali linux", "networking"] },
    { id: "games",    en: "Games",           es: "Juegos",                 incluye: ["pygame"] },
  ];

  const tarjetas = Array.from(document.querySelectorAll(".project-card"));
  let filtroActivo = "all";

  function tecnologiasDe(tarjeta) { return (tarjeta.dataset.tech || "").split("|").filter(Boolean); }
  function coincide(tarjeta, idCategoria) {
    if (idCategoria === "all") return true;
    const categoria = CATEGORIAS.find((c) => c.id === idCategoria);
    return !!categoria && tecnologiasDe(tarjeta).some((tec) => categoria.incluye.includes(tec));
  }

  function pintarFiltros() {
    const contenedor = document.getElementById("filters");
    if (!contenedor || !tarjetas.length) return;
    const opciones = [{ id: "all", etiqueta: t("filter.all"), total: tarjetas.length }].concat(
      CATEGORIAS.map((c) => ({ id: c.id, etiqueta: c[idioma], total: tarjetas.filter((x) => coincide(x, c.id)).length }))
        .filter((c) => c.total > 0)
    );
    contenedor.innerHTML = "";
    opciones.forEach((op) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "chip";
      b.dataset.filtro = op.id;
      b.setAttribute("aria-pressed", String(op.id === filtroActivo));
      b.innerHTML = `${op.etiqueta}<small>${op.total}</small>`;
      b.addEventListener("click", () => filtrar(op.id));
      contenedor.appendChild(b);
    });
  }

  function filtrar(idCategoria) {
    filtroActivo = idCategoria;
    let visibles = 0;
    tarjetas.forEach((tarjeta) => {
      const mostrar = coincide(tarjeta, idCategoria);
      tarjeta.classList.toggle("oculto", !mostrar);
      if (mostrar) {
        visibles++;
        tarjeta.classList.remove("aparece"); void tarjeta.offsetWidth; tarjeta.classList.add("aparece");
      }
    });
    const grid = document.getElementById("projectsGrid");
    let aviso = grid && grid.querySelector(".empty-filter");
    if (grid && !visibles) {
      if (!aviso) { aviso = document.createElement("p"); aviso.className = "empty-filter"; grid.appendChild(aviso); }
      aviso.textContent = t("projects.none");
    } else if (aviso) { aviso.remove(); }
    document.querySelectorAll("#filters .chip").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.filtro === idCategoria)));
    if (vistaJson) mostrarJson();
  }

  // ---------------------------------------------------------------
  // 4. VISTA JSON: muestra la respuesta real de la API
  // ---------------------------------------------------------------
  let vistaJson = false;
  let cacheProyectos = null;

  async function obtenerProyectos() {
    if (cacheProyectos) return { datos: cacheProyectos, ms: 0, estado: 200 };
    const inicio = performance.now();
    const respuesta = await fetch("/proyectos", { headers: { Accept: "application/json" } });
    const datos = await respuesta.json();
    if (respuesta.ok) cacheProyectos = datos;
    return { datos, ms: Math.round(performance.now() - inicio), estado: respuesta.status };
  }

  function escapar(texto) {
    return String(texto).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Colorea el JSON: claves, textos, números y null
  function resaltar(objeto) {
    return escapar(JSON.stringify(objeto, null, 2)).replace(
      /("(?:\\.|[^"\\])*")(\s*:)?|\b(-?\d+(?:\.\d+)?)\b|\bnull\b/g,
      (m, cadena, dosPuntos, numero) => {
        if (cadena) return dosPuntos ? `<span class="j-key">${cadena}</span>${dosPuntos}` : `<span class="j-str">${cadena}</span>`;
        if (numero) return `<span class="j-num">${numero}</span>`;
        return `<span class="j-null">null</span>`;
      }
    );
  }

  async function mostrarJson() {
    const salida = document.getElementById("jsonOutput");
    const estado = document.getElementById("jsonStatus");
    const nota = document.getElementById("jsonNote");
    try {
      const { datos, ms, estado: codigo } = await obtenerProyectos();
      const ids = new Set(tarjetas.filter((x) => !x.classList.contains("oculto")).map((x) => Number(x.dataset.id)));
      const filtrados = datos.filter((p) => ids.has(p.id));
      salida.innerHTML = resaltar(filtrados);
      estado.textContent = `${codigo} OK${ms ? " · " + ms + " ms" : ""}`;
      nota.textContent = filtroActivo === "all" ? "" : "· " + t("json.note").replace("{n}", filtrados.length).replace("{total}", datos.length);
    } catch (e) {
      salida.textContent = "Error: " + e.message;
      estado.textContent = "";
    }
  }

  function cambiarVista(json) {
    vistaJson = json;
    document.getElementById("jsonPanel").hidden = !json;
    document.getElementById("projectsGrid").hidden = json;
    document.getElementById("viewJson").setAttribute("aria-pressed", String(json));
    document.getElementById("viewCards").setAttribute("aria-pressed", String(!json));
    if (json) mostrarJson();
  }

  const botonJson = document.getElementById("viewJson");
  const botonTarjetas = document.getElementById("viewCards");
  if (botonJson && botonTarjetas) {
    botonJson.addEventListener("click", () => cambiarVista(true));
    botonTarjetas.addEventListener("click", () => cambiarVista(false));
  }

  // ---------------------------------------------------------------
  // 2. TERMINAL INTERACTIVA
  // ---------------------------------------------------------------
  const salida = document.getElementById("termOutput");
  const formulario = document.getElementById("termForm");
  const entrada = document.getElementById("termInput");
  const historial = [];
  let posicionHistorial = 0;
  const sinAnimacion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const MENSAJES = {
    en: {
      bienvenida: "Welcome! Type <span class=\"acc\">help</span> to see what you can do.",
      ayuda: [
        ["whoami", "who I am"],
        ["projects", "list my projects (live from my API)"],
        ["projects --tag <tag>", "filter: python, vision, web, data, security, games"],
        ["skills", "what I work with"],
        ["contact", "how to reach me"],
        ["logbook", "open my story (bitácora)"],
        ["lang es|en", "switch language"],
        ["theme dark|light", "switch theme"],
        ["clear", "clear the screen"],
      ],
      whoami: [
        "<span class=\"acc\">Hugo Maldonado</span> · AI engineering student @ Hybridge",
        "Bilingual interpreter (ES ⇄ EN) · CDMX, Mexico",
        "Building toward <span class=\"pur\">AI + cybersecurity</span>.",
      ],
      cargando: "Fetching GET /proyectos …",
      sinProyectos: "No projects match that tag.",
      tagDesconocido: "Unknown tag. Try: python, vision, web, data, security, games",
      skills: [
        "<span class=\"ok\">python</span>   Python · NumPy · Pandas · Jupyter",
        "<span class=\"ok\">vision</span>   OpenCV · Mediapipe",
        "<span class=\"ok\">web</span>      Flask · SQLAlchemy · REST APIs · HTML/CSS/JS",
        "<span class=\"ok\">security</span> Kali Linux · isolated labs · API keys",
        "<span class=\"ok\">tools</span>    Git · GitHub · Pygame",
        "<span class=\"ok\">langs</span>    Spanish · English · learning PT, FR, AR, DE",
      ],
      contacto: [
        "✉  <a href=\"mailto:sowyer99@hotmail.com\">sowyer99@hotmail.com</a>",
        "in <a href=\"https://www.linkedin.com/in/hugo-maldonado-a20445201\" target=\"_blank\" rel=\"noopener\">linkedin.com/in/hugo-maldonado</a>",
        "gh <a href=\"https://github.com/krma12\" target=\"_blank\" rel=\"noopener\">github.com/krma12</a>",
        "<span class=\"dim\">…or use the form below ↓</span>",
      ],
      bitacora: "Opening my logbook in a new tab…",
      sudo: [
        "<span class=\"warn\">[sudo] password for recruiter:</span> ********",
        "<span class=\"ok\">✓ Access granted.</span> Great choice. Let's talk →",
      ],
      noEncontrado: (c) => `command not found: <span class="err">${c}</span>. Type <span class="acc">help</span>.`,
      tema: (x) => `Theme set to ${x}.`,
      idioma: "Language set to English.",
      verRepo: "repo",
    },
    es: {
      bienvenida: "¡Bienvenido! Escribe <span class=\"acc\">help</span> para ver lo que puedes hacer.",
      ayuda: [
        ["whoami", "quién soy"],
        ["projects", "lista mis proyectos (en vivo desde mi API)"],
        ["projects --tag <tag>", "filtra: python, vision, web, data, security, games"],
        ["skills", "con qué trabajo"],
        ["contact", "cómo contactarme"],
        ["logbook", "abre mi historia (bitácora)"],
        ["lang es|en", "cambia el idioma"],
        ["theme dark|light", "cambia el tema"],
        ["clear", "limpia la pantalla"],
      ],
      whoami: [
        "<span class=\"acc\">Hugo Maldonado</span> · estudiante de Ingeniería en IA @ Hybridge",
        "Intérprete bilingüe (ES ⇄ EN) · CDMX, México",
        "Construyendo mi camino hacia <span class=\"pur\">IA + ciberseguridad</span>.",
      ],
      cargando: "Consultando GET /proyectos …",
      sinProyectos: "Ningún proyecto tiene esa etiqueta.",
      tagDesconocido: "Etiqueta desconocida. Prueba: python, vision, web, data, security, games",
      skills: [
        "<span class=\"ok\">python</span>   Python · NumPy · Pandas · Jupyter",
        "<span class=\"ok\">vision</span>   OpenCV · Mediapipe",
        "<span class=\"ok\">web</span>      Flask · SQLAlchemy · APIs REST · HTML/CSS/JS",
        "<span class=\"ok\">security</span> Kali Linux · laboratorios aislados · API keys",
        "<span class=\"ok\">tools</span>    Git · GitHub · Pygame",
        "<span class=\"ok\">idiomas</span>  Español · inglés · aprendiendo PT, FR, AR, DE",
      ],
      contacto: [
        "✉  <a href=\"mailto:sowyer99@hotmail.com\">sowyer99@hotmail.com</a>",
        "in <a href=\"https://www.linkedin.com/in/hugo-maldonado-a20445201\" target=\"_blank\" rel=\"noopener\">linkedin.com/in/hugo-maldonado</a>",
        "gh <a href=\"https://github.com/krma12\" target=\"_blank\" rel=\"noopener\">github.com/krma12</a>",
        "<span class=\"dim\">…o usa el formulario de abajo ↓</span>",
      ],
      bitacora: "Abriendo mi bitácora en otra pestaña…",
      sudo: [
        "<span class=\"warn\">[sudo] contraseña para reclutador:</span> ********",
        "<span class=\"ok\">✓ Acceso concedido.</span> Excelente decisión. Hablemos →",
      ],
      noEncontrado: (c) => `comando no encontrado: <span class="err">${c}</span>. Escribe <span class="acc">help</span>.`,
      tema: (x) => `Tema cambiado a ${x === "dark" ? "oscuro" : "claro"}.`,
      idioma: "Idioma cambiado a español.",
      verRepo: "repo",
    },
  };
  const m = () => MENSAJES[idioma];

  function linea(html, clase) {
    const div = document.createElement("div");
    div.className = "ln" + (clase ? " " + clase : "");
    div.innerHTML = html;
    salida.appendChild(div);
    salida.scrollTop = salida.scrollHeight;
    return div;
  }
  const lineas = (arr) => arr.forEach((l) => linea(l));

  const COMANDOS = {
    help() {
      m().ayuda.forEach(([cmd, desc]) => linea(`<span class="ok">${escapar(cmd.padEnd(22))}</span><span class="dim">${desc}</span>`));
    },
    whoami() { lineas(m().whoami); },
    skills() { lineas(m().skills); },
    contact() { lineas(m().contacto); },
    clear() { salida.innerHTML = ""; },
    logbook() { linea(m().bitacora, "dim"); window.open("https://krma12.github.io/mi-bitacora/", "_blank", "noopener"); },
    async projects(args) {
      let etiqueta = null;
      const i = args.indexOf("--tag");
      if (i !== -1) etiqueta = (args[i + 1] || "").toLowerCase();
      if (etiqueta && !CATEGORIAS.some((c) => c.id === etiqueta)) { linea(m().tagDesconocido, "warn"); return; }
      linea(m().cargando, "dim");
      try {
        const { datos, ms, estado } = await obtenerProyectos();
        linea(`<span class="ok">${estado} OK</span><span class="dim">${ms ? " · " + ms + " ms" : " · cached"}</span>`);
        const categoria = CATEGORIAS.find((c) => c.id === etiqueta);
        const lista = datos.filter((p) => !categoria || (p.tecnologias || []).some((tec) => categoria.incluye.includes(tec.toLowerCase())));
        if (!lista.length) { linea(m().sinProyectos, "warn"); return; }
        lista.forEach((p) => {
          const tecs = (p.tecnologias || []).join(", ");
          linea(`${p.emoji || "•"} <span class="acc">${escapar(p.titulo)}</span> <span class="dim">— ${escapar(tecs)}</span> <a href="${encodeURI(p.repo_url || "#")}" target="_blank" rel="noopener">${m().verRepo}</a>`);
        });
        if (categoria) filtrar(categoria.id);
      } catch (e) {
        linea("Error: " + escapar(e.message), "err");
      }
    },
    lang(args) {
      const nuevo = args[0] === "es" ? "es" : args[0] === "en" ? "en" : (idioma === "es" ? "en" : "es");
      guardar("lang", nuevo);
      aplicarIdioma(nuevo);
      linea(m().idioma, "ok");
    },
    theme(args) {
      const tema = args[0] === "light" ? "light" : "dark";
      if (window.portfolioTheme) window.portfolioTheme(tema);
      linea(m().tema(tema), "ok");
    },
    sudo(args) {
      if (args.join(" ") === "hire-hugo") {
        lineas(m().sudo);
        setTimeout(() => document.getElementById("contact").scrollIntoView({ behavior: sinAnimacion ? "auto" : "smooth" }), 900);
      } else {
        linea("sudo: " + escapar(args.join(" ") || "") + " — nice try 😉", "warn");
      }
    },
  };
  // Alias útiles
  COMANDOS.ls = COMANDOS.projects;
  COMANDOS.cls = COMANDOS.clear;

  async function ejecutar(textoComando) {
    const limpio = textoComando.trim();
    if (!limpio) return;
    linea(escapar(limpio), "cmd");
    historial.push(limpio);
    posicionHistorial = historial.length;
    const [nombre, ...args] = limpio.split(/\s+/);
    const comando = COMANDOS[nombre.toLowerCase()];
    if (comando) await comando(args);
    else linea(m().noEncontrado(escapar(nombre)));
  }

  // Escribe un comando letra por letra (para la demo inicial y los botones)
  function escribirYEjecutar(texto) {
    if (sinAnimacion) { ejecutar(texto); return Promise.resolve(); }
    return new Promise((resolver) => {
      let i = 0;
      entrada.value = "";
      const intervalo = setInterval(() => {
        entrada.value = texto.slice(0, ++i);
        if (i >= texto.length) {
          clearInterval(intervalo);
          setTimeout(async () => { entrada.value = ""; await ejecutar(texto); resolver(); }, 180);
        }
      }, 45);
    });
  }

  if (salida && formulario && entrada) {
    formulario.addEventListener("submit", (e) => {
      e.preventDefault();
      const texto = entrada.value;
      entrada.value = "";
      ejecutar(texto);
    });

    // Flechas = historial · Tab = autocompletar
    entrada.addEventListener("keydown", (e) => {
      if (e.key === "ArrowUp" && historial.length) {
        e.preventDefault();
        posicionHistorial = Math.max(0, posicionHistorial - 1);
        entrada.value = historial[posicionHistorial];
      } else if (e.key === "ArrowDown" && historial.length) {
        e.preventDefault();
        posicionHistorial = Math.min(historial.length, posicionHistorial + 1);
        entrada.value = historial[posicionHistorial] || "";
      } else if (e.key === "Tab" && entrada.value) {
        const opcion = Object.keys(COMANDOS).find((c) => c.startsWith(entrada.value.toLowerCase()));
        if (opcion) { e.preventDefault(); entrada.value = opcion + " "; }
      }
    });

    // Clic en la terminal = enfocar el campo (sin robar el foco al seleccionar texto o links)
    document.getElementById("terminal").addEventListener("click", (e) => {
      if (e.target.tagName !== "A" && !window.getSelection().toString()) entrada.focus({ preventScroll: true });
    });

    document.querySelectorAll(".term-chips [data-cmd]").forEach((boton) =>
      boton.addEventListener("click", () => escribirYEjecutar(boton.dataset.cmd))
    );
  }

  // ---------------------------------------------------------------
  // Arranque
  // ---------------------------------------------------------------
  const botonIdioma = document.getElementById("langToggle");
  if (botonIdioma) {
    botonIdioma.addEventListener("click", () => {
      const nuevo = idioma === "es" ? "en" : "es";
      guardar("lang", nuevo);
      aplicarIdioma(nuevo);
    });
  }

  aplicarIdioma(idioma);

  if (salida) {
    linea(m().bienvenida, "dim");
    // Pequeña demo al cargar: escribe "whoami" solo
    setTimeout(() => escribirYEjecutar("whoami"), sinAnimacion ? 0 : 600);
  }
})();
