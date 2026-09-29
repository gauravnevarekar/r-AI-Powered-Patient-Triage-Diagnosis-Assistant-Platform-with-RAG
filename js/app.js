/**
 * HealthBridge AI - Core Frontend Controller
 */

// State Object
const AppState = {
  sessionId: 'sess_' + Math.random().toString(36).substr(2, 9),
  symptomsText: '',
  selectedChips: [],
  duration: '< 24 hours',
  severity: 4,
  onset: 'Sudden onset',
  secondaryNotes: '',
  uploadedFiles: [],
  latestAssessment: null,
  rxContext: null,
  uploadedPrescription: null
};

// Navigation Function
function navigateTo(screenId) {
  const screens = document.querySelectorAll('.app-screen');
  screens.forEach(s => s.classList.add('hidden'));

  const target = document.getElementById(screenId);
  if (target) {
    target.classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Update Nav Items
  const navLinks = document.querySelectorAll('footer nav a');
  navLinks.forEach(link => {
    link.classList.remove('text-primary', 'font-bold');
    link.classList.add('text-on-surface-variant');
  });

  if (screenId === 'screen-home' || screenId === 'screen-symptom-input' || screenId === 'screen-results') {
    const navTriage = document.getElementById('nav-triage');
    if (navTriage) navTriage.classList.add('text-primary', 'font-bold');
  } else if (screenId === 'screen-care-finder') {
    const navCare = document.getElementById('nav-care');
    if (navCare) navCare.classList.add('text-primary', 'font-bold');
  } else if (screenId === 'screen-rx-qa') {
    const navRx = document.getElementById('nav-rx');
    if (navRx) navRx.classList.add('text-primary', 'font-bold');
    renderRxCard();
  } else if (screenId === 'screen-records') {
    const navRecords = document.getElementById('nav-records');
    if (navRecords) navRecords.classList.add('text-primary', 'font-bold');
  }
}

// Symptom Chip Toggle
function toggleSymptomChip(btn, symptomName) {
  const icon = btn.querySelector('.material-symbols-outlined');
  const index = AppState.selectedChips.indexOf(symptomName);

  if (index > -1) {
    AppState.selectedChips.splice(index, 1);
    btn.classList.remove('bg-primary', 'text-on-primary');
    btn.classList.add('bg-surface-container-low', 'text-on-surface-variant');
    if (icon) icon.textContent = 'add';
  } else {
    AppState.selectedChips.push(symptomName);
    btn.classList.remove('bg-surface-container-low', 'text-on-surface-variant');
    btn.classList.add('bg-primary', 'text-on-primary');
    if (icon) icon.textContent = 'check';
  }

  const checkLabel = document.getElementById('check-symptoms-btn-label');
  if (checkLabel) {
    if (AppState.selectedChips.length > 0) {
      checkLabel.textContent = `Check symptoms (${AppState.selectedChips.length} selected)`;
    } else {
      checkLabel.textContent = 'Check my symptoms';
    }
  }
}

// Set Duration Pill
function selectDuration(pill, value) {
  document.querySelectorAll('.duration-pill').forEach(p => {
    p.className = 'duration-pill flex items-center justify-center gap-1.5 py-3 px-space-xs rounded-xl bg-surface-container-low text-on-surface font-label-md text-label-md hover:bg-surface-container transition-all';
  });
  pill.className = 'duration-pill flex items-center justify-center gap-1.5 py-3 px-space-xs rounded-xl bg-primary text-on-primary font-label-md text-label-md shadow-sm transition-all';
  AppState.duration = value;
}

// Set Severity Level
function selectSeverity(btn, level, label, desc) {
  AppState.severity = level;
  const severityButtons = document.querySelectorAll('.severity-step');
  const severityScorePill = document.getElementById('severity-score-pill');
  const severityDescText = document.getElementById('severity-description-text');

  severityButtons.forEach(b => {
    b.className = 'severity-step flex flex-col items-center justify-center py-2.5 rounded-lg bg-surface-container-low text-secondary hover:bg-surface-container transition-colors';
  });

  if (level >= 4) {
    btn.className = 'severity-step flex flex-col items-center justify-center py-2.5 rounded-lg bg-error text-on-error shadow-sm font-semibold';
    if (severityScorePill) severityScorePill.className = 'font-label-sm text-label-sm px-2.5 py-0.5 rounded-full bg-error-container text-on-error-container';
  } else {
    btn.className = 'severity-step flex flex-col items-center justify-center py-2.5 rounded-lg bg-primary text-on-primary font-semibold shadow-sm';
    if (severityScorePill) severityScorePill.className = 'font-label-sm text-label-sm px-2.5 py-0.5 rounded-full bg-surface-container text-primary';
  }

  if (severityScorePill) severityScorePill.textContent = label;
  if (severityDescText) severityDescText.textContent = desc;
}

// Upload Medical History API Integration
async function handleFileUpload(event) {
  const files = event.target.files;
  if (!files || files.length === 0) return;

  const file = files[0];
  const formData = new FormData();
  formData.append('file', file);
  formData.append('category', 'labs');
  formData.append('session_id', AppState.sessionId);

  try {
    const res = await fetch('/api/history/upload', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    AppState.uploadedFiles.push(data.filename);

    const container = document.getElementById('fileListContainer');
    if (container) {
      const card = document.createElement('div');
      card.className = 'rounded-xl bg-surface-container-lowest p-space-sm shadow-sm flex items-center gap-space-sm transition-all hover:shadow';
      card.innerHTML = `
        <div class="w-12 h-12 rounded-lg bg-surface-container flex items-center justify-center text-primary shrink-0 relative">
          <span class="material-symbols-outlined text-[24px]">picture_as_pdf</span>
          <span class="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-primary-container text-on-primary flex items-center justify-center text-[10px]">
            <span class="material-symbols-outlined text-[10px]">check</span>
          </span>
        </div>
        <div class="flex flex-col min-w-0 flex-1">
          <span class="font-label-md text-label-md font-semibold text-on-surface truncate">${data.filename}</span>
          <span class="font-body-sm text-body-sm text-secondary">PDF Extracted: ${data.extracted_history ? data.extracted_history.join(', ') : 'Ready'}</span>
        </div>
      `;
      container.prepend(card);
    }
    if (data.extracted_medications && data.extracted_medications.length > 0 && data.extracted_medications[0] !== "No specific chronic medications flagged") {
      AppState.rxContext = data.extracted_medications.join(', ');
      AppState.uploadedPrescription = {
        filename: data.filename,
        medications: data.extracted_medications
      };
    } else {
      AppState.rxContext = data.filename;
      AppState.uploadedPrescription = {
        filename: data.filename,
        medications: [data.filename]
      };
    }
    renderRxCard();
  } catch (err) {
    console.error('File upload error:', err);
  }
}

// Submit Assessment to REST API
async function submitAssessment() {
  const descInput = document.getElementById('symptom-description');
  if (descInput) AppState.symptomsText = descInput.value;

  const secondaryInput = document.getElementById('secondary-input');
  if (secondaryInput) AppState.secondaryNotes = secondaryInput.value;

  // Show processing animation screen
  navigateTo('screen-processing');

  const payload = {
    session_id: AppState.sessionId,
    symptom_description: AppState.symptomsText || 'Sharp abdominal pain and nausea',
    symptom_chips: AppState.selectedChips,
    duration: AppState.duration,
    severity: AppState.severity,
    onset: AppState.onset,
    secondary_notes: AppState.secondaryNotes,
    dpdp_consent: true
  };

  try {
    const res = await fetch('/api/triage/assess', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    AppState.latestAssessment = data;

    // Simulate clinical step progress animation
    setTimeout(() => {
      renderAssessmentResults(data);
      navigateTo('screen-results');
    }, 1000);

  } catch (err) {
    console.error('Triage assessment error:', err);
    alert('Assessment failed. Ensure FastAPI backend is running.');
  }
}

// Render Results Screen with Live API Response
function renderAssessmentResults(data) {
  // Urgency Banner
  const urgencyBanner = document.getElementById('results-urgency-banner');
  const urgencyTitle = document.getElementById('results-urgency-title');
  const urgencyDesc = document.getElementById('results-urgency-desc');
  const careWindow = document.getElementById('results-care-window');

  if (urgencyTitle) urgencyTitle.textContent = data.urgency_title;
  if (urgencyDesc) urgencyDesc.textContent = data.urgency_description;
  if (careWindow) careWindow.textContent = `Care Window: ${data.time_window}`;

  if (urgencyBanner) {
    if (data.urgency_level === 'EMERGENCY_IMMEDIATE') {
      urgencyBanner.className = 'w-full rounded-xl bg-error text-on-error p-space-lg shadow-md flex flex-col gap-space-xs relative overflow-hidden';
    } else {
      urgencyBanner.className = 'w-full rounded-xl bg-error-container text-on-error-container p-space-lg shadow-md flex flex-col gap-space-xs relative overflow-hidden';
    }
  }

  // Primary Condition Match
  const conditionTitle = document.getElementById('results-condition-title');
  if (conditionTitle) conditionTitle.textContent = `${data.primary_condition} (${Math.round(data.primary_confidence * 100)}% Confidence)`;

  // Clinical Reasoning & RAG Citations
  const reasoningText = document.getElementById('results-reasoning-text');
  if (reasoningText) reasoningText.textContent = data.clinical_reasoning;

  const citationsContainer = document.getElementById('results-citations-container');
  if (citationsContainer && data.rag_citations) {
    citationsContainer.innerHTML = data.rag_citations.map(c => `
      <div class="inline-flex items-center gap-1.5 px-space-sm py-space-xxs rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm">
        <span class="material-symbols-outlined text-[14px]">menu_book</span>
        <span>Source: ${c.source_title} (${c.guideline_ref})</span>
      </div>
    `).join('');
  }

  // Recommended Specialist
  const specialistTitle = document.getElementById('results-specialist-title');
  if (specialistTitle) specialistTitle.textContent = data.recommended_specialist;
}

// Fetch Nearby Care Facilities using Real GPS
async function fetchNearbyCare() {
  const specialist = AppState.latestAssessment ? AppState.latestAssessment.recommended_specialist : 'General Surgeon';
  const urgency = AppState.latestAssessment ? AppState.latestAssessment.urgency_level : 'URGENT_12_24_HRS';

  let latParam = '';
  if (navigator.geolocation) {
    try {
      const pos = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 4000 });
      });
      latParam = `&lat=${pos.coords.latitude}&lng=${pos.coords.longitude}`;
    } catch (e) {
      console.log('GPS Permission notice (using default region):', e);
    }
  }

  try {
    const res = await fetch(`/api/care/nearby?specialist=${encodeURIComponent(specialist)}&urgency=${encodeURIComponent(urgency)}${latParam}`);
    const data = await res.json();

    const list = document.getElementById('facilitiesList');
    if (list && data.facilities) {
      list.innerHTML = data.facilities.map(f => `
        <article class="facility-card flex flex-col bg-surface-container-lowest rounded-xl p-space-md shadow-sm">
          <div class="flex items-start justify-between gap-space-xs mb-space-xs">
            <div class="flex flex-col flex-1 min-w-0">
              <span class="font-label-sm text-label-sm text-primary uppercase font-bold">${f.type}</span>
              <h2 class="font-headline-sm text-headline-sm text-on-surface truncate">${f.name}</h2>
            </div>
            <div class="w-9 h-9 rounded-full bg-surface-container flex items-center justify-center">
              <span class="material-symbols-outlined text-primary text-[20px]">local_hospital</span>
            </div>
          </div>
          <div class="flex flex-col gap-1 mb-space-md">
            <span class="font-label-md text-label-md text-primary font-semibold">${f.distance_km} km away • ${f.open_now ? 'Open Now' : 'Closed'}</span>
            <span class="font-body-sm text-body-sm text-on-surface-variant">${f.address}</span>
          </div>
          <div class="grid grid-cols-2 gap-space-xs">
            <a class="flex items-center justify-center gap-2 h-12 rounded-lg bg-surface-container text-primary font-label-lg text-label-lg" href="tel:${f.phone}">
              <span class="material-symbols-outlined text-[19px]">call</span>
              <span>Call</span>
            </a>
            <a class="flex items-center justify-center gap-2 h-12 rounded-lg bg-primary text-on-primary font-label-lg text-label-lg shadow-sm" href="${f.maps_url}" target="_blank">
              <span class="material-symbols-outlined text-[19px]">directions</span>
              <span>Directions</span>
            </a>
          </div>
        </article>
      `).join('');
    }
  } catch (err) {
    console.error('Care finder error:', err);
  }
}

