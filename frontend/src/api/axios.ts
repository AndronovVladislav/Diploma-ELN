import axios from 'axios';
import { useCoreStore } from '@/stores/core';
import router from '@/router';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    timeout: 30000
});

const TOKEN_REFRESH_URL = '/auth/refresh';

api.interceptors.request.use(config => {
    const coreStore = useCoreStore();

    if (coreStore.access_token) {
        config.headers.Authorization = `Bearer ${coreStore.access_token}`;
    }

    return config;
}, error => {
    return Promise.reject(error);
});

api.interceptors.response.use(response => response, async error => {
        const originalRequest = error.config;
        const coreStore = useCoreStore();

        if (error.response?.status === 401) {
            if (!error.config.url.includes(TOKEN_REFRESH_URL)) {
                try {
                    const response = await api.post(TOKEN_REFRESH_URL, {
                        refresh_token: coreStore.refresh_token
                    });

                    coreStore.access_token = response.data.access_token;

                    originalRequest.headers['Authorization'] = `Bearer ${coreStore.access_token}`;

                    return api(originalRequest);
                } catch (refreshError) {
                    coreStore.access_token = null;
                    coreStore.refresh_token = null;
                    await router.push('/auth/login');
                }
            } else {
                coreStore.access_token = null;
                coreStore.refresh_token = null;
                await router.push('/auth/login');
            }
        }

        return Promise.reject(error);
    }
);


export default api;
