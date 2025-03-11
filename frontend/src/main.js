import { createApp } from 'vue';
import Aura from '@primevue/themes/aura';
import PrimeVue from 'primevue/config';
import { createPinia } from 'pinia';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import persist from 'pinia-plugin-persistedstate';

import '@/assets/styles.scss';
import App from '@/App.vue';
import router from '@/router';

const app = createApp(App);

const pinia = createPinia();
pinia.use(persist);

app.use(pinia);
app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.app-dark'
        }
    }
});
app.use(ToastService);
app.use(ConfirmationService);

app.mount('#app');
