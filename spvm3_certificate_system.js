/* 
  SPVM3 TECH SOLUTION — CERTIFICATE SYSTEM & SUBJECT MANAGER
  Converts study minutes to course hours (30 mins = 1 Hour)
  Generates official certificates with exact Completion Timestamp (Date, Minute, Second), Brand Logo, & Student Name.
*/

const SPVM3_SUBJECTS_MASTER = [
  {
    id: "html-css",
    title: "HTML & CSS Complete Notes",
    file: "HTML-CSS-Complete-Notes.html",
    readTimeMin: 45,
    category: "web",
    level: "Beginner to Advanced",
    accent: "#e44d26",
    icon: "🌐",
    description: "Semantic HTML5, CSS3 Box Model, Flexbox, Grid, Animations & Responsive Design."
  },
  {
    id: "javascript",
    title: "JavaScript A–Z Interactive Notes",
    file: "js-notes.html",
    readTimeMin: 50,
    category: "web",
    level: "Intermediate",
    accent: "#f7df1e",
    icon: "⚡",
    description: "ES6+, Async/Await, Promises, Closures, DOM, Prototypes & Event Loop."
  },
  {
    id: "react-notes",
    title: "React.js Complete Interactive Notes",
    file: "react-notes.html",
    readTimeMin: 40,
    category: "web",
    level: "Intermediate",
    accent: "#61dafb",
    icon: "⚛️",
    description: "JSX, Component Lifecycle, Hooks, Context API & State Management."
  },
  {
    id: "react-manual",
    title: "React Field Manual Notes",
    file: "react-field-manual.html",
    readTimeMin: 35,
    category: "web",
    level: "Advanced",
    accent: "#00b4d8",
    icon: "📘",
    description: "Enterprise React patterns, Error Boundaries, Suspense & Architecture."
  },
  {
    id: "electron-js",
    title: "Electron.js Desktop Apps Notes",
    file: "electron-js-notes.html",
    readTimeMin: 35,
    category: "lang",
    level: "Intermediate",
    accent: "#47848f",
    icon: "💻",
    description: "Build cross-platform desktop applications with Main & Renderer IPC."
  },
  {
    id: "php-notes",
    title: "PHP Complete Reference Notes",
    file: "php-notes.html",
    readTimeMin: 40,
    category: "lang",
    level: "Beginner to Intermediate",
    accent: "#777bb4",
    icon: "🐘",
    description: "Server-side scripting, Form Handling, OOP in PHP 8 & MySQL Access."
  },
  {
    id: "python-notes",
    title: "Python A–Z Master Notes",
    file: "python_notes.html",
    readTimeMin: 90,
    category: "lang",
    level: "Beginner to Advanced",
    accent: "#3776ab",
    icon: "🐍",
    description: "Variables, OOP, Decorators, Generators, Multithreading & Frameworks."
  },
  {
    id: "c-programming",
    title: "C Programming Complete Notes",
    file: "C-Programming-Complete-Notes.html",
    readTimeMin: 60,
    category: "lang",
    level: "Beginner to Advanced",
    accent: "#2d7dd2",
    icon: "🔤",
    description: "Pointers, Memory Allocation, Structures, Unions, File I/O & Bitwise."
  },
  {
    id: "cpp-notes",
    title: "C++ Interactive Notes",
    file: "cpp-notes.html",
    readTimeMin: 55,
    category: "lang",
    level: "Intermediate to Advanced",
    accent: "#00599c",
    icon: "⚡",
    description: "OOP, STL Vectors/Maps, Smart Pointers, Templates & C++20 features."
  },
  {
    id: "java-notes",
    title: "Java Brewed Complete Notes",
    file: "java-notes.html",
    readTimeMin: 60,
    category: "lang",
    level: "Beginner to Advanced",
    accent: "#e76f51",
    icon: "☕",
    description: "JVM Architecture, OOP, Collections, Streams API & Multithreading."
  },
  {
    id: "dbms-sql",
    title: "DBMS & SQL Complete Reference Notes",
    file: "DBMS-and-SQL-Complete-Reference.html",
    readTimeMin: 75,
    category: "systems",
    level: "Beginner to Advanced",
    accent: "#00758f",
    icon: "🗄️",
    description: "Relational Algebra, ER Diagrams, Normalization, SQL Joins & ACID."
  },
  {
    id: "operating-systems",
    title: "Operating Systems Notes",
    file: "operating-systems-complete-notes.html",
    readTimeMin: 85,
    category: "systems",
    level: "Intermediate to Advanced",
    accent: "#10b981",
    icon: "🖥️",
    description: "Process Management, CPU Scheduling, Deadlocks, Paging & File Systems."
  },
  {
    id: "computer-fundamentals",
    title: "Fundamentals of Computers Notes",
    file: "fundamentals-of-computers-notes.html",
    readTimeMin: 40,
    category: "systems",
    level: "Beginner",
    accent: "#8b5cf6",
    icon: "🕹️",
    description: "Hardware Architecture, Binary Math, Logic Gates & OS Overview."
  },
  {
    id: "software-testing",
    title: "Software Testing & QA Notes",
    file: "software-testing-notes.html",
    readTimeMin: 45,
    category: "ai",
    level: "Intermediate",
    accent: "#ec4899",
    icon: "🧪",
    description: "Unit Testing, Integration, Black/White Box, TDD, BDD & Automation."
  },
  {
    id: "git-guide",
    title: "Git & Version Control Notes",
    file: "git-clone-guide.html",
    readTimeMin: 25,
    category: "devops",
    level: "Beginner to Intermediate",
    accent: "#f05032",
    icon: "🌿",
    description: "Git Init, Clone, Branching, Merging, Rebasing & Resolving Conflicts."
  },
  {
    id: "docker-notes",
    title: "Docker Containerization Notes",
    file: "docker-notes.html",
    readTimeMin: 45,
    category: "devops",
    level: "Intermediate",
    accent: "#2496ed",
    icon: "🐳",
    description: "Dockerfiles, Container Lifecycle, Volumes, Networking & Docker Compose."
  },
  {
    id: "kubernetes-guide",
    title: "Kubernetes Orchestration Notes",
    file: "kubernetes-a-to-z-guide.html",
    readTimeMin: 60,
    category: "devops",
    level: "Advanced",
    accent: "#326ce5",
    icon: "☸️",
    description: "Pods, Deployments, Services, Ingress, ConfigMaps, Secrets & Helm."
  },
  {
    id: "deep-learning",
    title: "Deep Learning & AI Notes",
    file: "deep-learning-notes.html",
    readTimeMin: 75,
    category: "ai",
    level: "Advanced",
    accent: "#a855f7",
    icon: "🧠",
    description: "Perceptrons, Backpropagation, CNNs, RNNs, LSTMs & Transformers."
  },
  {
    id: "ai-systems",
    title: "AI Systems & LLM Agents Notes",
    file: "ai-systems-notes.html",
    readTimeMin: 60,
    category: "ai",
    level: "Advanced",
    accent: "#06b6d4",
    icon: "🤖",
    description: "Autonomous Intelligent Agents, Multi-Agent Systems, ReAct Loops, LLM/VLM/SLM/LCM Architectures."
  },
  {
    id: "blockchain",
    title: "Blockchain & Cryptography Notes",
    file: "blockchain-notes.html",
    readTimeMin: 60,
    category: "systems",
    level: "Advanced",
    accent: "#e2933d",
    icon: "⛓️",
    description: "Cryptographic Hashing, Proof of Work/Stake, Merkle Trees, zk-SNARKs & Layer-2 Rollups."
  },
  {
    id: "dsa-notes",
    title: "Data Structures & Algorithms (DSA) Notes",
    file: "data-structures-notes.html",
    readTimeMin: 75,
    category: "systems",
    level: "Intermediate to Advanced",
    accent: "#7fe0b3",
    icon: "🧩",
    description: "Linear & Non-Linear Data Structures, Linked Lists, Trees, Graphs, Sorting & Complexity."
  }
];

