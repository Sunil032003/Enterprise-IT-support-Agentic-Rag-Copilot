const chat = document.getElementById('chat');
const form = document.getElementById('chatForm');
const question = document.getElementById('question');
const trace = document.getElementById('trace');
const sourceUsed = document.getElementById('sourceUsed');

function escapeHtml(s = '') {
  return String(s).replace(
    /[&<>'"]/g,
    (c) =>
      ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;',
      })[c]
  );
}

function formatText(s = '') {
  return escapeHtml(s).replace(/\n/g, '<br>');
}

function addMessage(role, text, source = '', citations = []) {
  const wrap = document.createElement('div');
  wrap.className = `message ${role}`;

  let citeHtml = '';
  if (citations && citations.length > 0) {
    const listHtml = citations
      .map((c) => {
        if (!c) return '';
        if (typeof c === 'string') return escapeHtml(c);
        if (c.url) {
          return `<a href="${escapeHtml(c.url)}" target="_blank" rel="noopener">${escapeHtml(c.title || c.url)}</a>`;
        }
        return escapeHtml(c.title || c.source || String(c));
      })
      .filter(Boolean)
      .join('<br>');

    if (listHtml) {
      citeHtml = `<div class="citations"><strong>Sources</strong><br>${listHtml}</div>`;
    }
  }

  wrap.innerHTML = `<div class="avatar">AI</div><div class="bubble">${formatText(text)}${source ? `<div class="answer-source">Source: ${escapeHtml(source)}</div>` : ''}${citeHtml}</div>`;
  chat.appendChild(wrap);
  chat.scrollTop = chat.scrollHeight;
}

function renderTrace(items = []) {
  trace.innerHTML =
    items && items.length
      ? items.map((x) => `<div class="trace-item">${escapeHtml(x)}</div>`).join('')
      : '<div class="empty">No trace.</div>';
}

async function askAgent(q) {
  addMessage('user', q);
  question.value = '';
  renderTrace(['Running LangGraph workflow...']);
  sourceUsed.textContent = 'Running';
  const btn = form.querySelector('button');
  btn.disabled = true;
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Request failed');
    addMessage('assistant', data.answer, data.source_used, data.citations || []);
    renderTrace(data.trace || []);
    sourceUsed.textContent = data.source_used || '—';
  } catch (e) {
    addMessage('assistant', `Error: ${e.message}`);
    renderTrace(['Request failed']);
    sourceUsed.textContent = 'Error';
  } finally {
    btn.disabled = false;
  }
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const q = question.value.trim();
  if (q) askAgent(q);
});

question.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    const q = question.value.trim();
    if (q) askAgent(q);
  }
});

document.querySelectorAll('.example').forEach((b) =>
  b.addEventListener('click', () => askAgent(b.textContent.trim()))
);

const modal = document.getElementById('uploadModal');
const openUpload = document.getElementById('openUpload');
const closeUpload = document.getElementById('closeUpload');
if (openUpload) openUpload.onclick = () => modal.classList.remove('hidden');
if (closeUpload) closeUpload.onclick = () => modal.classList.add('hidden');

const uploadBtn = document.getElementById('uploadBtn');
if (uploadBtn) {
  uploadBtn.onclick = async () => {
    const file = document.getElementById('fileInput').files[0];
    const key = document.getElementById('adminKey').value.trim() || 'change me';
    const status = document.getElementById('uploadStatus');
    if (!file) {
      status.textContent = 'Choose a file first.';
      return;
    }
    status.textContent = 'Indexing document...';
    const fd = new FormData();
    fd.append('file', file);
    try {
      const r = await fetch('/api/ingest', {
        method: 'POST',
        headers: { 'X-Admin-Key': key },
        body: fd
      });
      const d = await r.json();
      if (!r.ok) throw new Error(d.detail || 'Upload failed');
      status.textContent = d.chunks !== undefined
        ? `Indexed ${d.file || file.name}: ${d.chunks} chunks.`
        : (d.message || 'Successfully indexed document.');
    } catch (e) {
      status.textContent = `Error: ${e.message}`;
    }
  };
}
