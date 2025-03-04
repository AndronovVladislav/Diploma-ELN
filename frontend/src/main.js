import {createApp} from 'vue';
import Aura from '@primevue/themes/aura';
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import {createPinia} from 'pinia';
import persist from 'pinia-plugin-persistedstate';

import '@/assets/styles.scss';
import App from '@/App.vue';
import router from '@/router';

const app = createApp(App);

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

const pinia = createPinia();
pinia.use(persist);
app.use(pinia);

app.mount('#app');