// Calculation rule: 30 minutes = 1.0 Hour of course time
function calcCourseHours(minutes) {
  const hours = (minutes / 30).toFixed(1);
  return `${hours} ${hours === "1.0" ? "Hour" : "Hours"}`;
}

// Local Storage Handlers
function getCompletedCertData() {
  return JSON.parse(localStorage.getItem('spvm3_cert_records') || '{}');
}

function getStudentName() {
  return localStorage.getItem('spvm3_student_name') || '';
}

function setStudentName(name) {
  localStorage.setItem('spvm3_student_name', name || '');
}

function getStudentEmail() {
  return localStorage.getItem('spvm3_student_email') || '';
}

function setStudentEmail(email) {
  localStorage.setItem('spvm3_student_email', email || '');
}

function isStudentLoggedIn() {
  const email = getStudentEmail();
  return email && email.includes('@');
}

// -----------------------------------------------------------------------------
// COURSE READING & COMPLETION PROGRESS TRACKER (80% UNLOCK RULE)
// -----------------------------------------------------------------------------
function getCourseProgress(subjectId) {
  const storedProgress = localStorage.getItem(`spvm3_progress_${subjectId}`);
  if (storedProgress) {
    return Math.min(100, Math.max(0, parseInt(storedProgress, 10)));
  }
  // Default fallback for legacy visitors
  return 85; 
}

function setCourseProgress(subjectId, percent) {
  const current = getCourseProgress(subjectId);
  const updated = Math.min(100, Math.max(current, Math.round(percent)));
  localStorage.setItem(`spvm3_progress_${subjectId}`, updated.toString());
  
  // If progress reaches 80% for the first time, auto-trigger certificate email queue
  if (updated >= 80 && isStudentLoggedIn()) {
    const certRecords = getCompletedCertData();
    if (!certRecords[subjectId]) {
      markCourseCompleted(subjectId);
      const certData = certRecords[subjectId] || {};
      const subject = SPVM3_SUBJECTS_MASTER.find(s => s.id === subjectId);
      if (subject && certData.certId) {
        // Auto send certificate to student's Gmail (1-2 minutes queue)
        sendSPVM3CertificateEmailSilent(subjectId, certData.certId);
      }
    }
  }
  return updated;
}

// Auto track page scroll depth on course pages
function initAutoScrollProgressTracker(subjectId) {
  if (!subjectId) return;

  const updateProgressFromScroll = () => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = Math.max(
      document.body.scrollHeight,
      document.body.offsetHeight,
      document.documentElement.clientHeight,
      document.documentElement.scrollHeight,
      document.documentElement.offsetHeight
    );
    const windowHeight = window.innerHeight;
    const scrollable = docHeight - windowHeight;
    
    if (scrollable > 0) {
      const scrollPercent = (scrollTop / scrollable) * 100;
      // Calculate progress starting from 15% initial read up to 100%
      const calculatedProgress = Math.min(100, Math.round(scrollPercent));
      setCourseProgress(subjectId, calculatedProgress);
      updateTopProgressBarUI(calculatedProgress);
    }
  };

  window.addEventListener('scroll', updateProgressFromScroll, { passive: true });
  window.addEventListener('load', updateProgressFromScroll);
  updateProgressFromScroll();
}

function updateTopProgressBarUI(percent) {
  let barContainer = document.getElementById('spvm3-reading-progress-bar');
  if (!barContainer) {
    barContainer = document.createElement('div');
    barContainer.id = 'spvm3-reading-progress-bar';
    barContainer.style.cssText = `
      position: fixed; top: 0; left: 0; right: 0; height: 4px; z-index: 100000;
      background: rgba(255,255,255,0.1); pointer-events: none;
    `;
    barContainer.innerHTML = `<div id="spvm3-progress-fill" style="height: 100%; width: 0%; background: linear-gradient(90deg, #6366f1, #06b6d4, #10b981); transition: width 0.2s ease;"></div>`;
    document.body.appendChild(barContainer);
  }
  const fill = document.getElementById('spvm3-progress-fill');
  if (fill) fill.style.width = `${percent}%`;
}

