// =========================================================
// Menú del celular, tema claro/oscuro y foto de perfil.
// Vive en un archivo aparte (y no dentro del HTML) para que la política
// de seguridad CSP pueda bloquear cualquier script escrito en la página.
// =========================================================

// ---- Si la foto no carga, muestra las iniciales ----
(function () {
  const foto = document.getElementById("avatarFoto");
  if (!foto) return;
  const mostrarIniciales = () => {
    foto.style.display = "none";
    if (foto.nextElementSibling) foto.nextElementSibling.style.display = "flex";
  };
  if (foto.complete && foto.naturalWidth === 0) mostrarIniciales();
  foto.addEventListener("error", mostrarIniciales);
})();

// ---- Mobile menu toggle ----
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

menuToggle.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', isOpen);
  menuToggle.textContent = isOpen ? '✕' : '☰';
});

navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', false);
    menuToggle.textContent = '☰';
  });
});

// ---- Light / dark theme toggle ----
const root = document.documentElement;
const themeToggle = document.getElementById('themeToggle');

function applyTheme(theme){
  if(theme === 'dark'){
    root.setAttribute('data-theme', 'dark');
    themeToggle.textContent = '☀️';
  } else {
    root.removeAttribute('data-theme');
    themeToggle.textContent = '🌙';
  }
}

// localStorage puede fallar (modo privado, cookies bloqueadas): lo protegemos con try/catch
let storedTheme = null;
try { storedTheme = localStorage.getItem('theme'); } catch (e) {}
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
applyTheme(storedTheme || (prefersDark ? 'dark' : 'light'));

themeToggle.addEventListener('click', () => {
  const isDark = root.getAttribute('data-theme') === 'dark';
  const next = isDark ? 'light' : 'dark';
  applyTheme(next);
  try { localStorage.setItem('theme', next); } catch (e) {}
});

// La terminal (portfolio.js) usa esta función para el comando "theme dark|light"
window.portfolioTheme = (tema) => {
  applyTheme(tema);
  try { localStorage.setItem('theme', tema); } catch (e) {}
};
