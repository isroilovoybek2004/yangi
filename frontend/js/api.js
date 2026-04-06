const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000/api' 
    : '/api';

const api = {
    getToken: () => localStorage.getItem('access_token'),
    setTokens: (access, refresh) => {
        localStorage.setItem('access_token', access);
        if (refresh) localStorage.setItem('refresh_token', refresh);
    },
    clearTokens: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    // Auth
    async login(username, password) {
        const res = await fetch(`${API_BASE}/token/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        if (!res.ok) throw new Error('Invalid credentials');
        const data = await res.json();
        this.setTokens(data.access, data.refresh);
        return data;
    },

    async register(username, email, password) {
        const res = await fetch(`${API_BASE}/users/register/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, email, password})
        });
        if (!res.ok) throw new Error('Registration failed');
        return await res.json();
    },

    // Protected Request Wrapper
    async fetchProtected(endpoint, options = {}) {
        let token = this.getToken();
        if (!token) throw new Error('401: Token yo\'q');

        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...options.headers
        };

        let res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
        
        if (res.status === 401) {
            this.clearTokens();
            throw new Error('401: Seans muddati tugadi. Iltimos, qaytadan kiring.');
        }
        return res;
    },

    // Resources Fetching
    async getCourses() {
        const res = await this.fetchProtected('/courses/');
        return await res.json();
    },

    async getLessons() {
        const res = await this.fetchProtected('/lessons/lessons/');
        return await res.json();
    },
    
    async getTasks() {
        const res = await this.fetchProtected('/lessons/tasks/');
        return await res.json();
    },

    async getProgress() {
        const res = await this.fetchProtected('/progress/');
        return await res.json();
    },

    async submitCode(taskId, code) {
        const payload = {
            task: taskId,
            submitted_answer: code
        };
        const res = await this.fetchProtected('/progress/submissions/', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        return await res.json();
    },

    async askAI(actionType, payload) {
        const res = await this.fetchProtected(`/progress/ai/${actionType}/`, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'AI Xatosi');
        return data;
    },

    // Gamification
    async getGamificationProfile() {
        const res = await this.fetchProtected('/gamification/profile/');
        return await res.json();
    },

    async getLeaderboard() {
        const res = await this.fetchProtected('/gamification/leaderboard/');
        return await res.json();
    },

    async getStats() {
        const res = await this.fetchProtected('/gamification/stats/');
        return await res.json();
    }
};