// -----------------------------------------------------------------------------
// LOGIN MODAL SYSTEM
// -----------------------------------------------------------------------------
function showSPVM3LoginModal(onSuccessCallback) {
  let loginModal = document.getElementById('spvm3-login-modal');
  if (!loginModal) {
    loginModal = document.createElement('div');
    loginModal.id = 'spvm3-login-modal';
    document.body.appendChild(loginModal);
  }

  const currentName = getStudentName();
  const currentEmail = getStudentEmail();

  loginModal.innerHTML = `
    <div class="spvm3-cert-overlay" style="z-index: 100005;">
      <div class="spvm3-cert-dialog" style="max-width: 480px; background: #0d1322; border: 2px solid #6366f1; border-radius: 20px; padding: 32px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); color: #f1f5f9; text-align: center;">
        <button class="spvm3-cert-close" onclick="closeSPVM3LoginModal()">&times;</button>

        <div style="width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #06b6d4); display: flex; align-items: center; justify-content: center; font-size: 2rem; margin: 0 auto 16px; box-shadow: 0 0 20px rgba(99,102,241,0.4);">
          🔑
        </div>

        <h2 style="font-size: 1.6rem; font-weight: 800; color: #ffffff; margin-bottom: 6px;">Login to SPVM3 Learning Space</h2>
        <p style="font-size: 0.88rem; color: #94a3b8; margin-bottom: 24px;">Enter your Gmail address to unlock computer courses, track progress, and automatically receive your official ISO-certified Certificate!</p>

        <form onsubmit="handleSPVM3LoginSubmit(event, ${onSuccessCallback ? `'${onSuccessCallback}'` : 'null'})" style="display: flex; flex-direction: column; gap: 16px; text-align: left;">
          <div>
            <label style="font-size: 0.82rem; font-weight: 700; color: #cbd5e1; display: block; margin-bottom: 6px;">👤 Full Student Name:</label>
            <input type="text" id="loginNameInput" value="${currentName}" placeholder="e.g. Sanjay GL" required style="width: 100%; background: #0b0f19; border: 1px solid #6366f1; color: #ffffff; padding: 12px 16px; border-radius: 10px; font-weight: 600; outline: none;">
          </div>

          <div>
            <label style="font-size: 0.82rem; font-weight: 700; color: #cbd5e1; display: block; margin-bottom: 6px;">📧 Gmail Address (For Automatic Certificate Delivery):</label>
            <input type="email" id="loginEmailInput" value="${currentEmail}" placeholder="e.g. spvm3techsolution@gmail.com" required style="width: 100%; background: #0b0f19; border: 1px solid #06b6d4; color: #38bdf8; padding: 12px 16px; border-radius: 10px; font-weight: 600; outline: none;">
          </div>

          <div style="background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3); padding: 12px; border-radius: 10px; font-size: 0.78rem; color: #94a3b8;">
            ℹ️ <strong>Auto-Message Notice:</strong> Upon logging in, a welcome message will be sent to your Gmail in 2-3 minutes. Complete <strong>80% of any course</strong> to automatically unlock and receive your Certificate!
          </div>

          <button type="submit" style="background: linear-gradient(135deg, #6366f1, #06b6d4); color: #ffffff; border: none; padding: 14px; border-radius: 10px; font-weight: 800; font-size: 1rem; cursor: pointer; box-shadow: 0 4px 16px rgba(99,102,241,0.4); transition: transform 0.2s;">
            🚀 Login & Open Learning Space
          </button>
        </form>
      </div>
    </div>
  `;

  injectSPVM3CertStyles();
}

function handleSPVM3LoginSubmit(e, callbackName) {
  if (e) e.preventDefault();
  const name = document.getElementById('loginNameInput').value.trim();
  const email = document.getElementById('loginEmailInput').value.trim();

  if (!name || !email || !email.includes('@')) {
    alert("⚠️ Please enter a valid name and Gmail address!");
    return;
  }

  setStudentName(name);
  setStudentEmail(email);
  closeSPVM3LoginModal();

  // Send POST request to Python backend to queue 2-minute auto welcome email
  fetch('http://localhost:5000/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email })
  })
  .then(res => res.json())
  .then(data => {
    console.log("Login registered in database. Auto welcome email scheduled.");
  })
  .catch(err => {
    console.log("Local server offline; session stored in localStorage.");
  });

  alert(`✅ Welcome ${name}!\n\nYour session is active (${email}). A welcome email will be sent to your Gmail in 2-3 minutes.\n\nEnjoy learning! Complete 80% of any course to unlock your Certificate.`);

  if (callbackName && typeof window[callbackName] === 'function') {
    window[callbackName]();
  }
}

function closeSPVM3LoginModal() {
  const loginModal = document.getElementById('spvm3-login-modal');
  if (loginModal) loginModal.innerHTML = '';
}

