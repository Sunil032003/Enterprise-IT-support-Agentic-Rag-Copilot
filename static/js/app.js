/**
 * Enterprise IT Support Agentic RAG Copilot
 * Frontend Controller matching 3-Column Inspector Design
 */

(function () {
  'use strict';

  // State
  const state = {
    isSending: false,
    adminKey: localStorage.getItem('it_admin_key') || 'change me',
    selectedFile: null,
    messages: []
  };

  // Elements
  const el = {
    chatScrollArea: document.getElementById('chatScrollArea'),
    queryTextInput: document.getElementById('queryTextInput'),
    btnSendQuery: document.getElementById('btnSendQuery'),
    btnUploadClip: document.getElementById('btnUploadClip'),
    // Sidebar Vector Upload Elements
    sidebarAdminKey: document.getElementById('sidebarAdminKey'),
    sidebarFileInput: document.getElementById('sidebarFileInput'),
    sidebarFileBox: document.getElementById('sidebarFileBox'),
    sidebarSelectedFileName: document.getElementById('sidebarSelectedFileName'),
    sidebarUploadBtn: document.getElementById('sidebarUploadBtn'),
    sidebarUploadStatus: document.getElementById('sidebarUploadStatus'),
    // Right Inspector
    sourceUsedDisplay: document.getElementById('sourceUsedDisplay'),
    sourceUsedText: document.getElementById('sourceUsedText'),
    citationsContainer: document.getElementById('citationsContainer'),
    citationTitle: document.getElementById('citationTitle'),
    citationSnippet: document.getElementById('citationSnippet'),
    workflowTimelineContainer: document.getElementById('workflowTimelineContainer')
  };

  // Sample initial message matching user reference screenshot
  const initialConversation = [
    {
      role: 'user',
      text: 'What is the eligibility criteria in clinical research?',
      time: '10:15 AM'
    },
    {
      role: 'assistant',
      text: `In clinical research, **eligibility criteria** are the set of requirements or standards that a person must meet to participate in a clinical study or trial.

They are divided into two main categories:
1. **Inclusion criteria**: The specific characteristics, conditions, or factors a participant must have to qualify (such as a specific age range, gender, particular disease, stage of a condition, or general health status).
2. **Exclusion criteria**: The factors or conditions that disqualify or prevent a person from participating (such as pre-existing medical conditions, concurrent medications that might interfere with the trial, or health risks that could make participation unsafe).

### Why Eligibility Criteria Are Used:
* **Ensuring Participant Safety**: They protect participants by excluding individuals who might be at high risk of adverse reactions or complications from the study intervention.
* **Improving Data Integrity and Validity**: By selecting a well-defined group of participants, researchers can be confident that the study results are caused by the treatment being tested rather than unrelated health factors.
* **Targeting the Right Population**: They help ensure that the findings apply to the patient population intended to benefit from the therapy.
* **Ethical and Regulatory Compliance**: Regulatory bodies (such as the FDA or EMA) require clear, scientifically justified criteria to ensure trials are conducted ethically and produce reliable evidence.`,
      time: '10:15 AM',
      source_used: 'Web Search (Tavily)',
      citations: [
        {
          title: 'Tavily Web Search',
          snippet: 'General information on clinical research eligibility criteria'
        }
      ],
      trace: [
        { title: 'Routed to: kb', time: '10:15 AM', desc: 'Classified as knowledge base query', color: 'blue' },
        { title: 'Retrieved 3 docs from Pinecone KB', time: '10:15 AM', desc: 'Fetched relevant documents', color: 'green' },
        { title: 'KB Evidence Graded: weak', time: '10:15 AM', desc: 'KB documents did not fully answer', color: 'amber' },
        { title: 'Performed Tavily web search', time: '10:15 AM', desc: 'Searched the web for additional context', color: 'blue' },
        { title: 'Web Evidence Graded: good', time: '10:15 AM', desc: 'Web results are relevant', color: 'green' },
        { title: 'Generated Answer', time: '10:15 AM', desc: 'Final answer based on web results', color: 'green' }
      ]
    }
  ];

  function init() {
    if (el.sidebarAdminKey) {
      el.sidebarAdminKey.value = state.adminKey;
    }

    // Load initial conversation
    state.messages = initialConversation;
    renderAllMessages();

    // Set initial right panel to the latest assistant message
    const lastBotMsg = state.messages.filter(m => m.role === 'assistant').slice(-1)[0];
    if (lastBotMsg) {
      updateRightInspector(lastBotMsg);
    }

    setupEvents();
  }

  // ==========================================================================
  // Render Messages
  // ==========================================================================
  function renderAllMessages() {
    el.chatScrollArea.innerHTML = '';
    state.messages.forEach(msg => appendMessageElement(msg));
    scrollToBottom();
  }

  function appendMessageElement(msg) {
    const row = document.createElement('div');
    row.className = `chat-bubble-row ${msg.role}`;

    if (msg.role === 'user') {
      row.innerHTML = `
        <div class="user-bubble-wrapper">
          <div>
            <div class="user-message-bubble">${escapeHtml(msg.text)}</div>
            <div class="message-time-sub">${msg.time}</div>
          </div>
          <div class="user-mini-avatar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
        </div>
      `;
    } else {
      row.innerHTML = `
        <div class="assistant-bubble-wrapper">
          <div class="assistant-mini-avatar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"/>
              <rect x="4" y="8" width="16" height="12" rx="2"/>
              <path d="M9 13v2"/><path d="M15 13v2"/>
            </svg>
          </div>
          <div class="assistant-message-container">
            <div class="assistant-message-content">
              ${formatMarkdown(msg.text)}
            </div>
            <div class="message-time-sub" style="text-align:left;">${msg.time}</div>
          </div>
        </div>
      `;
    }

    el.chatScrollArea.appendChild(row);
  }

  function showTypingIndicator() {
    const typingRow = document.createElement('div');
    typingRow.className = 'chat-bubble-row assistant';
    typingRow.id = 'typingIndicatorRow';
    typingRow.innerHTML = `
      <div class="assistant-bubble-wrapper">
        <div class="assistant-mini-avatar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"/>
            <rect x="4" y="8" width="16" height="12" rx="2"/>
            <path d="M9 13v2"/><path d="M15 13v2"/>
          </svg>
        </div>
        <div class="assistant-message-container">
          <div class="typing-dots-row">
            <div class="t-dot"></div>
            <div class="t-dot"></div>
            <div class="t-dot"></div>
          </div>
        </div>
      </div>
    `;
    el.chatScrollArea.appendChild(typingRow);
    scrollToBottom();
  }

  function hideTypingIndicator() {
    const row = document.getElementById('typingIndicatorRow');
    if (row) row.remove();
  }

  function scrollToBottom() {
    el.chatScrollArea.scrollTop = el.chatScrollArea.scrollHeight;
  }

  // ==========================================================================
  // Update Right Inspector Panel
  // ==========================================================================
  function updateRightInspector(botMsg) {
    // 1. Source Used
    let sourceText = 'Web Search (Tavily)';
    if (botMsg.source_used) {
      if (botMsg.source_used.toLowerCase().includes('kb')) {
        sourceText = 'Internal KB (Pinecone)';
      } else if (botMsg.source_used.toLowerCase().includes('direct')) {
        sourceText = 'Direct LLM Response';
      } else {
        sourceText = botMsg.source_used;
      }
    }
    el.sourceUsedText.innerText = sourceText;

    // 2. Citations
    el.citationsContainer.innerHTML = '';
    const citations = botMsg.citations || ['Internal Knowledge Base'];
    citations.forEach(c => {
      const title = typeof c === 'string' ? c : (c.title || 'Knowledge Base');
      const snippet = typeof c === 'string' ? 'Source reference for response verification' : (c.snippet || 'Referenced documentation');
      
      const div = document.createElement('div');
      div.className = 'citation-entry-box';
      div.innerHTML = `
        <div class="citation-header-row">
          <a href="#" class="citation-link-text">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            <span>${escapeHtml(title)}</span>
          </a>
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:var(--text-light);"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        </div>
        <div class="citation-subtext">${escapeHtml(snippet)}</div>
      `;
      el.citationsContainer.appendChild(div);
    });

    // 3. Workflow Trace Timeline
    el.workflowTimelineContainer.innerHTML = '';
    const traceSteps = parseTraceSteps(botMsg.trace, botMsg.time);

    traceSteps.forEach(step => {
      const stepDiv = document.createElement('div');
      stepDiv.className = 'timeline-step';
      stepDiv.innerHTML = `
        <div class="step-node-dot ${step.color}"></div>
        <div class="step-content-box">
          <div class="step-title-row">
            <span class="step-title">${escapeHtml(step.title)}</span>
            <span class="step-time">${escapeHtml(step.time)}</span>
          </div>
          <div class="step-desc">${escapeHtml(step.desc)}</div>
        </div>
      `;
      el.workflowTimelineContainer.appendChild(stepDiv);
    });
  }

  function parseTraceSteps(rawTrace, fallbackTime) {
    const time = fallbackTime || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (!rawTrace || rawTrace.length === 0) {
      return [
        { title: 'Routed to: kb', time: time, desc: 'Classified as knowledge base query', color: 'blue' },
        { title: 'Retrieved Pinecone KB', time: time, desc: 'Fetched relevant policy documents', color: 'green' },
        { title: 'Generated Answer', time: time, desc: 'Synthesized final response', color: 'green' }
      ];
    }

    // If trace elements are structured objects
    if (typeof rawTrace[0] === 'object' && rawTrace[0].title) {
      return rawTrace;
    }

    // Convert string array to styled timeline objects
    return rawTrace.map(stepStr => {
      let color = 'blue';
      let desc = 'Processing node execution';
      const s = String(stepStr);

      if (s.includes('Routed to:')) {
        color = 'blue';
        desc = 'Classified query intent';
      } else if (s.includes('Pinecone') || s.includes('Retrieved')) {
        color = 'green';
        desc = 'Fetched relevant documents from vector store';
      } else if (s.includes('Graded: weak')) {
        color = 'amber';
        desc = 'KB documents did not fully answer';
      } else if (s.includes('Graded: good')) {
        color = 'green';
        desc = 'Evidence verified as relevant';
      } else if (s.includes('Tavily') || s.includes('web search')) {
        color = 'blue';
        desc = 'Searched the web for additional context';
      } else if (s.includes('Rewrote')) {
        color = 'amber';
        desc = 'Refined query keywords for better retrieval';
      } else {
        color = 'green';
        desc = 'Agentic step completed';
      }

      return {
        title: s,
        time: time,
        desc: desc,
        color: color
      };
    });
  }

  // ==========================================================================
  // Markdown Formatter
  // ==========================================================================
  function formatMarkdown(text) {
    if (!text) return '';
    let html = escapeHtml(text);

    // Bold
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Headings
    html = html.replace(/^### (.*$)/gim, '<h4 style="margin:12px 0 6px; font-weight:700;">$1</h4>');
    html = html.replace(/^## (.*$)/gim, '<h3 style="margin:14px 0 8px; font-weight:700;">$1</h3>');

    // Bullet lists
    html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
    html = html.replace(/^(?:<li>.*<\/li>\s*)+/gims, '<ul style="margin:8px 0 12px 20px;">$&</ul>');

    // Numbered lists
    html = html.replace(/^\d+\.\s+(.*$)/gim, '<li>$1</li>');
    
    // Paragraphs
    html = html.split('\n\n').map(chunk => {
      chunk = chunk.trim();
      if (!chunk) return '';
      if (chunk.startsWith('<h') || chunk.startsWith('<ul') || chunk.startsWith('<ol')) {
        return chunk;
      }
      return `<p>${chunk.replace(/\n/g, '<br>')}</p>`;
    }).join('');

    return html;
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // ==========================================================================
  // Send Query Handler
  // ==========================================================================
  async function handleSend() {
    const question = el.queryTextInput.value.trim();
    if (!question || state.isSending) return;

    el.queryTextInput.value = '';
    state.isSending = true;
    el.btnSendQuery.disabled = true;

    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Append User Message
    const userMsg = {
      role: 'user',
      text: question,
      time: currentTime
    };
    state.messages.push(userMsg);
    appendMessageElement(userMsg);
    scrollToBottom();

    // Show typing
    showTypingIndicator();

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question })
      });

      hideTypingIndicator();

      if (!response.ok) {
        const errJson = await response.json().catch(() => ({}));
        throw new Error(errJson.detail || `Server error (${response.status})`);
      }

      const data = await response.json();
      const botMsg = {
        role: 'assistant',
        text: data.answer || 'No answer provided.',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        source_used: data.source_used || 'kb',
        citations: data.citations || ['Internal KB'],
        trace: data.trace || ['Routed to: kb', 'Retrieved docs from Pinecone', 'Synthesized Answer']
      };

      state.messages.push(botMsg);
      appendMessageElement(botMsg);
      updateRightInspector(botMsg);
      scrollToBottom();

    } catch (err) {
      hideTypingIndicator();
      console.warn('API error:', err);

      const botMsg = {
        role: 'assistant',
        text: `⚠️ **Diagnostic Notice**: ${err.message}\n\nPlease check your server logs or API credentials in \`.env\`.`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        source_used: 'Diagnostic',
        citations: ['System Diagnostics'],
        trace: ['Failed at /chat endpoint', `Error: ${err.message}`]
      };

      state.messages.push(botMsg);
      appendMessageElement(botMsg);
      updateRightInspector(botMsg);
      scrollToBottom();
    } finally {
      state.isSending = false;
      el.btnSendQuery.disabled = false;
      el.queryTextInput.focus();
    }
  }

  // ==========================================================================
  // Sidebar Vector Document Upload
  // ==========================================================================
  async function handleSidebarVectorUpload() {
    const file = state.selectedFile || (el.sidebarFileInput && el.sidebarFileInput.files[0]);
    const key = el.sidebarAdminKey ? el.sidebarAdminKey.value.trim() : '';

    if (!key) {
      if (el.sidebarUploadStatus) {
        el.sidebarUploadStatus.innerHTML = `
          <div class="sidebar-status-msg error">Please enter the Admin API Key</div>
        `;
      }
      if (el.sidebarAdminKey) el.sidebarAdminKey.focus();
      return;
    }

    if (!file) {
      if (el.sidebarUploadStatus) {
        el.sidebarUploadStatus.innerHTML = `
          <div class="sidebar-status-msg error">Please choose a document first</div>
        `;
      }
      return;
    }

    state.adminKey = key;
    localStorage.setItem('it_admin_key', key);

    el.sidebarUploadBtn.disabled = true;
    el.sidebarUploadStatus.innerHTML = `
      <div class="sidebar-status-msg loading">
        Chunking and indexing ${escapeHtml(file.name)} into Pinecone...
      </div>
    `;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/ingest', {
        method: 'POST',
        headers: { 'x-admin-key': key },
        body: formData
      });

      const json = await res.json();
      if (!res.ok) {
        throw new Error(json.detail || 'Ingestion failed');
      }

      el.sidebarUploadStatus.innerHTML = `
        <div class="sidebar-status-msg success">
          ✓ Indexed ${escapeHtml(file.name)} in Pinecone!
        </div>
      `;

      showToast(`Successfully indexed ${file.name}`, 'success');

      setTimeout(() => {
        state.selectedFile = null;
        if (el.sidebarFileInput) el.sidebarFileInput.value = '';
        if (el.sidebarSelectedFileName) el.sidebarSelectedFileName.innerText = 'No file chosen';
      }, 4000);

    } catch (e) {
      el.sidebarUploadStatus.innerHTML = `
        <div class="sidebar-status-msg error">
          ❌ ${escapeHtml(e.message)}
        </div>
      `;
      showToast(e.message, 'error');
    } finally {
      el.sidebarUploadBtn.disabled = false;
    }
  }

  function showToast(text, type = 'info') {
    const toast = document.createElement('div');
    toast.className = 'toast-notice';
    toast.innerText = text;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // ==========================================================================
  // Event Listeners
  // ==========================================================================
  function setupEvents() {
    // Send message
    el.btnSendQuery.addEventListener('click', handleSend);
    el.queryTextInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleSend();
      }
    });

    // Upload paperclip button in chat bar triggers file picker
    if (el.btnUploadClip) {
      el.btnUploadClip.addEventListener('click', () => {
        if (el.sidebarFileInput) el.sidebarFileInput.click();
      });
    }

    // Sidebar Vector Upload
    if (el.sidebarFileBox && el.sidebarFileInput) {
      el.sidebarFileBox.addEventListener('click', () => el.sidebarFileInput.click());

      el.sidebarFileInput.addEventListener('change', () => {
        if (el.sidebarFileInput.files.length > 0) {
          state.selectedFile = el.sidebarFileInput.files[0];
          if (el.sidebarSelectedFileName) {
            el.sidebarSelectedFileName.innerText = state.selectedFile.name;
          }
          if (el.sidebarUploadStatus) {
            el.sidebarUploadStatus.innerHTML = '';
          }
        }
      });

      // Drag and drop
      el.sidebarFileBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        el.sidebarFileBox.classList.add('dragover');
      });

      el.sidebarFileBox.addEventListener('dragleave', () => {
        el.sidebarFileBox.classList.remove('dragover');
      });

      el.sidebarFileBox.addEventListener('drop', (e) => {
        e.preventDefault();
        el.sidebarFileBox.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
          state.selectedFile = e.dataTransfer.files[0];
          if (el.sidebarSelectedFileName) {
            el.sidebarSelectedFileName.innerText = state.selectedFile.name;
          }
          if (el.sidebarUploadStatus) {
            el.sidebarUploadStatus.innerHTML = '';
          }
        }
      });
    }

    if (el.sidebarUploadBtn) {
      el.sidebarUploadBtn.addEventListener('click', handleSidebarVectorUpload);
    }
  }

  // Boot on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
