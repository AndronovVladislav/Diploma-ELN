import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { useCoreStore } from '@/stores/core';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard/Dashboard.vue')
                },
                {
                    path: '/experiment/laboratory/:id',
                    component: () => import('@/views/Editors/LabExperiment/LabExperiment.vue'),
                    props: true
                },
                {
                    path: '/experiment/computational/:id',
                    component: () => import('@/views/Editors/ComputationalExperiment.vue'),
                    props: true
                },
                {
                    path: '/ontology',
                    name: 'ontology',
                    component: () => import('@/views/OntologyDetails/OntologyList.vue')
                },
                {
                    path: '/ontology/details/om2',
                    name: 'OM2Details',
                    component: () => import('@/views/OntologyDetails/OM2Details.vue')
                },
                {
                    path: '/ontology/details/chebi',
                    name: 'ChEBIDetails',
                    component: () => import('@/views/OntologyDetails/ChEBIDetails.vue')
                },
                {
                    path: '/profile',
                    name: 'profile',
                    component: () => import('@/views/Profile.vue')
                },
                {
                    path: '/uikit/formlayout',
                    name: 'formlayout',
                    component: () => import('@/sakai/views/uikit/FormLayout.vue')
                },
                {
                    path: '/uikit/input',
                    name: 'input',
                    component: () => import('@/sakai/views/uikit/InputDoc.vue')
                },
                {
                    path: '/uikit/button',
                    name: 'button',
                    component: () => import('@/sakai/views/uikit/ButtonDoc.vue')
                },
                {
                    path: '/uikit/table',
                    name: 'table',
                    component: () => import('@/sakai/views/uikit/TableDoc.vue')
                },
                {
                    path: '/uikit/list',
                    name: 'list',
                    component: () => import('@/sakai/views/uikit/ListDoc.vue')
                },
                {
                    path: '/uikit/tree',
                    name: 'tree',
                    component: () => import('@/sakai/views/uikit/TreeDoc.vue')
                },
                {
                    path: '/uikit/panel',
                    name: 'panel',
                    component: () => import('@/sakai/views/uikit/PanelsDoc.vue')
                },
                {
                    path: '/uikit/overlay',
                    name: 'overlay',
                    component: () => import('@/sakai/views/uikit/OverlayDoc.vue')
                },
                {
                    path: '/uikit/media',
                    name: 'media',
                    component: () => import('@/sakai/views/uikit/MediaDoc.vue')
                },
                {
                    path: '/uikit/message',
                    name: 'message',
                    component: () => import('@/sakai/views/uikit/MessagesDoc.vue')
                },
                {
                    path: '/uikit/file',
                    name: 'file',
                    component: () => import('@/sakai/views/uikit/FileDoc.vue')
                },
                {
                    path: '/uikit/menu',
                    name: 'menu',
                    component: () => import('@/sakai/views/uikit/MenuDoc.vue')
                },
                {
                    path: '/uikit/charts',
                    name: 'charts',
                    component: () => import('@/sakai/views/uikit/ChartDoc.vue')
                },
                {
                    path: '/uikit/misc',
                    name: 'misc',
                    component: () => import('@/sakai/views/uikit/MiscDoc.vue')
                },
                {
                    path: '/uikit/timeline',
                    name: 'timeline',
                    component: () => import('@/sakai/views/uikit/TimelineDoc.vue')
                },
                {
                    path: '/pages/empty',
                    name: 'empty',
                    component: () => import('@/sakai/views/pages/Empty.vue')
                },
                {
                    path: '/pages/crud',
                    name: 'crud',
                    component: () => import('@/sakai/views/pages/Crud.vue')
                },
                {
                    path: '/documentation',
                    name: 'documentation',
                    component: () => import('@/sakai/views/pages/Documentation.vue')
                },
                {
                    path: '/support',
                    name: 'support',
                    component: () => import('@/views/pages/Support.vue')
                },
                {
                    path: '/explore',
                    name: 'explore',
                    component: () => import('@/views/Explore.vue')
                }
            ]
        },
        {
            path: '/notfound',
            name: 'notfound',
            component: () => import('@/views/pages/NotFound.vue')
        },
        {
            path: '/auth/signin',
            name: 'signin',
            component: () => import('@/views/Auth/SignIn.vue'),
            meta: { public: true }
        },
        {
            path: '/auth/signup',
            name: 'signup',
            component: () => import('@/views/Auth/SignUp.vue'),
            meta: { public: true }
        },
        {
            path: '/auth/accessdenied',
            name: 'accessDenied',
            component: () => import('@/views/Utils/AccessDenied.vue'),
            meta: { public: true }
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/Utils/Error.vue')
        },
        {
            path: '/:pathMatch(.*)*',
            redirect: '/notfound'
        }
    ]
});

router.beforeEach((to) => {
    const coreStore = useCoreStore();

    if (!(isPublic(to) || isAuthenticated(coreStore))) {
        return { name: 'accessDenied' };
    }

    return true;
});

function isAuthenticated(coreStore) {
    return !!coreStore.access_token;
}

function isPublic(to) {
    return 'meta' in to && 'public' in to.meta && to.meta.public;
}

export default router;