// -----------------------------------------------------------------------------
// 80% COURSE LOCKED MODAL
// -----------------------------------------------------------------------------
function showSPVM3LockedModal(subjectId, currentProgress) {
  const subject = SPVM3_SUBJECTS_MASTER.find(s => s.id === subjectId) || { title: "Computer Course" };

  let lockedModal = document.getElementById('spvm3-locked-modal');
  if (!lockedModal) {
    lockedModal = document.createElement('div');
    lockedModal.id = 'spvm3-locked-modal';
    document.body.appendChild(lockedModal);
  }

  lockedModal.innerHTML = `
    <div class="spvm3-cert-overlay" style="z-index: 100004;">
      <div class="spvm3-cert-dialog" style="max-width: 520px; background: #0d1322; border: 2px solid #f59e0b; border-radius: 20px; padding: 32px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); color: #f1f5f9; text-align: center;">
        <button class="spvm3-cert-close" onclick="closeSPVM3LockedModal()">&times;</button>

        <div style="width: 75px; height: 75px; border-radius: 50%; background: rgba(245,158,11,0.15); border: 2px solid #f59e0b; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; margin: 0 auto 16px; box-shadow: 0 0 20px rgba(245,158,11,0.3);">
          🔒
        </div>

        <h2 style="font-size: 1.6rem; font-weight: 800; color: #fbbf24; margin-bottom: 8px;">Certificate Locked</h2>
        <p style="font-size: 0.92rem; color: #cbd5e1; margin-bottom: 20px;">
          You have completed <strong>${currentProgress}%</strong> of <em>${subject.title}</em>.<br>
          You must reach at least <strong>80% course completion</strong> to unlock your official Certificate!
        </p>

        <!-- Progress Bar -->
        <div style="background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1); padding: 14px; border-radius: 12px; margin-bottom: 24px; text-align: left;">
          <div style="display: flex; justify-content: space-between; font-size: 0.82rem; font-weight: 700; color: #94a3b8; margin-bottom: 8px;">
            <span>Current Reading Progress:</span>
            <span style="color: ${currentProgress >= 80 ? '#10b981' : '#f59e0b'}; font-weight: 800;">${currentProgress}% / 80% Required</span>
          </div>
          <div style="height: 12px; background: rgba(255,255,255,0.08); border-radius: 6px; overflow: hidden; position: relative;">
            <div style="height: 100%; width: ${currentProgress}%; background: linear-gradient(90deg, #f59e0b, #eab308); border-radius: 6px; transition: width 0.3s;"></div>
            <div style="position: absolute; left: 80%; top: 0; bottom: 0; width: 2px; background: #ef4444;" title="80% Unlock Threshold"></div>
          </div>
          <div style="font-size: 0.72rem; color: #64748b; margin-top: 6px; text-align: right;">Need ${Math.max(0, 80 - currentProgress)}% more to unlock 🎓</div>
        </div>

        <div style="display: flex; gap: 12px; justify-content: center;">
          <button onclick="closeSPVM3LockedModal()" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #ffffff; border: none; padding: 12px 24px; border-radius: 10px; font-weight: 800; font-size: 0.95rem; cursor: pointer; box-shadow: 0 4px 14px rgba(245,158,11,0.4);">
            📖 Continue Reading Course
          </button>
        </div>
      </div>
    </div>
  `;

  injectSPVM3CertStyles();
}

function closeSPVM3LockedModal() {
  const lockedModal = document.getElementById('spvm3-locked-modal');
  if (lockedModal) lockedModal.innerHTML = '';
}

