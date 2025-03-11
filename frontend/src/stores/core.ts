import { defineStore } from 'pinia';

export const useCoreStore = defineStore('core',
    {
        state: () => ({
            access_token: null as (string | null),
            refresh_token: null as (string | null),
        }),
        getters: {},
        actions: {},
        persist: true
    }
);