// Prescription Q&A Handler
async function handleRxQuestion(event) {
  event.preventDefault();
  const input = document.getElementById('chatInput');
  const feed = document.getElementById('chatFeed');
  if (!input || !feed) return;

  const text = input.value.trim();
  if (!text) return;

  // Add User Bubble
  const userDiv = document.createElement('div');
  userDiv.className = 'flex flex-col items-end gap-1.5 w-full';
  userDiv.innerHTML = `
    <div class="flex items-center gap-1.5 pr-1">
      <span class="font-label-sm text-label-sm text-on-surface-variant">You</span>
    </div>
    <div class="bg-primary text-on-primary rounded-2xl rounded-tr-none px-space-md py-space-sm max-w-[85%] shadow-sm">
      <p class="font-body-md text-body-md text-on-primary">${text}</p>
    </div>
  `;
  feed.appendChild(userDiv);
  input.value = '';

  try {
    const res = await fetch('/api/rx/qa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: AppState.sessionId,
        prescription_name: AppState.rxContext,
        question: text
      })
    });
    const data = await res.json();

    // Add AI RAG Response Bubble
    const aiDiv = document.createElement('div');
    aiDiv.className = 'flex flex-col items-start gap-space-xs w-full mt-2';
    aiDiv.innerHTML = `
      <div class="flex items-center gap-space-xs pl-1">
        <div class="w-6 h-6 rounded-full bg-primary-container flex items-center justify-center text-on-primary">
          <span class="material-symbols-outlined text-[14px]">smart_toy</span>
        </div>
        <span class="font-label-md text-label-md text-on-surface">HealthTriage Clinical AI</span>
      </div>
      <div class="bg-surface-container-lowest text-on-surface rounded-2xl rounded-tl-none p-space-md max-w-[92%] shadow-sm flex flex-col gap-space-sm">
        <p class="font-body-md text-body-md text-on-surface">${data.answer}</p>
        ${data.safety_alert ? `<div class="bg-error-container/40 p-2 rounded text-error font-body-sm">${data.safety_alert}</div>` : ''}
        <div class="pt-1 flex flex-wrap items-center gap-1.5">
          <div class="bg-surface-container-high px-2.5 py-1 rounded-full flex items-center gap-1 text-on-surface-variant">
            <span class="material-symbols-outlined text-[14px] text-primary">menu_book</span>
            <span class="font-label-sm text-label-sm">${data.source_monograph}</span>
          </div>
        </div>
      </div>
    `;
    feed.appendChild(aiDiv);
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  } catch (err) {
    console.error('Rx Q&A error:', err);
  }
}