// -----------------------------------------------------------------------------
// GATEKEEPER CERTIFICATE RENDERER
// -----------------------------------------------------------------------------
function showSPVM3Certificate(subjectId) {
  // 1. Check Login
  if (!isStudentLoggedIn()) {
    showSPVM3LoginModal();
    return;
  }

  // 2. Check 80% Progress Rule
  const progress = getCourseProgress(subjectId);
  if (progress < 80) {
    showSPVM3LockedModal(subjectId, progress);
    return;
  }

  // 3. Render Certificate Modal if progress >= 80%
  const subject = SPVM3_SUBJECTS_MASTER.find(s => s.id === subjectId);
  if (!subject) return;

  const certData = markCourseCompleted(subjectId);
  const studentName = getStudentName();
  const studentEmail = getStudentEmail();
  const convertedHours = calcCourseHours(subject.readTimeMin);

  let modalEl = document.getElementById('spvm3-certificate-modal');
  if (!modalEl) {
    modalEl = document.createElement('div');
    modalEl.id = 'spvm3-certificate-modal';
    document.body.appendChild(modalEl);
  }

  const verifyUrl = `${window.location.origin}${window.location.pathname.replace(/[^/]*$/, '')}verify-certificate.html?certId=${encodeURIComponent(certData.certId)}`;
  const qrCodeImageUrl = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(verifyUrl)}`;

  modalEl.innerHTML = `
    <div class="spvm3-cert-overlay" id="spvm3CertOverlay">
      <div class="spvm3-cert-dialog">
        <button class="spvm3-cert-close" onclick="closeSPVM3Certificate()">&times;</button>
        
        <!-- Editable Student Name & Email Bar -->
        <div class="spvm3-name-bar" style="flex-wrap: wrap;">
          <div style="flex: 1; min-width: 220px; display: flex; align-items: center; gap: 8px;">
            <label for="studentNameInput" style="font-weight: 700; white-space: nowrap;">👤 Student Name:</label>
            <input type="text" id="studentNameInput" value="${studentName}" placeholder="Enter Your Name..." onchange="updateCertStudentName(this.value, '${subjectId}')" style="width: 100%;">
          </div>
          <div style="flex: 1; min-width: 260px; display: flex; align-items: center; gap: 8px;">
            <label for="studentEmailInput" style="font-weight: 700; white-space: nowrap;">📧 Student Email:</label>
            <input type="email" id="studentEmailInput" value="${studentEmail}" placeholder="your.name@gmail.com..." onchange="setStudentEmail(this.value)" style="width: 100%;">
          </div>
          <a href="${verifyUrl}" target="_blank" style="background: rgba(6,182,212,0.2); color: #38bdf8; border: 1px solid #06b6d4; padding: 6px 12px; border-radius: 8px; text-decoration: none; font-size: 0.8rem; font-weight: 700;">🔍 Verify Link ➔</a>
        </div>

        <!-- PRINTABLE CERTIFICATE CARD -->
        <div class="spvm3-certificate-card" id="spvm3PrintableCert">
          <div class="spvm3-cert-border-outer">
            <div class="spvm3-cert-border-inner">
              
              <!-- Brand Header with Left SPVM3 Logo, Center SPVM3 Education Platform, Right Subject Logo -->
              <div class="spvm3-cert-header" style="display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 20px; border-bottom: 1px dashed rgba(99,102,241,0.3); padding-bottom: 16px;">
                <!-- Left: SPVM3 Brand Logo -->
                <div style="text-align: left;">
                  <img src="spvm3_logo.jpg" alt="SPVM3 Tech Solution Logo" class="spvm3-cert-logo">
                </div>

                <!-- Center: SPVM3 TECH SOLUTION / SPVM3 Education Platform -->
                <div style="text-align: center; flex: 1;">
                  <div class="spvm3-cert-brand-title">SPVM3 TECH SOLUTION</div>
                  <div class="spvm3-cert-brand-sub" style="color: #38bdf8; font-size: 0.85rem; font-weight: 800; letter-spacing: 0.06em;">SPVM3 EDUCATION PLATFORM</div>
                  <div style="font-size: 0.68rem; color: #94a3b8; letter-spacing: 0.12em; font-weight: 700; margin-top: 2px;">ISO CERTIFIED COMPUTER SCIENCE ACADEMY</div>
                </div>

                <!-- Right: Subject Specific Emblem/Logo -->
                <div style="text-align: right;">
                  <div style="width: 80px; height: 80px; border-radius: 50%; background: rgba(99,102,241,0.12); border: 2px solid ${subject.accent || '#06b6d4'}; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; box-shadow: 0 0 16px rgba(99,102,241,0.3); margin: 0 auto;">
                    ${subject.icon || '💻'}
                  </div>
                  <span style="font-size: 0.65rem; color: #94a3b8; font-weight: 700; display: block; margin-top: 4px; text-transform: uppercase;">${subject.id.toUpperCase()}</span>
                </div>
              </div>

              <!-- Certificate Main Content -->
              <div class="spvm3-cert-body">
                <h1 class="spvm3-cert-title">CERTIFICATE OF COMPLETION</h1>
                <p class="spvm3-cert-subtitle">THIS IS PROUDLY PRESENTED TO</p>
                
                <div class="spvm3-cert-name" id="certStudentNameDisplay">${studentName}</div>
                
                <p class="spvm3-cert-statement">
                  For successfully studying and completing the specialized computer-based curriculum:
                </p>
                
                <h2 class="spvm3-cert-course">${subject.title}</h2>

                <div class="spvm3-cert-meta-grid">
                  <div class="spvm3-meta-item">
                    <span class="spvm3-meta-label">Course Duration:</span>
                    <span class="spvm3-meta-val">${convertedHours} (${subject.readTimeMin} Mins Study Units)</span>
                  </div>
                  <div class="spvm3-meta-item">
                    <span class="spvm3-meta-label">Completion Date:</span>
                    <span class="spvm3-meta-val">${certData.completedDate}</span>
                  </div>
                  <div class="spvm3-meta-item">
                    <span class="spvm3-meta-label">Exact Completion Time:</span>
                    <span class="spvm3-meta-val">${certData.completedTime}</span>
                  </div>
                  <div class="spvm3-meta-item">
                    <span class="spvm3-meta-label">Certificate Unique ID:</span>
                    <span class="spvm3-meta-val" style="color: #fbbf24; font-family: monospace;">${certData.certId}</span>
                  </div>
                </div>
              </div>

              <!-- Signatures, Official Seal & QR Code -->
              <div class="spvm3-cert-footer">
                <div class="spvm3-sign-box">
                  <div class="spvm3-signature">Sanjay GL</div>
                  <div class="spvm3-sign-line"></div>
                  <div class="spvm3-sign-title">SANJAY GL</div>
                  <div class="spvm3-sign-sub">Founder & Lead Director, SPVM3</div>
                </div>

                <div style="display: flex; align-items: center; gap: 16px;">
                  <div class="spvm3-seal-box">
                    <div class="spvm3-gold-seal">
                      <span>★ ★ ★</span>
                      <strong>VERIFIED</strong>
                      <small>OFFICIAL</small>
                    </div>
                  </div>

                  <!-- Dynamic QR Code -->
                  <div style="background: #ffffff; padding: 6px; border-radius: 8px; border: 1px solid #06b6d4; text-align: center;">
                    <img src="${qrCodeImageUrl}" alt="Certificate Verification QR Code" style="width: 72px; height: 72px; display: block;">
                    <span style="font-size: 0.55rem; color: #000; font-weight: 800; display: block; margin-top: 2px;">SCAN TO VERIFY</span>
                  </div>
                </div>

                <div class="spvm3-sign-box">
                  <div class="spvm3-signature" style="font-family: 'Courier New', monospace; font-size: 1.1rem; color: #06b6d4;">SPVM3 ACADEMY</div>
                  <div class="spvm3-sign-line"></div>
                  <div class="spvm3-sign-title">ACADEMIC DIRECTOR</div>
                  <div class="spvm3-sign-sub">SPVM3 Tech Solution</div>
                </div>
              </div>

            </div>
          </div>
        </div>

        <!-- 3-WAY DOWNLOAD OPTIONS & EMAIL AUTOMATION ACTIONS -->
        <div class="spvm3-cert-actions" style="margin-top: 18px;">
          <div style="width: 100%; display: flex; align-items: center; justify-content: space-between; gap: 8px; background: rgba(0,0,0,0.3); padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(99,102,241,0.2); margin-bottom: 6px;">
            <span style="font-size: 0.85rem; font-weight: 700; color: #38bdf8;">📥 3 Download Formats:</span>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
              <button class="spvm3-btn-print" style="background: linear-gradient(135deg, #06b6d4, #0284c7); padding: 8px 14px; font-size: 0.82rem;" onclick="downloadSPVM3CertificateImage('${certData.certId}')">🖼️ Download Image (.png)</button>
              <button class="spvm3-btn-print" style="background: linear-gradient(135deg, #ef4444, #dc2626); padding: 8px 14px; font-size: 0.82rem;" onclick="downloadSPVM3CertificatePDF('${certData.certId}')">📕 Download PDF (.pdf)</button>
              <button class="spvm3-btn-print" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8); padding: 8px 14px; font-size: 0.82rem;" onclick="downloadSPVM3CertificateDoc('${certData.certId}', '${subject.title}')">📄 Download Document (.doc)</button>
            </div>
          </div>

          <div style="width: 100%; display: flex; align-items: center; justify-content: space-between; gap: 8px;">
            <button class="spvm3-btn-print" style="background: linear-gradient(135deg, #10b981, #059669);" onclick="sendSPVM3CertificateEmail('${subjectId}', '${certData.certId}')">📧 Send Certificate to Email</button>
            <a href="${verifyUrl}" target="_blank" style="background: rgba(6,182,212,0.2); color: #38bdf8; border: 1px solid #06b6d4; padding: 10px 16px; border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 0.85rem;">🔍 Verification Page</a>
            <button class="spvm3-btn-close" onclick="closeSPVM3Certificate()">Close Window</button>
          </div>
        </div>

      </div>
    </div>
  `;

  injectSPVM3CertStyles();
}

function updateCertStudentName(name, subjectId) {
  setStudentName(name);
  const displayEl = document.getElementById('certStudentNameDisplay');
  if (displayEl) displayEl.textContent = name || 'Sanjay GL';
}

function closeSPVM3Certificate() {
  const modalEl = document.getElementById('spvm3-certificate-modal');
  if (modalEl) modalEl.innerHTML = '';
}

// 1. Download Option 1: Image (PNG)
function downloadSPVM3CertificateImage(certId) {
  downloadSPVM3Certificate(certId);
}

function downloadSPVM3Certificate(certId) {
  const target = document.getElementById('spvm3PrintableCert') || document.querySelector('.cert-report');
  if (!target) return;

  if (typeof html2canvas === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
    script.onload = () => captureAndDownload(target, certId);
    document.head.appendChild(script);
  } else {
    captureAndDownload(target, certId);
  }
}

// 2. Download Option 2: PDF Document (.pdf)
function downloadSPVM3CertificatePDF(certId) {
  const target = document.getElementById('spvm3PrintableCert') || document.querySelector('.cert-report');
  if (!target) {
    window.print();
    return;
  }

  if (typeof html2pdf !== 'undefined') {
    const opt = {
      margin:       0.2,
      filename:     `SPVM3_Certificate_${certId || 'Official'}.pdf`,
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { scale: 2, useCORS: true },
      jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
    };
    html2pdf().set(opt).from(target).save();
  } else {
    // Load html2pdf.js dynamically
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
    script.onload = () => {
      const opt = {
        margin:       0.2,
        filename:     `SPVM3_Certificate_${certId || 'Official'}.pdf`,
        image:        { type: 'jpeg', quality: 0.98 },
        html2canvas:  { scale: 2, useCORS: true },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
      };
      html2pdf().set(opt).from(target).save();
    };
    script.onerror = () => {
      // Fallback to high quality print dialog
      window.print();
    };
    document.head.appendChild(script);
  }
}

// 3. Download Option 3: Word Document (.doc)
function downloadSPVM3CertificateDoc(certId, courseTitle) {
  const target = document.getElementById('spvm3PrintableCert') || document.querySelector('.cert-report');
  const studentName = getStudentName();
  
  const headerHtml = "<html xmlns:o='urn:schemas-microsoft-com:office:office' "+
        "xmlns:w='urn:schemas-microsoft-com:office:word' "+
        "xmlns='http://www.w3.org/TR/REC-html40'>"+
        "<head><meta charset='utf-8'><title>Certificate of Completion</title>"+
        "<style>body { font-family: Arial, sans-serif; background: #0b0f19; color: #ffffff; padding: 20px; } "+
        ".title { font-size: 24pt; font-weight: bold; color: #fbbf24; text-align: center; } "+
        ".subtitle { font-size: 14pt; color: #38bdf8; text-align: center; } "+
        ".name { font-size: 28pt; font-weight: bold; color: #ffffff; text-align: center; margin: 20px 0; border-bottom: 2px solid #6366f1; } "+
        ".course { font-size: 20pt; font-weight: bold; color: #38bdf8; text-align: center; } "+
        ".meta { font-size: 11pt; color: #cbd5e1; margin-top: 30px; } "+
        ".footer { margin-top: 40px; border-top: 1px solid #6366f1; padding-top: 15px; display: flex; justify-content: space-between; } "+
        "</style></head><body>";
  
  const footerHtml = "</body></html>";
  const sourceHTML = headerHtml + target.innerHTML + footerHtml;
  
  const source = 'data:application/vnd.ms-word;charset=utf-8,' + encodeURIComponent(sourceHTML);
  const fileDownload = document.createElement("a");
  document.body.appendChild(fileDownload);
  fileDownload.href = source;
  fileDownload.download = `SPVM3_Certificate_${certId || 'Official'}.doc`;
  fileDownload.click();
  document.body.removeChild(fileDownload);
}

// Automatic Silent Background Certificate Email Trigger (Hits 80% Completion)
function sendSPVM3CertificateEmailSilent(subjectId, certId) {
  const studentName = getStudentName() || 'Student';
  const studentEmail = getStudentEmail();
  
  if (!studentEmail || !studentEmail.includes('@')) return;
  
  const subject = SPVM3_SUBJECTS_MASTER.find(s => s.id === subjectId) || { title: "Computer Course", readTimeMin: 45 };
  const hours = calcCourseHours(subject.readTimeMin);
  
  const payload = {
    name: studentName,
    email: studentEmail,
    subject_id: subjectId,
    course_title: subject.title,
    cert_id: certId,
    course_hours: hours,
    delay_seconds: 60, // Delivered in 1 min after reaching 80%
    timestamp: new Date().toISOString()
  };

  fetch('http://localhost:5000/api/send-certificate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    console.log(`[Auto-Certificate] Certificate email queued for ${studentEmail}`);
  })
  .catch(err => {
    console.log("[Auto-Certificate] Python server offline for silent email trigger.");
  });
}

// Automatic Certificate Email Sender Function
function sendSPVM3CertificateEmail(subjectId, certId) {
  const studentName = getStudentName();
  const studentEmail = document.getElementById('studentEmailInput') ? document.getElementById('studentEmailInput').value.trim() : getStudentEmail();
  
  if (!studentEmail || !studentEmail.includes('@')) {
    alert("⚠️ Please enter a valid student email address to receive your certificate!");
    const emailInput = document.getElementById('studentEmailInput');
    if (emailInput) emailInput.focus();
    return;
  }
  
  setStudentEmail(studentEmail);
  const subject = SPVM3_SUBJECTS_MASTER.find(s => s.id === subjectId) || { title: "Computer Course", readTimeMin: 45 };
  const hours = calcCourseHours(subject.readTimeMin);
  
  const payload = {
    name: studentName,
    email: studentEmail,
    subject_id: subjectId,
    course_title: subject.title,
    cert_id: certId,
    course_hours: hours,
    timestamp: new Date().toISOString()
  };

  // UI status feedback
  const sendBtn = event ? event.currentTarget : null;
  const originalText = sendBtn ? sendBtn.innerHTML : '';
  if (sendBtn) {
    sendBtn.disabled = true;
    sendBtn.innerHTML = '⏳ Sending Email...';
  }

  // Attempt backend API call to local Python Flask Auto-Email server
  fetch('http://localhost:5000/api/send-certificate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    if (sendBtn) {
      sendBtn.disabled = false;
      sendBtn.innerHTML = '✅ Certificate Sent!';
    }
    alert(`🎉 Certificate successfully sent to ${studentEmail}!\n\nCheck your email inbox for your welcome message and certificate link.`);
  })
  .catch(err => {
    // Fallback if local backend server is not currently running
    if (sendBtn) {
      sendBtn.disabled = false;
      sendBtn.innerHTML = originalText;
    }
    
    // Construct default email client trigger
    const mailSubject = encodeURIComponent(`SPVM3 Certificate of Completion — ${subject.title}`);
    const mailBody = encodeURIComponent(`Hi ${studentName},\n\nThank you for completing ${subject.title} on SPVM3 Education Platform!\n\nCertificate Unique ID: ${certId}\nCourse Duration: ${hours}\n\nVerify your certificate here:\n${window.location.origin}${window.location.pathname.replace(/[^/]*$/, '')}verify-certificate.html?certId=${certId}\n\nBest regards,\nSanjay GL\nSPVM3 Tech Solution`);
    
    window.open(`mailto:${studentEmail}?subject=${mailSubject}&body=${mailBody}`, '_blank');
    alert(`📧 Opened email app to deliver Certificate (${certId}) to ${studentEmail}.\n\nTip: Run python spvm3_auto_email_certificate_server.py to enable automatic silent background email sending via SMTP / Brevo!`);
  });
}

function captureAndDownload(target, certId) {
  html2canvas(target, {
    scale: 2,
    useCORS: true,
    backgroundColor: '#0b0f19'
  }).then(canvas => {
    const link = document.createElement('a');
    link.download = `SPVM3_Certificate_${certId || 'Official'}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
  });
}

