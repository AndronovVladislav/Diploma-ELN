import { defineStore } from 'pinia';

interface LayoutConfig {
    preset: string,
    primary: string,
    surface: string | null,
    darkTheme: boolean,
    menuMode: string
}

interface LayoutState {
    staticMenuDesktopInactive: boolean,
    overlayMenuActive: boolean,
    profileSidebarVisible: boolean,
    configSidebarVisible: boolean,
    staticMenuMobileActive: boolean,
    menuHoverActive: boolean,
    activeMenuItem: string | null
}


export const useCoreStore = defineStore('core',
    {
        state: () => ({
            username: null as (string | null),
            access_token: null as (string | null),
            refresh_token: null as (string | null),
            layoutConfig: {
                preset: 'Aura',
                primary: 'emerald',
                surface: 'zinc',
                darkTheme: false,
                menuMode: 'static'
            } as LayoutConfig,
            layoutState: {
                staticMenuDesktopInactive: false,
                overlayMenuActive: false,
                profileSidebarVisible: false,
                configSidebarVisible: false,
                staticMenuMobileActive: false,
                menuHoverActive: false,
                activeMenuItem: null
            } as LayoutState
        }),
        getters: {},
        actions: {},
        persist: true
    }
);
