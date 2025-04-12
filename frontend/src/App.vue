<template>
    <Toast />
    <router-view />
</template>

<script setup>
import { onBeforeMount } from 'vue';
import { useCoreStore } from '@/stores/core';
import { onPresetChange, primaryColors, surfaces, updateColors } from '@/layout/composables/themeManager';
import { useLayout } from '@/layout/composables/layout';

const coreStore = useCoreStore();
const { toggleDarkMode } = useLayout();

onBeforeMount(() => {
    const primaryColor = primaryColors.value.find((c) => c.name === coreStore.layoutConfig.primary);
    const surfaceColor = surfaces.value.find((c) => c.name === coreStore.layoutConfig.surface);

    updateColors('primary', primaryColor);
    updateColors('surface', surfaceColor);
    onPresetChange(coreStore.layoutConfig.preset);

    if (coreStore.layoutConfig.darkTheme) {
        coreStore.layoutConfig.darkTheme = !coreStore.layoutConfig.darkTheme;
        toggleDarkMode();
    }
});
</script>
