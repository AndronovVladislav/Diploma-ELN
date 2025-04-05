<template>
    <div class="card w-full">
        <h1 class="text-3xl font-bold mb-4 flex items-center">
            <i class="pi pi-chart-line mr-3 text-blue-500"></i>
            Панель управления
        </h1>

        <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold">Ваши эксперименты</h2>
            <div class="relative">
                <Button
                    aria-controls="createMenu"
                    aria-haspopup="true"
                    class="p-button-primary"
                    icon="pi pi-plus"
                    label="Создать"
                    @click="toggleCreateMenu"
                />
                <Menu id="createMenu" ref="createMenu" :model="createOptions" popup />
            </div>
        </div>

        <ExperimentTable />

        <CreateExperimentDialog />
        <CreateFolderDialog />
        <MoveExperimentDialog />
    </div>
</template>

<script lang="ts" setup>
import { onBeforeMount, ref } from 'vue';
import { Button, Menu } from 'primevue';

import ExperimentTable from '@/views/Dashboard/ExperimentTable.vue';
import MoveExperimentDialog from '@/views/Dashboard/MoveExperimentDialog.vue';
import { useDashboardStore } from '@/stores/dashboard';
import CreateFolderDialog from '@/views/Dashboard/CreateFolderDialog.vue';
import CreateExperimentDialog from '@/views/Dashboard/CreateExperimentDialog.vue';

const dashboardStore = useDashboardStore();

const createMenu = ref<InstanceType<typeof Menu> | null>(null);

const createOptions = ref([
    {
        label: 'Эксперимент',
        icon: 'pi pi-book',
        command: () => {
            dashboardStore.createExperimentDialog.visible = true;
        }
    },
    {
        label: 'Папка',
        icon: 'pi pi-folder',
        command: () => {
            dashboardStore.createFolderDialog.visible = true;
        }
    }
]);

const toggleCreateMenu = (event: Event) => {
    createMenu.value?.toggle(event);
};

onBeforeMount(async () => {
    await dashboardStore.fetchExperimentFS();
});
</script>
