const API_BASE = '';

function $(sel) { return document.querySelector(sel); }
function $all(sel) { return Array.from(document.querySelectorAll(sel)); }

function saveToken(token) { localStorage.setItem('token', token); }
function getToken() { return localStorage.getItem('token'); }
function authHeaders() { const t = getToken(); return t ? { 'Authorization': `Bearer ${t}` } : {}; }

async function signup(email, password, role, name) {
  const r = await fetch(`${API_BASE}/api/auth/signup`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password, role, name }) });
  if (!r.ok) throw new Error('Signup failed');
  return await r.json();
}

async function login(email, password) {
  const r = await fetch(`${API_BASE}/api/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
  if (!r.ok) throw new Error('Login failed');
  const data = await r.json();
  saveToken(data.access_token);
  return data;
}

async function listPhotographers(params = {}) {
  const usp = new URLSearchParams(params);
  const r = await fetch(`${API_BASE}/api/photographers/?${usp.toString()}`);
  return await r.json();
}

async function addFavorite(userId, photographerId) {
  const r = await fetch(`${API_BASE}/api/favorites/add?user_id=${userId}&photographer_id=${photographerId}`, { method: 'POST', headers: { ...authHeaders() } });
  return await r.json();
}

async function translateText(text, target='en') {
  const r = await fetch(`${API_BASE}/api/chat/translate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text, target }) });
  return await r.json();
}

function getUserIdFromToken() {
  const t = getToken();
  if (!t) return null;
  try {
    const payload = JSON.parse(atob(t.split('.')[1]));
    return payload.sub ? parseInt(payload.sub, 10) : null;
  } catch { return null; }
}
