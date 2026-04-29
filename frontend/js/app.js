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
        this.dashBadges = document.getElementById('dash-badges'); // Endi ishlatilmaydi, lekin saqlab turamiz xato bermasligi uchun
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
        const token = localStorage.getItem('access_token');
        if (!token) {
            this.switchView('auth');
        } else {
            this.switchView('dashboard');
        }
    },

    // 401 bo'lganda
    handleUnauth() {
        this.switchView('auth');
    },

    toggleAuthMode() {
        this.isLoginMode = !this.isLoginMode;
        document.getElementById('auth-title').innerText = this.isLoginMode ? 'Tizimga kirish' : "Ro'yxatdan o'tish";
        document.getElementById('auth-subtitle').innerText = this.isLoginMode ? "Darslarni davom ettirish uchun akkauntingizga kiring" : "Yangi platformaga xush kelibsiz";
        document.getElementById('auth-submit-btn').innerText = this.isLoginMode ? 'Kirish' : "Ro'yxatdan o'tish";
        document.getElementById('auth-toggle-text').innerText = this.isLoginMode ? "Akkauntingiz yo'qmi?" : "Akkauntingiz bormi?";
        document.getElementById('auth-toggle-link').innerText = this.isLoginMode ? "Ro'yxatdan o'tish" : 'Kirish';
        document.getElementById('group-email').style.display = this.isLoginMode ? 'none' : 'block';
        document.getElementById('auth-error').style.display = 'none';
    },

    async handleAuthSubmit() {
        const username = document.getElementById('auth-username').value.trim();
        const password = document.getElementById('auth-password').value.trim();
        const email = document.getElementById('auth-email').value.trim();
        const errorDiv = document.getElementById('auth-error');
        const btn = document.getElementById('auth-submit-btn');

        if (!username || !password) {
            errorDiv.innerText = "Maydonlarni to'ldiring";
            errorDiv.style.display = 'block';
            return;
        }

        try {
            btn.disabled = true;
            btn.innerText = "Kutib turing...";
            if (this.isLoginMode) {
                await api.login(username, password);
            } else {
                if (!email) throw new Error("Email manzilni kiriting");
                await api.register({ username, password, email });
                await api.login(username, password); // Auto login
            }
            
            // Success
            errorDiv.style.display = 'none';
            document.getElementById('auth-username').value = '';
            document.getElementById('auth-password').value = '';
            document.getElementById('auth-email').value = '';
            
            this.showApp();
        } catch (err) {
            errorDiv.innerText = err.message;
            errorDiv.style.display = 'block';
        } finally {
            btn.disabled = false;
            btn.innerText = this.isLoginMode ? "Kirish" : "Ro'yxatdan o'tish";
        }
    },

    handleLogout() {
        api.logout();
        this.showApp();
    },

    switchView(viewName) {
        // Navbarni berkitish yoki ko'rsatish
        const navLinksElem = document.querySelector('.nav-links');
        const userProfile = document.querySelector('.user-profile');
        if (viewName === 'auth') {
            if (navLinksElem) navLinksElem.style.display = 'none';
            if (userProfile) userProfile.style.display = 'none';
        } else {
            if (navLinksElem) navLinksElem.style.display = 'flex';
            if (userProfile) userProfile.style.display = 'flex';
            
            // Username yangilash
            const savedUser = localStorage.getItem('username');
            if (savedUser && this.navUsername) {
                this.navUsername.innerText = savedUser;
            }
        }

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
                'courses': 'Mavjud mavzular',
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
            const [profile, stats] = await Promise.all([
                api.getGamificationProfile(),
                api.getStats()
            ]);
            
            this.dashPoints.innerText = `${profile.xp} XP`;
            this.dashLevel.innerText = `${profile.level}-daraja`;
            this.dashLevelName.innerText = profile.level_name;
            this.dashStreak.innerText = `${profile.streak_days} kun`;

            // Sidebar username
            const savedUser = localStorage.getItem('username');
            if (savedUser) this.navUsername.innerText = savedUser;

            // Render Charts
            this.renderActivityHeatmap(stats.activity_data);
            this.renderCourseMasteryChart(stats.courses_progress);
        } catch (e) {
            if (e.message && e.message.includes('401')) return this.handleUnauth();
            console.error("Dashboard ma'lumotlarini yuklashda xato:", e);
        }
    },

    _heatmapAllData: null,
    _heatmapYear: null,

    renderActivityHeatmap(activityData) {
        // Store full data for year switching
        if (activityData !== undefined) {
            this._heatmapAllData = activityData;
        }
        const allData = this._heatmapAllData || [];

        // --- Year selector ---
        const yearSelector = document.getElementById('heatmap-year-selector');
        const currentYear = new Date().getFullYear();
        // Find which years have data
        const yearsWithData = [...new Set(allData.map(d => parseInt(d.date.substring(0, 4))))];
        // Always show at least current and previous year
        const allYears = [...new Set([currentYear - 1, currentYear, ...yearsWithData])].sort();
        
        if (!this._heatmapYear) this._heatmapYear = currentYear;

        if (yearSelector && yearSelector.childElementCount !== allYears.length) {
            yearSelector.innerHTML = '';
            allYears.forEach(y => {
                const btn = document.createElement('button');
                btn.className = `year-btn${y === this._heatmapYear ? ' active' : ''}`;
                btn.textContent = y;
                btn.onclick = () => {
                    this._heatmapYear = y;
                    this.renderActivityHeatmap(undefined);
                };
                yearSelector.appendChild(btn);
            });
        } else if (yearSelector) {
            yearSelector.querySelectorAll('.year-btn').forEach(btn => {
                btn.classList.toggle('active', parseInt(btn.textContent) === this._heatmapYear);
            });
        }

        const selectedYear = this._heatmapYear;

        const container = document.getElementById('activity-heatmap');
        const monthsContainer = document.getElementById('activity-months');
        if (!container) return;

        const CELL = 11;
        const GAP  = 3;
        const STEP = CELL + GAP; // 14px per column

        // Build activity map for selected year
        const activityMap = {};
        allData.forEach(item => {
            if (item.date.startsWith(String(selectedYear))) {
                activityMap[item.date] = item.count;
            }
        });

        // Build 52 weeks for the selected year
        const startDate = new Date(selectedYear, 0, 1); // Jan 1
        const endDate   = selectedYear === currentYear
            ? new Date() // today
            : new Date(selectedYear, 11, 31); // Dec 31

        // Roll back to Monday of the week containing Jan 1
        const startDow = startDate.getDay(); // 0=Sun
        const adjustedStart = new Date(startDate);
        adjustedStart.setDate(startDate.getDate() - (startDow === 0 ? 6 : startDow - 1));

        // Build weeks
        const weeks = [];
        let week = [];
        const cursor = new Date(adjustedStart);
        while (cursor <= endDate || week.length > 0) {
            const dateStr = cursor.toISOString().split('T')[0];
            const inYear  = cursor.getFullYear() === selectedYear;
            const count   = inYear ? (activityMap[dateStr] || 0) : -1; // -1 = outside year
            week.push({ date: dateStr, count, month: cursor.getMonth(), year: cursor.getFullYear(), inYear });
            cursor.setDate(cursor.getDate() + 1);
            if (week.length === 7) { weeks.push(week); week = []; }
            if (cursor > endDate && week.length === 0) break;
        }
        if (week.length > 0) {
            while (week.length < 7) {
                week.push({ date: '', count: -1, month: -1, year: -1, inYear: false });
            }
            weeks.push(week);
        }

        // Render month labels
        if (monthsContainer) {
            monthsContainer.innerHTML = '';
            monthsContainer.style.cssText = 'position:relative; height:18px; font-size:0.7rem; color:var(--text-muted); margin-bottom:3px;';
            const monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
            let lastLabel = -1;
            let lastLabelWeek = -5;
            weeks.forEach((w, wi) => {
                const firstInYear = w.find(d => d.inYear);
                if (!firstInYear) return;
                if (firstInYear.month !== lastLabel && (wi - lastLabelWeek) >= 3) {
                    const label = document.createElement('span');
                    label.style.cssText = `position:absolute; left:${wi * STEP}px; white-space:nowrap;`;
                    label.textContent = monthNames[firstInYear.month];
                    monthsContainer.appendChild(label);
                    lastLabel = firstInYear.month;
                    lastLabelWeek = wi;
                }
            });
        }

        // Render heatmap grid
        container.innerHTML = '';
        container.style.cssText = `display:grid; grid-template-rows:repeat(7,${CELL}px); grid-auto-columns:${CELL}px; grid-auto-flow:column; gap:${GAP}px; justify-content:start;`;

        // Detect light theme for correct gray/yellow colors
        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        const COLORS = {
            0: isLight ? '#ebedf0' : '#21262d',         // GRAY — no activity
            1: isLight ? '#fffacd' : 'rgba(255,212,59,0.25)', // very light yellow
            2: isLight ? '#fde272' : 'rgba(255,212,59,0.5)',
            3: isLight ? '#fcc419' : 'rgba(255,212,59,0.78)',
            4: isLight ? '#c9a900' : '#FFD43B',          // full yellow
        };

        weeks.forEach(w => {
            w.forEach(day => {
                const box = document.createElement('div');
                box.style.cssText = `width:${CELL}px; height:${CELL}px; border-radius:2px; cursor:pointer; transition:transform 0.15s;`;
                if (!day.inYear || day.count < 0) {
                    box.style.visibility = 'hidden';
                } else {
                    let level = 0;
                    if (day.count >= 1) level = 1;
                    if (day.count >= 3) level = 2;
                    if (day.count >= 5) level = 3;
                    if (day.count >= 7) level = 4;
                    box.style.backgroundColor = COLORS[level];
                    box.title = `${day.date}: ${day.count} ta kirish`;
                    box.onmouseenter = () => box.style.transform = 'scale(1.3)';
                    box.onmouseleave = () => box.style.transform = 'scale(1)';
                }
                container.appendChild(box);

            });
        });
    },

    renderCourseMasteryChart(coursesProgress) {
        const ctx = document.getElementById('mastery-chart');
        if (!ctx) return;
        
        if (this.masteryChart) {
            this.masteryChart.destroy();
        }

        if (!coursesProgress || coursesProgress.length === 0) {
            const container = ctx.parentNode;
            container.innerHTML = '<p class="empty-msg" style="text-align:center; padding-top:100px; color:var(--text-muted);">Hozircha tizimga mavzular kiritilmagan.</p>';
            return;
        }

        const labels = coursesProgress.map(c => c.course_name);
        const data = coursesProgress.map(c => c.percentage);
        
        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        const textColor = isLight ? '#1a1a2e' : '#f8fafc';
        const gridColor = isLight ? 'rgba(0,0,0,0.05)' : 'rgba(255,255,255,0.05)';

        this.masteryChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: "O'zlashtirish foizi (%)",
                    data: data,
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderColor: '#3b82f6',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y', // horizontal bar chart
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: isLight ? 'rgba(255,255,255,0.95)' : 'rgba(15,23,42,0.95)',
                        titleColor: isLight ? '#1a1a2e' : '#f8fafc',
                        bodyColor: isLight ? '#1a1a2e' : '#f8fafc',
                        borderColor: gridColor,
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: gridColor },
                        ticks: { color: textColor, font: { family: 'Inter', size: 11 } }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: textColor, font: { family: 'Inter', size: 12 } }
                    }
                }
            }
        });
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
        this.coursesList.innerHTML = '<p>Yuklanmoqda...</p>';
        try {
            const [courses, lessons, progress] = await Promise.all([
                api.getCourses(),
                api.getLessons(),
                api.getProgress()
            ]);

            this.coursesList.innerHTML = '';

            if (!courses || courses.length === 0) {
                this.coursesList.innerHTML = '<p class="empty-msg">Hozircha mavzular mavjud emas.</p>';
                return;
            }

            // Build completed task set from progress
            const completedTaskIds = new Set(
                (progress || []).filter(p => p.is_completed).map(p => p.task)
            );

            courses.forEach(c => {
                const cLessons = lessons.filter(l => l.course === c.id);

                const card = document.createElement('div');
                card.className = 'course-card glass-panel';
                card.style.cssText = 'margin-bottom: 24px;';

                // Header
                card.innerHTML = `
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                        <div class="course-icon">
                            <img src="img/python-logo.svg" alt="Python" style="width:26px; height:26px; object-fit:contain;">
                        </div>
                        <div>
                            <h3 style="margin:0; font-size:1.1rem;">${c.title}</h3>
                            <p style="margin:2px 0 0; font-size:0.82rem; color:var(--text-muted);">${c.description || ''}</p>
                        </div>
                    </div>
                    <div class="lesson-table-wrapper">
                        <table class="lesson-table">
                            <thead>
                                <tr>
                                    <th style="text-align:left;">Mavzu nomi</th>
                                    <th style="text-align:center; width:130px;">Topshiriq</th>
                                    <th style="text-align:center; width:100px;">Test</th>
                                </tr>
                            </thead>
                            <tbody id="lessons-body-${c.id}"></tbody>
                        </table>
                    </div>
                `;

                this.coursesList.appendChild(card);
                const tbody = document.getElementById(`lessons-body-${c.id}`);

                if (cLessons.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="3" style="text-align:center; color:var(--text-muted); padding:16px;">Hozircha darslar yo'q</td></tr>`;
                    return;
                }

                cLessons.forEach(l => {
                    // tasks = kod topshiriqlari, quizzes = test savollari (alohida model)
                    const tasks   = l.tasks   || [];
                    const quizzes = l.quizzes || [];

                    const taskTotal = tasks.length;
                    const taskComp  = tasks.filter(t => completedTaskIds.has(t.id)).length;
                    const taskDone  = taskTotal > 0 && taskComp === taskTotal;

                    // Quiz uchun completion tracking: quiz.questions orqali
                    // Hozircha quizTotal — quiz bloklar soni (har quiz = 1 test bloki)
                    const quizTotal = quizzes.length;
                    // Quiz savollarini progress bilan tekshirish (QuizQuestion idlari)
                    const quizQIds  = quizzes.flatMap(q => (q.questions || []).map(qq => qq.id));
                    const quizComp  = quizQIds.filter(id => completedTaskIds.has(id)).length;
                    const quizDone  = quizTotal > 0 && quizQIds.length > 0 && quizComp === quizQIds.length;

                    const taskBadge = taskTotal === 0
                        ? `<span class="status-badge status-empty">Mavjud emas</span>`
                        : taskDone
                            ? `<span class="status-badge status-done"><i class="fa-solid fa-check"></i> Bajarildi</span>`
                            : taskComp > 0
                                ? `<span class="status-badge status-partial">${taskComp}/${taskTotal} bajarildi</span>`
                                : `<span class="status-badge status-pending">Bajarilmagan</span>`;

                    const quizBadge = quizTotal === 0
                        ? `<span class="status-badge status-empty">Mavjud emas</span>`
                        : quizDone
                            ? `<span class="status-badge status-done"><i class="fa-solid fa-check"></i> Bajarildi</span>`
                            : quizComp > 0
                                ? `<span class="status-badge status-partial">${quizComp}/${quizQIds.length} bajarildi</span>`
                                : `<span class="status-badge status-pending">Bajarilmagan</span>`;

                    const tr = document.createElement('tr');
                    tr.className = 'lesson-row';
                    tr.innerHTML = `
                        <td class="lesson-name-cell">
                            <i class="fa-solid fa-circle-play" style="color:var(--accent); margin-right:8px; font-size:0.85rem;"></i>
                            ${l.title}
                        </td>
                        <td style="text-align:center;">${taskBadge}</td>
                        <td style="text-align:center;">${quizBadge}</td>
                    `;
                    tr.onclick = () => this.openLesson(l);
                    tbody.appendChild(tr);
                });
            });
        } catch (e) {
            if (e.message && e.message.includes('401')) return this.handleUnauth();
            this.coursesList.innerHTML = '<p class="error-msg">Kurslarni yuklab bo\'lmadi. Backend ishlayaptimi?</p>';
        }
    },

    async openLesson(lesson) {
        this.switchView('editor');
        this.lessonTitle.innerText = lesson.title;

        // --- YouTube video ---
        let contentHtml = lesson.content || "Mavzu bo'yicha ma'lumot yuklanmoqda...";
        let videoHtml = '';
        if (lesson.video_url) {
            // video_url ni embed URL ga aylantirish (watch?v= -> embed/)
            let embedUrl = lesson.video_url;
            const ytMatch = lesson.video_url.match(
                /(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([A-Za-z0-9_\-]{11})/
            );
            if (ytMatch) {
                embedUrl = `https://www.youtube.com/embed/${ytMatch[1]}`;
            }

            // Eski dars matnidagi YouTube iframe'larni va ularning bo'sh qolgan wrapperlarini o'chirib tashlaymiz
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = contentHtml;
            const iframes = tempDiv.querySelectorAll('iframe[src*="youtube"], iframe[src*="youtu.be"]');
            iframes.forEach(iframe => {
                let parent = iframe.parentElement;
                iframe.remove();
                while (parent && parent !== tempDiv) {
                    if (parent.innerHTML.trim() === '' || parent.innerHTML.trim() === '<br>') {
                        let nextParent = parent.parentElement;
                        parent.remove();
                        parent = nextParent;
                    } else {
                        break;
                    }
                }
            });

            // Shuningdek, bazada qolib ketgan bo'sh video wrapperlarni ham tozalaymiz
            const emptyWrappers = tempDiv.querySelectorAll('.video-wrapper, .lesson-video-wrapper');
            emptyWrappers.forEach(wrapper => {
                const textContent = wrapper.innerHTML.replace(/&nbsp;/g, '').trim();
                if (textContent === '' || textContent === '<br>' || textContent === '<p></p>' || textContent === '<p><br></p>') {
                    wrapper.remove();
                }
            });

            contentHtml = tempDiv.innerHTML;

            videoHtml = `
                <div class="lesson-video-wrapper" style="
                    position:relative; padding-bottom:56.25%; height:0; overflow:hidden;
                    border-radius:12px; margin-bottom:20px; 
                    background: rgba(255, 255, 255, 0.05);
                    backdrop-filter: blur(16px);
                    -webkit-backdrop-filter: blur(16px);
                    border: 1px solid var(--border-glass);
                    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                ">
                    <iframe
                        src="${embedUrl}"
                        title="Dars videosi"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                        allowfullscreen
                        style="position:absolute; top:0; left:0; width:100%; height:100%; border-radius:10px;"
                    ></iframe>
                </div>`;
        }
        this.lessonContent.innerHTML = videoHtml + contentHtml;
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
            // Task seksiyasiga scroll
            setTimeout(() => {
                const taskSection = document.querySelector('.task-section');
                if (taskSection) {
                    taskSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 300);
        } else {
            this.taskTitle.innerText = "Vazifalar yo'q";
            this.taskQuestion.innerText = "Ushbu dars uchun hozircha vazifalar mavjud emas.";
            this.currentTask = null;
            hintsBox.classList.add('hidden');
        }

        const quizSection = document.getElementById('quiz-section');
        const quizContainer = document.getElementById('quiz-container');
        if (lesson.quizzes && lesson.quizzes.length > 0) {
            if (quizSection) quizSection.style.display = 'block';
            this.renderQuizzes(lesson.quizzes, quizContainer);
        } else {
            if (quizSection) quizSection.style.display = 'none';
        }
    },

    renderQuizzes(quizzes, container) {
        if (!container) return;
        container.innerHTML = '';
        
        quizzes.forEach((quiz, qzIdx) => {
            const quizDiv = document.createElement('div');
            quizDiv.className = 'quiz-block';
            quizDiv.innerHTML = `<h4 style="color:var(--primary); margin-bottom: 10px;">${quiz.title}</h4>`;
            
            if (quiz.questions && quiz.questions.length > 0) {
                quiz.questions.forEach((q, i) => {
                    const qDiv = document.createElement('div');
                    qDiv.className = 'quiz-question';
                    qDiv.style.marginBottom = '15px';
                    
                    let html = `<p><strong>${i+1}.</strong> ${q.question_text}</p>`;
                    html += `<div class="quiz-choices" style="display: flex; flex-direction: column; gap: 8px; margin-top: 10px;">`;
                    
                    q.choices.forEach(c => {
                        html += `
                            <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 5px; border: 1px solid var(--border-glass);">
                                <input type="radio" name="question_${q.id}" value="${c.is_correct}">
                                <span>${c.choice_text}</span>
                            </label>
                        `;
                    });
                    
                    html += `</div>`;
                    html += `<p class="quiz-feedback hidden" id="feedback_${q.id}" style="margin-top: 8px; font-size: 0.85rem; padding: 8px; border-radius: 5px;"></p>`;
                    
                    qDiv.innerHTML = html;
                    quizDiv.appendChild(qDiv);
                });
                
                const btn = document.createElement('button');
                btn.className = 'btn-primary btn-sm';
                btn.style.marginTop = '15px';
                btn.innerHTML = '<i class="fa-solid fa-check"></i> Javoblarni tekshirish';
                btn.onclick = async () => {
                    let score = 0;
                    quiz.questions.forEach(q => {
                        const selected = quizDiv.querySelector(`input[name="question_${q.id}"]:checked`);
                        const feedbackEl = quizDiv.querySelector(`#feedback_${q.id}`);
                        feedbackEl.classList.remove('hidden');
                        
                        if (!selected) {
                            feedbackEl.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i> Javob belgilanmadi.`;
                            feedbackEl.style.background = 'rgba(255,165,0,0.1)';
                            feedbackEl.style.color = 'orange';
                        } else if (selected.value === 'true') {
                            score++;
                            feedbackEl.innerHTML = `<i class="fa-solid fa-circle-check"></i> To'g'ri! ${q.explanation ? '<br><small>'+q.explanation+'</small>' : ''}`;
                            feedbackEl.style.background = 'rgba(74,222,128,0.1)';
                            feedbackEl.style.color = '#4ade80';
                        } else {
                            feedbackEl.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> Noto'g'ri. ${q.explanation ? '<br><small>'+q.explanation+'</small>' : ''}`;
                            feedbackEl.style.background = 'rgba(248,113,113,0.1)';
                            feedbackEl.style.color = '#f87171';
                        }
                    });
                    
                    if (score === quiz.questions.length && score > 0) {
                        // XP berish API ga so'rov
                        try {
                            const xpRes = await api.quizXP();
                            let msg = `🎉 Tabriklaymiz! Barcha ${score} ta savolga to'g'ri javob berdingiz!\n+${xpRes.xp_earned || 5} XP qo'shildi!`;
                            if (xpRes.new_badges && xpRes.new_badges.length > 0) {
                                msg += `\n🏅 Yangi yutuq: ${xpRes.new_badges.join(', ')}`;
                            }
                            alert(msg);
                            this.loadDashboard();
                        } catch(e) {
                            alert(`Tabriklaymiz! Barcha ${score} ta savolga to'g'ri javob berdingiz!`);
                        }
                        // Tugmani o'chirish (qayta bosmasligi uchun)
                        btn.disabled = true;
                        btn.innerHTML = '<i class="fa-solid fa-check-double"></i> Yakunlandi';
                    } else {
                        alert(`Natija: ${quiz.questions.length} tadan ${score} tasi to'g'ri. Qayta urinib ko'ring!`);
                    }
                };
                quizDiv.appendChild(btn);
            } else {
                quizDiv.innerHTML += '<p style="font-size:0.8rem; color:var(--text-muted)">Savollar tizimga kiritilmagan.</p>';
            }
            
            container.appendChild(quizDiv);
            if (qzIdx < quizzes.length - 1) {
                container.appendChild(document.createElement('hr'));
            }
        });
    },

    renderTask(task) {
        this.currentTask = task;
        const hintsBox = document.getElementById('ai-hints');
        const hintsToggle = document.getElementById('btn-toggle-hints');
        this.taskTitle.innerText = task.title;
        this.taskQuestion.innerText = task.question;
        // Boshlang'ich kodni editorga yuklash
        const starterCode = task.starter_code || '';
        this.cmEditor.setValue(starterCode);
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
        // CodeMirror ni to'g'ri o'lchamda ko'rsatish uchun refresh
        setTimeout(() => this.cmEditor.refresh(), 50);
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
                const feedbackHtml = (res.ai_feedback || '').replace(/\n/g, '<br>');
                this.submissionResult.innerHTML = `<span style="color:#4ade80"><i class="fa-solid fa-circle-check"></i> Muvaffaqiyatli! Kod to'g'ri ishladi.</span><br><span style="color:var(--primary)">+${res.xp_earned} XP to'plandi</span>${badgeMsg}<br><br><strong>Natija:</strong><br><code style="font-family:monospace;white-space:pre-wrap">${feedbackHtml}</code>`;
                // Dashboard ni yangilash
                this.loadDashboard();
            } else {
                this.submissionResult.className = 'terminal-output error';
                const errHtml = (res.ai_feedback || 'Sintaktik xato.').replace(/\n/g, '<br>');
                this.submissionResult.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> Xato.<br><br>${errHtml}`;
            }
        } catch(e) {
            this.submissionResult.className = 'terminal-output error';
            this.submissionResult.innerHTML = 'Backend bilan bog\'lanishda xato yuz berdi.';
        }
    },

    async askAI(type) {
        if (!this.currentTask) return alert("Avval masalani tanlang.");
        const code = this.cmEditor.getValue();

        if (type === 'explain') {
            if (!code.trim()) return alert("Tushuntirish uchun kod yozing.");
        }

        let payload = { code: code, task_question: this.currentTask.question };

        if (type === 'analyze') {
            const terminalText = this.submissionResult.innerText.trim();
            // Terminal bo'sh yoki faqat "Kutilmoqda" matni bo'lsa bloklash
            const isIdle = !terminalText || terminalText === 'Kutilmoqda...' || terminalText === 'Natijani kutilmoqda...';
            if (isIdle) {
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
    
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            alert("Siz hozir ochiq demo rejimidasiz. Tizim avtomatik ravishda mehmon akkauntiga ulangan, shuning uchun profildan chiqish hozircha o'chirib qo'yilgan.");
        });
    }
};
