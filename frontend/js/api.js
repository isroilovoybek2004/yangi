const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000/api' 
    : '/api';

const api = {
    // Request Wrapper (No longer requires token for Demo)
    async fetchProtected(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        let res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
        
        if (res.status === 401) {
            throw new Error('401: Backend himoyani qabul qilmadi.');
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