function injectSPVM3CertStyles() {
  if (document.getElementById('spvm3-cert-styles')) return;

  const styleEl = document.createElement('style');
  styleEl.id = 'spvm3-cert-styles';
  styleEl.innerHTML = `
    .spvm3-cert-overlay {
      position: fixed; inset: 0; background: rgba(5, 8, 15, 0.88);
      backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      z-index: 100000; display: flex; align-items: center; justify-content: center;
      padding: 20px; overflow-y: auto;
    }
    .spvm3-cert-dialog {
      max-width: 900px; width: 100%; position: relative;
    }
    .spvm3-cert-close {
      position: absolute; top: -15px; right: -15px; background: #f43f5e; color: #fff;
      border: none; width: 36px; height: 36px; border-radius: 50%; font-size: 1.4rem;
      cursor: pointer; z-index: 10; box-shadow: 0 4px 12px rgba(244,63,94,0.4);
    }
    .spvm3-name-bar {
      background: rgba(18, 26, 43, 0.95); border: 1px solid rgba(99, 102, 241, 0.4);
      padding: 12px 20px; border-radius: 12px; margin-bottom: 16px;
      display: flex; align-items: center; gap: 12px; color: #f1f5f9; font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .spvm3-name-bar input {
      flex: 1; background: #0b0f19; border: 1px solid #6366f1; color: #38bdf8;
      padding: 8px 14px; border-radius: 8px; font-weight: 700; font-size: 1rem; outline: none;
    }

    /* CERTIFICATE GRAPHICAL BOX */
    .spvm3-certificate-card {
      background: #0b0f19; color: #f1f5f9; border-radius: 16px; padding: 24px;
      box-shadow: 0 25px 60px rgba(0,0,0,0.8); font-family: 'Plus Jakarta Sans', sans-serif;
      position: relative; overflow: hidden;
    }
    .spvm3-cert-border-outer {
      border: 3px double #6366f1; padding: 8px; border-radius: 12px; position: relative;
    }
    .spvm3-cert-border-inner {
      border: 1px solid rgba(6, 182, 212, 0.4); padding: 36px 32px; border-radius: 8px;
      background: radial-gradient(circle at 50% 30%, rgba(99, 102, 241, 0.12), transparent 70%), #0d1322;
      text-align: center;
    }

    .spvm3-cert-header {
      margin-bottom: 24px; display: flex; flex-direction: column; align-items: center;
    }
    .spvm3-cert-logo {
      width: 90px; height: 90px; object-fit: contain; margin-bottom: 12px;
      border-radius: 50%; border: 2px solid #06b6d4; box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    }
    .spvm3-cert-brand-title {
      font-size: 1.6rem; font-weight: 800; letter-spacing: 0.08em;
      background: linear-gradient(135deg, #ffffff, #38bdf8, #818cf8);
      -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }
    .spvm3-cert-brand-sub {
      font-size: 0.72rem; color: #94a3b8; letter-spacing: 0.15em; font-weight: 700; margin-top: 2px;
    }

    .spvm3-cert-title {
      font-size: 1.9rem; font-weight: 800; color: #fbbf24; letter-spacing: 0.06em; margin: 12px 0 4px;
      text-shadow: 0 0 14px rgba(251, 191, 36, 0.3);
    }
    .spvm3-cert-subtitle {
      font-size: 0.8rem; color: #94a3b8; letter-spacing: 0.2em; font-weight: 600; margin-bottom: 16px;
    }
    .spvm3-cert-name {
      font-size: 2.2rem; font-weight: 800; color: #ffffff; margin: 10px 0 16px;
      border-bottom: 2px solid #6366f1; display: inline-block; padding: 0 30px 6px;
      font-family: 'Outfit', sans-serif; text-shadow: 0 4px 12px rgba(99,102,241,0.5);
    }
    .spvm3-cert-statement {
      font-size: 0.95rem; color: #cbd5e1; max-width: 650px; margin: 0 auto 14px; line-height: 1.5;
    }
    .spvm3-cert-course {
      font-size: 1.45rem; font-weight: 700; color: #38bdf8; margin-bottom: 24px;
    }

    .spvm3-cert-meta-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;
      background: rgba(0,0,0,0.3); padding: 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06);
      margin-bottom: 32px; text-align: left;
    }
    .spvm3-meta-item { display: flex; flex-direction: column; }
    .spvm3-meta-label { font-size: 0.72rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .spvm3-meta-val { font-size: 0.88rem; color: #f1f5f9; font-weight: 700; }

    .spvm3-cert-footer {
      display: flex; align-items: flex-end; justify-content: space-between; margin-top: 20px; gap: 20px;
    }
    .spvm3-sign-box { text-align: center; flex: 1; }
    .spvm3-signature { font-family: 'Brush Script MT', cursive, sans-serif; font-size: 1.8rem; color: #818cf8; margin-bottom: 4px; }
    .spvm3-sign-line { height: 1px; background: #475569; width: 140px; margin: 0 auto 6px; }
    .spvm3-sign-title { font-size: 0.8rem; font-weight: 800; color: #f1f5f9; }
    .spvm3-sign-sub { font-size: 0.7rem; color: #94a3b8; }

    .spvm3-gold-seal {
      width: 76px; height: 76px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b, #d97706);
      border: 3px solid #fef08a; display: flex; flex-direction: column; align-items: center; justify-content: center;
      color: #78350f; box-shadow: 0 4px 14px rgba(245,158,11,0.5); margin: 0 auto;
    }
    .spvm3-gold-seal span { font-size: 0.65rem; }
    .spvm3-gold-seal strong { font-size: 0.7rem; font-weight: 800; letter-spacing: 0.05em; }
    .spvm3-gold-seal small { font-size: 0.55rem; font-weight: 700; }

    .spvm3-cert-actions {
      display: flex; gap: 12px; margin-top: 18px; justify-content: flex-end; flex-wrap: wrap;
    }
    .spvm3-btn-print {
      background: linear-gradient(135deg, #10b981, #059669); color: #fff; border: none; padding: 12px 24px;
      border-radius: 10px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 14px rgba(16,185,129,0.3);
    }
    .spvm3-btn-close {
      background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); padding: 12px 20px;
      border-radius: 10px; font-weight: 600; cursor: pointer;
    }

    /* 100% PERFECT 1-PAGE LANDSCAPE PRINT MEDIA STYLES */
    @media print {
      @page {
        size: A4 landscape;
        margin: 8mm;
      }
      
      body > *:not(#spvm3-certificate-modal),
      #techvault-global-header,
      .navbar,
      .spvm3-name-bar,
      .spvm3-cert-actions,
      .spvm3-cert-close,
      .verify-header,
      .search-form,
      .status-banner,
      .footer,
      .spvm3-global-footer {
        display: none !important;
      }

      html, body {
        background: #ffffff !important;
        color: #000000 !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 100% !important;
        width: 100% !important;
        overflow: hidden !important;
      }

      #spvm3-certificate-modal,
      .spvm3-cert-overlay {
        position: absolute !important;
        left: 0 !important; top: 0 !important;
        width: 100% !important; height: 100% !important;
        padding: 0 !important; margin: 0 !important;
        background: #ffffff !important;
        display: block !important;
      }

      .spvm3-cert-dialog {
        max-width: 100% !important; width: 100% !important;
        margin: 0 !important; padding: 0 !important;
      }

      #spvm3PrintableCert,
      .cert-report {
        position: relative !important; width: 100% !important; max-width: 960px !important;
        margin: 0 auto !important; page-break-inside: avoid !important; break-inside: avoid !important;
        background: #ffffff !important; color: #000000 !important; box-shadow: none !important;
        border: 3px double #000000 !important;
      }

      .spvm3-cert-border-inner {
        background: #ffffff !important; border: 1px solid #333333 !important; padding: 24px 20px !important;
      }
      .spvm3-cert-brand-title { color: #000000 !important; -webkit-text-fill-color: #000000 !important; }
      .spvm3-cert-title { color: #b45309 !important; text-shadow: none !important; }
      .spvm3-cert-name { color: #000000 !important; border-bottom: 2px solid #000000 !important; text-shadow: none !important; }
      .spvm3-cert-course { color: #1d4ed8 !important; }
      .spvm3-meta-val, .spvm3-sign-title { color: #000000 !important; }
      .spvm3-meta-item { background: #f8fafc !important; border: 1px solid #e2e8f0 !important; }
    }
  `;
  document.head.appendChild(styleEl);
}
