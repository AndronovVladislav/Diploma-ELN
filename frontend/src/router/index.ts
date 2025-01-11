import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router';
// import DashboardView from '../views/DashboardView.vue';
// import ExperimentsView from '../views/ExperimentsView.vue';
// import TemplatesView from '../views/TemplatesView.vue';
// import SettingsView from '../views/SettingsView.vue';
import HomeView from '../views/Home.vue';

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Home',
        component: HomeView,
    },
    // {
    //   path: '/experiments',
    //   name: 'Experiments',
    //   component: ExperimentsView,
    // },
    // {
    //   path: '/templates',
    //   name: 'Templates',
    //   component: TemplatesView,
    // },
    // {
    //   path: '/settings',
    //   name: 'Settings',
    //   component: SettingsView,
    // },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;