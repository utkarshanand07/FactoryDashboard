const { createApp } = Vue;

// Relative URL automatically works for Docker & Render
const API_URL = '/api';

createApp({
    data() {
        return {
            factory: { total_production: 0, global_utilization: 0 },
            workers: [],
            error: null
        }
    },
    mounted() {
        this.fetchData();

        // Auto-refresh data every 2 seconds to see updates live!
        setInterval(this.fetchData, 2000);
    },
    methods: {
        async fetchData() {
            try {
                const [fRes, wRes] = await Promise.all([
                    fetch(`${API_URL}/metrics/factory`),
                    fetch(`${API_URL}/metrics/workers`)
                ]);

                if (!fRes.ok || !wRes.ok) throw new Error("API Error");

                this.factory = await fRes.json();
                this.workers = await wRes.json();
                this.error = null;
            } catch (e) {
                console.error("Connection Error:", e);
                this.error = "Backend unavailable. Retrying...";
            }
        }
    }
}).mount('#app');