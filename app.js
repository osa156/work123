// AI Safety Learning Hub — Frontend App
let modulesCache = [];
let quizState = null;

async function loadStats() {
  const s = await api('/stats');
  if (!s) return;
  document.getElementById('s-modules').textContent = s.modules;
  document.getElementById('s-lessons').textContent = s.lessons;
  document.getElementById('s-completed').textContent = s.completed;
}

async function loadModules() {
  modulesCache = await api('/modules') || [];
  renderFeatured();
  renderCurriculum();
}

function renderFeatured() {
  document.getElementById('featured').innerHTML = modulesCache.slice(0, 3).map(m => `
    <div class="card">
      <span class="badge accent">${escapeHtml(m.level)}</span>
      <h3 style="margin:10px 0 8px;">${escapeHtml(m.title)}</h3>
      <p style="color:var(--text-muted);font-size:0.9rem;margin-bottom:12px;">${escapeHtml(m.summary)}</p>
      <span class="badge">&#9201; ${escapeHtml(m.duration)}</span>
    </div>`).join('');
}

function renderCurriculum() {
  document.getElementById('module-list').innerHTML = modulesCache.map((m, i) => `
    <div class="card" style="display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap;">
      <div style="background:var(--primary);color:#fff;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0;">${i+1}</div>
      <div style="flex:1;min-width:200px;">
        <h3 style="margin-bottom:6px;">${escapeHtml(m.title)}</h3>
        <p style="color:var(--text-muted);font-size:0.9rem;margin-bottom:12px;">${escapeHtml(m.summary)}</p>
        <span class="badge primary">${escapeHtml(m.level)}</span>
        <span class="badge">&#9201; ${escapeHtml(m.duration)}</span>
        <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
          <button class="btn btn-sm" onclick="openLesson(${m.id})">View Lessons</button>
          <button class="btn btn-outline btn-sm" onclick="startQuiz(${m.id})">Take Quiz</button>
        </div>
      </div>
    </div>`).join('');
}

async function openLesson(mid) {
  const lessons = await api(`/modules/${mid}/lessons`);
  const mod = modulesCache.find(m => m.id === mid);
  document.getElementById('lesson-content').innerHTML = `
    <span class="badge primary">${escapeHtml(mod.level)}</span>
    <h1 style="margin:10px 0 8px;">${escapeHtml(mod.title)}</h1>
    <p style="color:var(--text-muted);margin-bottom:24px;">${escapeHtml(mod.summary)}</p>
    ${(lessons||[]).map((l,i)=>`
      <div class="card"><h3 style="margin-bottom:10px;color:var(--accent);">Lesson ${i+1}: ${escapeHtml(l.title)}</h3>
      <p>${escapeHtml(l.body)}</p></div>`).join('')}
    <div style="text-align:center;margin-top:24px;">
      <button class="btn" style="padding:14px 32px;" onclick="startQuiz(${mid})">Complete Module — Take Quiz</button>
    </div>`;
  showView('lesson');
}

async function startQuiz(mid) {
  const qs = await api(`/modules/${mid}/quiz`);
  if (!qs || !qs.length) { showToast('No quiz available', 'danger'); return; }
  quizState = { mid, qs, idx: 0, score: 0 };
  renderQuestion();
  showView('quiz');
}

function renderQuestion() {
  const { qs, idx } = quizState;
  if (idx >= qs.length) { showQuizResult(); return; }
  const item = qs[idx];
  document.getElementById('quiz-container').innerHTML = `
    <div class="card">
      <span class="badge accent">Question ${idx+1} of ${qs.length}</span>
      <h2 style="margin:12px 0 20px;">${escapeHtml(item.question)}</h2>
      <div style="display:flex;flex-direction:column;gap:10px;" id="q-opts">
        ${item.options.map((o,i)=>`
          <button class="btn btn-outline" style="text-align:left;justify-content:flex-start;" onclick="answerQuiz(${i})">
            <span style="background:var(--border);width:28px;height:28px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:700;margin-right:10px;flex-shrink:0;">${String.fromCharCode(65+i)}</span>
            ${escapeHtml(o)}
          </button>`).join('')}
      </div>
    </div>`;
}

function answerQuiz(i) {
  const item = quizState.qs[quizState.idx];
  const btns = document.querySelectorAll('#q-opts button');
  btns.forEach((b, j) => { b.disabled = true;
    if (j === item.correct_index) b.style.background = 'var(--success)';
    else if (j === i) b.style.background = 'var(--danger)'; });
  if (i === item.correct_index) quizState.score++;
  setTimeout(() => { quizState.idx++; renderQuestion(); }, 1100);
}

async function showQuizResult() {
  const { score, qs, mid } = quizState;
  const pct = Math.round(score / qs.length * 100);
  const passed = pct >= 70;
  if (passed) await api('/progress', { method: 'POST', body: { module_id: mid, score, total: qs.length } });
  document.getElementById('quiz-container').innerHTML = `
    <div class="card" style="text-align:center;padding:40px;">
      <div style="font-size:4rem;margin-bottom:16px;">${passed ? '&#127942;' : '&#128218;'}</div>
      <h2>${passed ? 'Quiz Passed!' : 'Keep Practicing'}</h2>
      <p style="font-size:1.3rem;margin:12px 0;">Score: <strong>${score}/${qs.length}</strong> (${pct}%)</p>
      <p style="color:var(--text-muted);margin-bottom:24px;">${passed ? 'Progress saved to server.' : 'Passing is 70%. Review lessons and retry.'}</p>
      <button class="btn" onclick="showView('curriculum')">Back to Curriculum</button>
      <button class="btn btn-outline" style="margin-left:8px;" onclick="startQuiz(${mid})">Retry</button>
    </div>`;
  loadStats();
}

async function loadProgress() {
  const rows = await api('/progress') || [];
  const el = document.getElementById('progress-list');
  if (!rows.length) { el.innerHTML = '<div class="card" style="text-align:center;"><p style="color:var(--text-muted);">No progress yet.</p></div>'; return; }
  el.innerHTML = rows.map(r => {
    const pct = Math.round(r.score / r.total * 100);
    return `<div class="card" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
      <div><h3 style="margin-bottom:4px;">${escapeHtml(r.module_title)}</h3>
        <span class="badge success">&#10003; Passed</span>
        <span class="badge">${r.score}/${r.total} (${pct}%)</span>
        <span class="badge">${fmtDate(r.completed_at)}</span></div>
      <button class="btn btn-outline btn-sm" onclick="startQuiz(${r.module_id})">Retake</button>
    </div>`; }).join('');
}

function onView(name) {
  if (name === 'curriculum') renderCurriculum();
  if (name === 'progress') loadProgress();
  if (name === 'home') renderFeatured();
}

// Init
loadStats();
loadModules();
