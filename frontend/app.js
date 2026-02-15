const { createApp } = Vue;
const API_URL = '/api';

const app = createApp({
    data() {
        return {
            factory: { total_production: 0, global_utilization: 0 },
            workers: [],
            isSimulating: false
        }
    },
    mounted() {
        this.fetchData();
        setInterval(this.fetchData, 2000);
    },
    methods: {
        async fetchData() {
            try {
                const [fRes, wRes] = await Promise.all([
                    fetch(`${API_URL}/metrics/factory`),
                    fetch(`${API_URL}/metrics/workers`)
                ]);
                this.factory = await fRes.json();
                this.workers = await wRes.json();
            } catch (e) { console.error(e); }
        },

        async simulateWork() {
            this.isSimulating = true;
            try {
                await fetch(`${API_URL}/ingest/simulate`, { method: 'POST' });

                await this.fetchData();
            } catch (e) {
                alert("Simulation failed!");
            }
            this.isSimulating = false;
        }
    }
}).mount('#app');

window.app = app;