<template>
    <div class="card w-full">
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-xl font-semibold">
                Ваши эксперименты
            </h1>
            <div class="flex items-center gap-2">
                <FileUpload
                    auto
                    customUpload
                    mode="basic"
                    name="file"
                    accept="application/json"
                    chooseLabel="Импорт"
                    @select="onFileChange"
                />
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
import FileUpload from 'primevue/fileupload';

import ExperimentTable from '@/views/Dashboard/ExperimentTable.vue';
import { useDashboard } from '@/composables/useDashboard';
import TemplateTable from '@/views/Dashboard/TemplateTable.vue';
import api from '@/api/axios';
import { useNotifier } from '@/composables/useNotifier';

const {
    createExperimentDialog,
    createExperimentsFolderDialog,
    createTemplatesFolderDialog,
    createTemplateDialog,
    fetchExperimentFS,
    fetchTemplateFS
} = useDashboard();

const Notifier = useNotifier();

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

const onFileChange = async (event) => {
    const files = event.files;
    if (!files || files.length === 0) return;
    const file = files[0];
    let content: string;

    try {
        content = await file.text();
    } catch (err) {
        Notifier.error({ detail: 'Не удалось прочитать файл' });
        return;
    }

    let data: any;
    try {
        data = JSON.parse(content);
    } catch (err) {
        Notifier.error({ detail: 'Неверный формат JSON' });
        return;
    }

    const kind = 'measurements' in data ? 'laboratory' : 'computational';

    try {
        await api.post(`/experiment/import/${kind}`, data);
        Notifier.success({ detail: 'Импорт завершён' });
        await fetchExperimentFS();
    } catch (error) {
        console.error('Ошибка при импорте эксперимента:', error);
        Notifier.error({ detail: error instanceof Error ? error.message : 'Неизвестная ошибка' });
    }
};
</script>
