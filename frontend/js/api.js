const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000/api' 
    : '/api';

const api = {
    // Request Wrapper with JWT Token
    async fetchProtected(endpoint, options = {}) {
        const token = localStorage.getItem('access_token');
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        let res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
        
        if (res.status === 401) {
            // Optional: try refresh token here
            localStorage.removeItem('access_token');
            throw new Error('401');
        }
        return res;
    },

    // Authentication
    async login(username, password) {
        const res = await fetch(`${API_BASE}/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Login xatosi');
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        localStorage.setItem('username', username);
        return data;
    },

    async register(userData) {
        const res = await fetch(`${API_BASE}/users/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        const data = await res.json();
        if (!res.ok) {
            let errorMsg = 'Xatolik yuz berdi';
            if (data.username) errorMsg = data.username[0];
            else if (data.email) errorMsg = data.email[0];
            else if (typeof data === 'string') errorMsg = data;
            throw new Error(errorMsg);
        }
        return data;
    },

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
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
    },

    async quizXP() {
        const res = await this.fetchProtected('/progress/quiz-xp/', {
            method: 'POST',
            body: JSON.stringify({})
        });
        return await res.json();
    },

    async getBadges() {
        const res = await this.fetchProtected('/gamification/badges/');
        return await res.json();
    }
};
