const app = {
    currentUsername: 'Student',
    isLoginMode: true,
    currentTask: null,

    init() {
        this.cacheDOM();
        this.bindEvents();
        this.showApp();
    },

    cacheDOM() {
        // Navigation
        this.navLinks = document.querySelectorAll('.nav-links li');
        this.views = document.querySelectorAll('.view');
        this.pageTitle = document.getElementById('page-title');
        this.navUsername = document.getElementById('nav-username');

        // Courses & Tasks
        this.coursesList = document.getElementById('courses-list');
        this.lessonTitle = document.getElementById('lesson-title');
        this.lessonContent = document.getElementById('lesson-content');
        this.taskTitle = document.getElementById('task-title');
        this.taskQuestion = document.getElementById('task-question');
        // CodeMirror editorini ishga tushirish
        const textArea = document.getElementById('code-editor');
        this.cmEditor = CodeMirror.fromTextArea(textArea, {
            mode: 'python',
            theme: 'dracula',
            lineNumbers: true,
            autoCloseBrackets: true,
            matchBrackets: true,
            styleActiveLine: true,
            indentUnit: 4,
            tabSize: 4,
            indentWithTabs: false,
            lineWrapping: false,
            extraKeys: {
                'Tab': function(cm) {
                    cm.replaceSelection('    ', 'end');
                }
            },
            placeholder: '# Python kodini shu yerga yozing...'
        });
        // Pseudo-reference for legacy code
        this.codeEditor = {
            get value() { return this._cm ? this._cm.getValue() : ''; },
            set value(v) { if (this._cm) this._cm.setValue(v); },
            _cm: this.cmEditor
        };
        this.submitCodeBtn = document.getElementById('submit-code-btn');
        this.submissionResult = document.getElementById('submission-result');
        this.progressTbody = document.getElementById('progress-tbody');
        
        // AI Buttons
        this.btnExplain = document.getElementById('btn-explain');
        this.btnHint = document.getElementById('btn-hint');
        this.btnAnalyze = document.getElementById('btn-analyze');

        // Gamification Elements
        this.dashLevel = document.getElementById('dash-level');
        this.dashLevelName = document.getElementById('dash-level-name');
        this.dashPoints = document.getElementById('dash-points');
        this.dashStreak = document.getElementById('dash-streak');
        this.dashBadges = document.getElementById('dash-badges');
        this.leaderboardTbody = document.getElementById('leaderboard-tbody');
        
        // Stats Elements
        this.statAccuracy = document.getElementById('stat-accuracy');
        this.statTotalSub = document.getElementById('stat-total-sub');
        this.statCorrectSub = document.getElementById('stat-correct-sub');
        this.statFinishedTasks = document.getElementById('stat-finished-tasks');
        this.statsBadgesList = document.getElementById('stats-badges-list');
    },

    bindEvents() {

        this.navLinks.forEach(link => {
            link.addEventListener('click', () => {
                const view = link.getAttribute('data-view');
                if (view) this.switchView(view);
            });
        });

        this.submitCodeBtn.addEventListener('click', () => this.submitTask());
        
        // AI Event Listeners
        this.btnExplain.addEventListener('click', () => this.askAI('explain'));
        this.btnHint.addEventListener('click', () => this.askAI('hint'));
        this.btnAnalyze.addEventListener('click', () => this.askAI('analyze'));

        // AI Hints Toggle (lesson panel)
        const hintsToggle = document.getElementById('btn-toggle-hints');
        if (hintsToggle) {
            hintsToggle.addEventListener('click', () => {
                const hintsBox = document.getElementById('ai-hints');
                if (hintsBox) {
                    const isHidden = hintsBox.classList.contains('hidden');
                    hintsBox.classList.toggle('hidden');
                    hintsToggle.classList.toggle('active', isHidden);
                    hintsToggle.innerHTML = isHidden
                        ? '<i class="fa-solid fa-robot"></i> AI yordamini yashirish'
                        : '<i class="fa-solid fa-robot"></i> AI yordamini ko\'rsatish';
                }
            });
        }

        // AI Toolbar Toggle (code editor panel)
        const aiPanelToggle = document.getElementById('btn-toggle-ai-panel');
        const aiToolbar = document.getElementById('ai-toolbar');
        if (aiPanelToggle && aiToolbar) {
            aiPanelToggle.addEventListener('click', () => {
                const isHidden = aiToolbar.classList.contains('hidden');
                aiToolbar.classList.toggle('hidden');
                aiPanelToggle.classList.toggle('active', isHidden);
            });
        }
    },

    showApp() {
        this.loadDashboard();
    },

    // 401 bo'lganda
    handleUnauth() {
        console.error("Autentifikatsiya xatosi - Demo serverini tekshiring.");
    },

    switchView(viewName) {
        this.navLinks.forEach(l => l.classList.remove('active'));
        const navItem = document.querySelector(`.nav-links li[data-view="${viewName}"]`);
        if (navItem) navItem.classList.add('active');

        this.views.forEach(v => v.classList.remove('active'));
        const viewElem = document.getElementById(`view-${viewName}`);
        if(viewElem) {
            viewElem.classList.add('active');
            
            // CodeMirror yopiq tabda initsializatsiya bo'lsa refresh qilish kerak
            if (viewName === 'editor' && this.cmEditor) {
                setTimeout(() => {
                    this.cmEditor.refresh();
                }, 10);
            }
            
            // Set Titles
            const titles = {
                'dashboard': 'Bosh sahifa',
                'courses': 'Mavjud kurslar',
                'progress': 'Mening vazifalarim',
                'editor': 'Ish maydoni',
                'leaderboard': 'Global reyting',
                'stats': 'Batafsil statistika'
            };
            this.pageTitle.innerText = titles[viewName] || 'PyLearn Akademiyasi';

            // Load logic
            try {
                if (viewName === 'dashboard') this.loadDashboard();
                if (viewName === 'courses') this.loadCourses();
                if (viewName === 'progress') this.loadProgress();
                if (viewName === 'leaderboard') this.loadLeaderboard();
                if (viewName === 'stats') this.loadStats();
            } catch (e) {
                console.error("View yuklashda xato:", e);
            }
        }
    },

    async loadDashboard() {
        try {
            const profile = await api.getGamificationProfile();
            this.dashPoints.innerText = `${profile.xp} XP`;
            this.dashLevel.innerText = `${profile.level}-daraja`;
            this.dashLevelName.innerText = profile.level_name;
            this.dashStreak.innerText = `${profile.streak_days} Kun`;

            // Sidebar username
            const savedUser = localStorage.getItem('username');
            if (savedUser) this.navUsername.innerText = savedUser;

            // Display badges (first 4)
            this.dashBadges.innerHTML = '';
            if (profile.badges && profile.badges.length > 0) {
                profile.badges.slice(0, 4).forEach(ub => {
                    const badge = ub.badge;
                    const div = document.createElement('div');
                    div.className = 'badge-item';
                    div.title = badge.name + ': ' + badge.description;
                    div.innerText = badge.icon;
                    this.dashBadges.appendChild(div);
                });
            } else {
                this.dashBadges.innerHTML = '<p class="empty-msg">Hozircha yutuqlar yo\'q.</p>';
            }
        } catch (e) {
            if (e.message && e.message.includes('401')) return this.handleUnauth();
            console.error("Dashboard ma'lumotlarini yuklashda xato:", e);
        }
    },

    async loadLeaderboard() {
        this.leaderboardTbody.innerHTML = '<tr><td colspan="5">Reyting yuklanmoqda...</td></tr>';
        try {
            const lb = await api.getLeaderboard();
            this.leaderboardTbody.innerHTML = '';

            if (!lb || lb.length === 0) {
                this.leaderboardTbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color: var(--text-muted)">Hali hech kim reyting jadvalida yo\'q.</td></tr>';
                return;
            }
            
            lb.forEach((entry, index) => {
                const tr = document.createElement('tr');
                const rankClass = index < 3 ? `rank-${index + 1}` : '';
                const medals = ['🥇', '🥈', '🥉'];
                const rankDisplay = index < 3 ? medals[index] : `#${index + 1}`;
                tr.innerHTML = `
                    <td class="${rankClass}">${rankDisplay}</td>
                    <td><strong>${entry.username}</strong></td>
                    <td><span class="badge-level">${entry.level_name || (entry.level + '-daraja')}</span></td>
                    <td><i class="fa-solid fa-star" style="color: #f59e0b;"></i> <strong>${entry.xp}</strong> XP</td>
                    <td><i class="fa-solid fa-medal" style="color: var(--primary);"></i> ${entry.badges_count}</td>
                `;
                this.leaderboardTbody.appendChild(tr);
            });
        } catch (e) {
            if (e.message && e.message.includes('401')) return this.handleUnauth();
            this.leaderboardTbody.innerHTML = '<tr><td colspan="5" class="error-msg">Reytingni yuklashda xato yuz berdi.</td></tr>';
        }
    },

    async loadStats() {
        try {
            const [stats, profile] = await Promise.all([
                api.getStats(),
                api.getGamificationProfile()
            ]);

            this.statAccuracy.innerText = `${stats.success_rate}%`;
            this.statTotalSub.innerText = stats.total_submissions;
            this.statCorrectSub.innerText = stats.correct_submissions;
            this.statFinishedTasks.innerText = stats.completed_tasks;

            // Load full badges list
            this.statsBadgesList.innerHTML = '';
            if (profile.badges && profile.badges.length > 0) {
                profile.badges.forEach(ub => {
                    const b = ub.badge;
                    const card = document.createElement('div');
                    card.className = 'badge-card';
                    card.innerHTML = `
                        <span class="icon">${b.icon}</span>
                        <h4>${b.name}</h4>
                        <p>${b.description}</p>
                        <small style="color:var(--primary); font-size:0.7rem;">Olingan sana: ${new Date(ub.earned_at).toLocaleDateString('uz-UZ')}</small>
                    `;
                    this.statsBadgesList.appendChild(card);
                });
            } else {
                this.statsBadgesList.innerHTML = '<p class="empty-msg">Sizda hali yutuqlar yo\'q. O\'rganishda davom eting!</p>';
            }
        } catch (e) {
            if (e.message && e.message.includes('401')) return this.handleUnauth();
            console.error("Statistikani yuklashda xato yuz berdi:", e);
        }
    },

    async loadCourses() {
        this.coursesList.innerHTML = '<p>Kurslar yuklanmoqda...</p>';
        try {
            const [courses, lessons] = await Promise.all([
                api.getCourses(),
                api.getLessons()
            ]);
            
            this.coursesList.innerHTML = '';

            if (!courses || courses.length === 0) {
                this.coursesList.innerHTML = '<p class="empty-msg">Hozircha kurslar mavjud emas. Admin panelidan kurs qo\'shing.</p>';
                return;
            }

            courses.forEach(c => {
                const cLessons = lessons.filter(l => l.course === c.id);
                
                const card = document.createElement('div');
                card.className = 'course-card glass-panel';
                card.innerHTML = `
                    <div class="course-header">
                        <div class="course-icon"><i class="fa-brands fa-python"></i></div>
                        <span style="font-size: 0.8rem; color: var(--primary);">O'qituvchi: ${c.instructor_detail?.username || 'Admin'}</span>
                    </div>
                    <h3>${c.title}</h3>
                    <p>${c.description}</p>
                    <hr style="border: 0; border-top: 1px solid var(--border-glass); margin: 15px 0;">
                    <div class="course-lessons">
                        ${cLessons.length === 0 ? '<p style="font-size:0.8rem; color:var(--text-muted)">Hozircha darslar yo\'q</p>' : ''}
                    </div>
                `;
                
                const lessonsContainer = card.querySelector('.course-lessons');
                cLessons.forEach(l => {
                    const lCard = document.createElement('div');
                    lCard.className = 'lesson-card';
                    lCard.innerHTML = `<i class="fa-solid fa-play" style="font-size: 0.7rem; margin-right: 8px;"></i> ${l.title}`;
                    lCard.onclick = () => this.openLesson(l);
                    lessonsContainer.appendChild(lCard);
                });
                
                this.coursesList.appendChild(card);
            });
        } catch (e) {
            if (e.message && e.message.includes('401')) return this.handleUnauth();
            this.coursesList.innerHTML = '<p class="error-msg">Kurslarni yuklab bo\'lmadi. Backend ishlayaptimi?</p>';
        }
    },

    async openLesson(lesson) {
        this.switchView('editor');
        this.lessonTitle.innerText = lesson.title;
        this.lessonContent.innerHTML = lesson.content || "Mavzu bo'yicha ma'lumot yuklanmoqda...";
        // VS Code stilida kod bloklarni bo'yash
        syntaxHighlighter.highlight(this.lessonContent);
        
        const taskTabs = document.getElementById('task-tabs');
        if (taskTabs) taskTabs.innerHTML = '';
        const hintsBox = document.getElementById('ai-hints');
        
        if (lesson.tasks && lesson.tasks.length > 0) {
            lesson.tasks.forEach((task, index) => {
                const btn = document.createElement('button');
                btn.className = 'task-tab-btn' + (index === 0 ? ' active' : '');
                btn.innerText = (index + 1) + "-topshiriq";
                btn.onclick = () => {
                    document.querySelectorAll('.task-tab-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    this.renderTask(task);
                };
                if (taskTabs) taskTabs.appendChild(btn);
            });
            this.renderTask(lesson.tasks[0]);
        } else {
            this.taskTitle.innerText = "Vazifalar yo'q";
            this.taskQuestion.innerText = "Ushbu dars uchun hozircha vazifalar mavjud emas.";
            this.currentTask = null;
            hintsBox.classList.add('hidden');
        }
    },

    renderTask(task) {
        this.currentTask = task;
        const hintsBox = document.getElementById('ai-hints');
        const hintsToggle = document.getElementById('btn-toggle-hints');
        this.taskTitle.innerText = task.title;
        this.taskQuestion.innerText = task.question;
        this.cmEditor.setValue('');
        this.cmEditor.clearHistory();
        this.submissionResult.className = 'terminal-output';
        this.submissionResult.innerHTML = 'Kutilmoqda...';
        
        // Always hide hints initially, user decides to show
        hintsBox.classList.add('hidden');
        if (hintsToggle) {
            hintsToggle.classList.remove('active');
            hintsToggle.innerHTML = '<i class="fa-solid fa-robot"></i> AI yordamini ko\'rsatish';
        }

        if (task.ai_hints) {
            document.getElementById('hint-text').innerText = task.ai_hints;
            if (hintsToggle) hintsToggle.style.display = 'inline-flex';
        } else {
            if (hintsToggle) hintsToggle.style.display = 'none';
        }
    },


    async submitTask() {
        if (!this.currentTask) return alert("Avval darsni tanlang!");
        
        const code = this.cmEditor.getValue();
        if (!code.trim()) return alert("Iltimos, kod yozing!");
        
        this.submissionResult.className = 'terminal-output';
        this.submissionResult.innerHTML = 'Mantiq tekshirilmoqda... <i class="fa-solid fa-spinner fa-spin"></i>';
        
        try {
            const res = await api.submitCode(this.currentTask.id, code);
            
            if (res.is_correct) {
                let badgeMsg = "";
                if (res.new_badges && res.new_badges.length > 0) {
                    badgeMsg = `<br><br><span style="color:#f59e0b"><i class="fa-solid fa-medal"></i> YANGI YUTUQ: ${res.new_badges.join(', ')}!</span>`;
                }
                this.submissionResult.innerHTML = `<span style="color:#4ade80">Muvaffaqiyatli! Kompilyatsiya muvaffaqiyatli o'tdi.</span><br><span style="color:var(--primary)">+${res.xp_earned} XP to'plandi</span>${badgeMsg}<br><br>Natija: <br>${res.ai_feedback || ""}`;
            } else {
                this.submissionResult.className = 'terminal-output error';
                this.submissionResult.innerHTML = `Xato.<br>Xatolik: ${res.ai_feedback || "Sintaktik xato."}`;
            }
        } catch(e) {
            this.submissionResult.className = 'terminal-output error';
            this.submissionResult.innerHTML = 'Backend bilan bog\'lanishda xato yuz berdi.';
        }
    },

    async askAI(type) {
        if (!this.currentTask) return alert("Avval masalani tanlang.");
        const code = this.cmEditor.getValue();
        
        if (!code.trim() && type === 'explain') return alert("Tushuntirish uchun kod yozing.");
        
        let payload = { code: code, task_question: this.currentTask.question };
        
        if (type === 'analyze') {
            const terminalText = this.submissionResult.innerText;
            const hasErrorClass = this.submissionResult.classList.contains('error');
            const lowerText = terminalText.toLowerCase();
            const hasErrorText = lowerText.includes('xato') || lowerText.includes('error') || lowerText.includes('fail');

            if (!terminalText || (!hasErrorClass && !hasErrorText)) {
                return alert("Tahlil qilish uchun avval kodni yuborib, xato chiqaring.");
            }
            payload.error_message = terminalText;
        }
        
        this.submissionResult.className = 'terminal-output';
        this.submissionResult.innerHTML = `AI o'ylamoqda... <i class="fa-solid fa-spinner fa-spin"></i>`;
        
        try {
            const res = await api.askAI(type, payload);
            // Format markdown-like newlines
            let text = res.ai_response.replace(/\n/g, '<br>');
            this.submissionResult.innerHTML = `<strong style="color:var(--primary)"><i class="fa-solid fa-robot"></i> AI Javobi:</strong><br><br>${text}`;
        } catch(e) {
            this.submissionResult.className = 'terminal-output error';
            this.submissionResult.innerHTML = `<strong>AI Error:</strong><br>${e.message}`;
        }
    },

    async loadProgress() {
        this.progressTbody.innerHTML = '<tr><td colspan="4">Yuklanmoqda...</td></tr>';
        
        try {
            const progresses = await api.getProgress();
            this.progressTbody.innerHTML = '';
            
            if(progresses.length === 0) {
                this.progressTbody.innerHTML = '<tr><td colspan="4" style="text-align:center; color: var(--text-muted)">Hali vazifalar bajarilmagan. O\'rganishni boshlang!</td></tr>';
                return;
            }

            progresses.forEach(p => {
                const statusBadge = p.is_completed ? '<span class="badge success">Bajarildi</span>' : '<span class="badge pending">Tugallanmagan</span>';
                
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${p.task_detail?.title || `Topshiriq #${p.task}`}</strong></td>
                    <td>${statusBadge}</td>
                    <td><i class="fa-solid fa-star" style="color: #f59e0b; font-size: 0.8rem"></i> ${p.score}</td>
                    <td style="color:var(--text-muted); font-size:0.9rem;">${p.ai_feedback || "Fikr-mulohaza yo'q"}</td>
                `;
                this.progressTbody.appendChild(tr);
            });
            
        } catch(e) {
            if (e.message && e.message.includes('401')) return this.handleUnauth();
            this.progressTbody.innerHTML = `<tr><td colspan="4" class="error-msg">Progressni yuklashda xato yuz berdi.</td></tr>`;
        }
    }
};

/* ═══════════════════════════════════════════════════
   THEME PICKER — fon tanlash logikasi
   ═══════════════════════════════════════════════════ */
const themePicker = {
    init() {
        this.modal = document.getElementById('theme-modal');
        this.openBtn = document.getElementById('theme-picker-btn');
        this.closeBtn = document.getElementById('theme-modal-close');
        this.options = document.querySelectorAll('.theme-option');

        if (!this.modal || !this.openBtn) return;

        // Saqlangan temani yuklash
        const saved = localStorage.getItem('pylearn-theme') || 'default';
        this.applyTheme(saved);

        this.openBtn.addEventListener('click', () => this.open());
        this.closeBtn.addEventListener('click', () => this.close());
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.close();
        });

        this.options.forEach(opt => {
            opt.addEventListener('click', () => {
                const theme = opt.getAttribute('data-theme-value');
                this.applyTheme(theme);
                localStorage.setItem('pylearn-theme', theme);
            });
        });
    },

    open() {
        this.modal.classList.add('active');
    },

    close() {
        this.modal.classList.remove('active');
    },

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.options.forEach(opt => {
            opt.classList.toggle('active', opt.getAttribute('data-theme-value') === theme);
        });
    }
};

/* ═══════════════════════════════════════════════════
   SYNTAX HIGHLIGHTER — VS Code stilidagi kod bloklar
   ═══════════════════════════════════════════════════ */
const syntaxHighlighter = {
    KEYWORDS: [
        'False','None','True','and','as','assert','async','await',
        'break','class','continue','def','del','elif','else','except',
        'finally','for','from','global','if','import','in','is',
        'lambda','nonlocal','not','or','pass','raise','return',
        'try','while','with','yield'
    ],
    BUILTINS: [
        'print','len','range','int','str','float','list','dict','set',
        'tuple','type','input','open','sorted','enumerate','zip','map',
        'filter','abs','max','min','sum','round','isinstance','hasattr',
        'getattr','setattr','super','staticmethod','classmethod','property'
    ],

    highlight(container) {
        if (!container) return;
        const codeBlocks = container.querySelectorAll('pre code');
        codeBlocks.forEach(block => {
            const raw = block.textContent;
            block.innerHTML = this.highlightPython(raw);
        });
    },

    highlightPython(code) {
        const lines = code.split('\n');
        return lines.map((line, i) => {
            let html = this.escapeHtml(line);

            // Comments (# ...)
            html = html.replace(/(#.*)$/gm, '<span class="comment">$1</span>');

            // Strings — triple-quoted, double, single
            html = html.replace(/(&#039;&#039;&#039;[\s\S]*?&#039;&#039;&#039;|&quot;&quot;&quot;[\s\S]*?&quot;&quot;&quot;|&quot;[^&]*?&quot;|&#039;[^&]*?&#039;)/g, '<span class="string">$1</span>');
            // Simpler string matching for normal quotes
            html = html.replace(/("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g, (m) => {
                if (m.includes('class="')) return m; // already wrapped
                return `<span class="string">${m}</span>`;
            });

            // Numbers
            html = html.replace(/\b(\d+\.?\d*)\b/g, (m, p1, offset, str) => {
                // Skip if inside a span
                const before = str.substring(0, offset);
                if (before.includes('<span') && !before.includes('</span>')) return m;
                return `<span class="number">${p1}</span>`;
            });

            // Keywords
            this.KEYWORDS.forEach(kw => {
                const re = new RegExp(`\\b(${kw})\\b`, 'g');
                html = html.replace(re, (m, p1, offset, str) => {
                    const before = str.substring(0, offset);
                    if (before.includes('<span') && !before.includes('</span>')) return m;
                    return `<span class="keyword">${p1}</span>`;
                });
            });

            // Builtins
            this.BUILTINS.forEach(bi => {
                const re = new RegExp(`\\b(${bi})\\b(?=\\s*\\()`, 'g');
                html = html.replace(re, (m, p1, offset, str) => {
                    const before = str.substring(0, offset);
                    if (before.includes('<span') && !before.includes('</span>')) return m;
                    return `<span class="builtin">${p1}</span>`;
                });
            });

            // Function definitions: def xxx(
            html = html.replace(/\b(def)\b(\s+)(\w+)/g, (m, d, sp, fn, offset, str) => {
                const before = str.substring(0, offset);
                if (before.includes('<span') && !before.includes('</span>')) return m;
                return `<span class="keyword">${d}</span>${sp}<span class="func">${fn}</span>`;
            });

            // Class definitions: class xxx
            html = html.replace(/\b(class)\b(\s+)(\w+)/g, (m, c, sp, cn, offset, str) => {
                const before = str.substring(0, offset);
                if (before.includes('<span') && !before.includes('</span>')) return m;
                return `<span class="keyword">${c}</span>${sp}<span class="builtin">${cn}</span>`;
            });

            return html;
        }).join('\n');
    },

    escapeHtml(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }
};

window.onload = () => {
    app.init();
    themePicker.init();
};
