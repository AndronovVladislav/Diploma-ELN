import axios from 'axios';
import { useCoreStore } from '@/stores/core';
import router from '@/router';

const api = axios.create({
    baseURL: '/',
    timeout: 5000
});

const TOKEN_REFRESH_URL = '/auth/refresh'

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

    if (error.response.status === 401 && !error.request.baseURL.includes(TOKEN_REFRESH_URL)) {

        try {
            const response = await api.post('/auth/refresh', {
                refresh_token: coreStore.refresh_token
            });

            coreStore.access_token = response.data.access_token;

            originalRequest.headers['Authorization'] = `Bearer ${coreStore.access_token}`;

            return api(originalRequest);
        } catch (refreshError) {
            coreStore.access_token = null;
            coreStore.refresh_token = null;
            router.push('/auth/login')
        }
    }

    return Promise.reject(error);
});


export default api;
