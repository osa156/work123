// API Client & UI Helpers
const API = '/api';
async function api(endpoint, options = {}) {
  try {
    const res = await fetch(API + endpoint, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
      body: options.body ? JSON.stringify(options.body) : undefined
    });
    if (!res.ok) throw new Error('API error: ' + res.status);
    return await res.json();
  } catch (err) {
    console.error(err);
    showToast('Connection error — is the backend running? (python run.py)', 'danger');
    return null;
  }
}
function showToast(msg, type = 'success') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.style.borderColor = type === 'danger' ? 'var(--danger)' : 'var(--success)';
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}
function showView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  const el = document.getElementById('view-' + name);
  if (el) el.classList.add('active');
  const navBtn = document.getElementById('nav-' + name);
  if (navBtn) navBtn.classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (typeof onView === 'function') onView(name);
}
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str || '';
  return div.innerHTML;
}
function fmtDate(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}
function closeModal() { document.getElementById('modal').classList.remove('show'); }