// Purge Session Data (DPDP Act 2023 Erasure)
async function purgePatientSession() {
  try {
    await fetch(`/api/privacy/session/${AppState.sessionId}`, { method: 'DELETE' });
    alert('All session data permanently purged under DPDP Act 2023.');
    AppState.sessionId = 'sess_' + Math.random().toString(36).substr(2, 9);
    AppState.rxContext = null;
    AppState.uploadedPrescription = null;
    renderRxCard();
    navigateTo('screen-home');
  } catch (err) {
    console.error('Erasure error:', err);
  }
}

// Render Attached Prescription Card for Rx Q&A
function renderRxCard() {
  const container = document.getElementById('attached-prescription-container');
  if (!container) return;

  if (AppState.uploadedPrescription || AppState.rxContext) {
    const rxName = AppState.rxContext || (AppState.uploadedPrescription ? AppState.uploadedPrescription.filename : '');
    const meds = (AppState.uploadedPrescription && AppState.uploadedPrescription.medications && AppState.uploadedPrescription.medications.length > 0)
      ? AppState.uploadedPrescription.medications.join(', ')
      : rxName;

    container.innerHTML = `
      <div class="bg-surface-container-lowest rounded-xl p-space-md shadow-sm flex items-center justify-between">
        <div>
          <div class="flex items-center gap-1.5 mb-1">
            <span class="material-symbols-outlined text-[18px] text-primary">description</span>
            <span class="font-label-md text-label-md text-on-surface font-bold">Attached Prescription</span>
          </div>
          <p class="font-body-sm text-secondary">${meds}</p>
        </div>
        <button type="button" class="text-xs text-secondary hover:text-error px-2 py-1" onclick="clearAttachedPrescription()">
          Clear
        </button>
      </div>
    `;
  } else {
    container.innerHTML = `
      <div class="bg-surface-container-lowest rounded-xl p-space-md shadow-sm flex flex-col items-center text-center py-6 gap-2">
        <div class="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center text-secondary">
          <span class="material-symbols-outlined text-[24px]">upload_file</span>
        </div>
        <span class="font-label-md text-on-surface font-semibold">No Prescription Attached</span>
        <p class="font-body-sm text-secondary">Upload a prescription to ask questions about your medication, side effects, and interactions.</p>
        <label class="mt-2 inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-primary text-on-primary font-label-md cursor-pointer hover:bg-primary/90 transition-colors">
          <span class="material-symbols-outlined text-[18px]">cloud_upload</span>
          <span>Upload Prescription</span>
          <input type="file" class="hidden" accept="image/*,application/pdf" onchange="handleFileUpload(event)">
        </label>
      </div>
    `;
  }
}

function clearAttachedPrescription() {
  AppState.rxContext = null;
  AppState.uploadedPrescription = null;
  renderRxCard();
}

document.addEventListener('DOMContentLoaded', renderRxCard);

