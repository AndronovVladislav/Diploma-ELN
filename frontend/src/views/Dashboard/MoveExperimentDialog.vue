<template>
    <Dialog v-model:visible="visibleModel" header="Перемещение эксперимента" modal>
        <p>Выберите новую папку для эксперимента "<strong>{{ dashboardStore.selectedExperiment.path }}</strong>":</p>

        <Select v-model="selectedFolder"
                :options="dashboardStore.formattedFolders(dashboardStore.selectedExperiment.kind).value"
                class="w-full mt-2"
                option-label="path"
                placeholder="Выберите папку"
        />

        <div class="flex justify-end mt-4 gap-2">
            <Button label="Отмена" severity="secondary" @click="visibleModel = false" />
            <Button :disabled="!selectedFolder" label="Переместить" severity="success" @click="confirmMove" />
        </div>
    </Dialog>
</template>

<script lang="ts" setup>
import { Button, Dialog, Select } from 'primevue';
import { ref, watch } from 'vue';

import { Folder, SimplifiedView } from '@/views/Dashboard/typing';
import { useDashboardStore } from '@/stores/dashboard';
import { findById, removeExperiment } from '@/utils/fileSystem';

const dashboardStore = useDashboardStore();
const visibleModel = dashboardStore.getVisibleModel(dashboardStore.moveExperimentDialog);
const selectedFolder = ref<SimplifiedView | null>(null);

watch(() => visibleModel, (newVal) => {
    if (!newVal.value) {
        selectedFolder.value = null;
    }
});

const confirmMove = () => {
    if (!dashboardStore.selectedExperiment || !selectedFolder.value) return;

    const targetFolder = findById(dashboardStore.experimentFS, selectedFolder.value.id) as Folder;
    if (dashboardStore.currentFolder.id === targetFolder.id) {
        return;
    }

    removeExperiment(dashboardStore.experimentFS, dashboardStore.selectedExperiment.id);
    if (targetFolder) {
        targetFolder.children.push(dashboardStore.selectedExperiment);
    }
    visibleModel.value = false;
};
</script>
