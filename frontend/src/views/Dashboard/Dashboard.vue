<template>
    <div class="card w-full">
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-xl font-semibold">Ваши эксперименты</h1>
            <div class="relative">
                <Button
                    aria-controls="menuExperimentsRef"
                    aria-haspopup="true"
                    class="p-button-primary"
                    icon="pi pi-plus"
                    label="Создать"
                    @click="(e) => menuExperimentsRef?.toggle(e)"
                />
                <Menu id="menuExperimentsRef" ref="menuExperimentsRef" :model="createOptionsExperiments" popup />
            </div>
        </div>

        <ExperimentTable />
    </div>

    <div class="card w-full">
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-xl font-semibold">Ваши шаблоны</h1>
            <div class="relative">
                <Button
                    aria-controls="menuTemplatesRef"
                    aria-haspopup="true"
                    class="p-button-primary"
                    icon="pi pi-plus"
                    label="Создать"
                    @click="(e) => menuTemplatesRef?.toggle(e)"
                />
                <Menu id="menuTemplatesRef" ref="menuTemplatesRef" :model="createOptionsTemplates" popup />
            </div>
        </div>

        <TemplateTable />
    </div>
</template>

<script lang="ts" setup>
import { onBeforeMount, ref } from 'vue';
import { Button, Menu } from 'primevue';

import ExperimentTable from '@/views/Dashboard/ExperimentTable.vue';
import { useDashboard } from '@/composables/useDashboard';
import TemplateTable from '@/views/Dashboard/TemplateTable.vue';

const {
    createExperimentDialog,
    createExperimentsFolderDialog,
    createTemplatesFolderDialog,
    createTemplateDialog,
    fetchExperimentFS,
    fetchTemplateFS
} = useDashboard();

const menuExperimentsRef = ref<InstanceType<typeof Menu> | null>(null);
const menuTemplatesRef = ref<InstanceType<typeof Menu> | null>(null);

const createOptionsExperiments = ref([
    {
        label: 'Эксперимент',
        icon: 'pi pi-book',
        command: () => {
            createExperimentDialog.value.visible = true;
        }
    },
    {
        label: 'Папка',
        icon: 'pi pi-folder',
        command: () => {
            createExperimentsFolderDialog.value.visible = true;
        }
    }
]);

const createOptionsTemplates = ref([
    {
        label: 'Шаблон',
        icon: 'pi pi-objects-column',
        command: () => {
            createTemplateDialog.value.visible = true;
        }
    },
    {
        label: 'Папка',
        icon: 'pi pi-folder',
        command: () => {
            createTemplatesFolderDialog.value.visible = true;
        }
    }
]);

onBeforeMount(async () => {
    await fetchExperimentFS();
    await fetchTemplateFS();
});
</script>
