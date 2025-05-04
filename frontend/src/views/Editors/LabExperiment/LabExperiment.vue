<template>
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
        <ProgressSpinner />
    </div>

    <div v-else class="flex flex-col gap-4">
        <Button v-if="isChanged" label="Сохранить изменения" icon="pi pi-save" class="w-fit" @click="saveChanges" />
        <Panel toggleable>
            <template #header>
                <div>
                    <span class="text-xl font-bold">Description</span>
                </div>
            </template>
            <Editor v-model:description="description" />
        </Panel>
        <Panel toggleable>
            <template #header>
                <div>
                    <span class="text-xl font-bold">Measurements</span>
                </div>
            </template>
            <Table v-model:columns="columns" v-model:data="measurements" v-model:mainColumn="mainColumnName" />
        </Panel>
        <Panel toggleable collapsed>
            <template #header>
                <div>
                    <span class="text-xl font-bold">Charts</span>
                </div>
            </template>
            <Charts :mainColumn="mainColumnName" :data="measurements" />
        </Panel>
    </div>
</template>

<script lang="ts" setup>
import { computed, onBeforeMount, onBeforeUnmount, ref, watchEffect } from 'vue';
import Editor from '@/components/Editor.vue';
import api from '@/api/axios';
import Table from '@/views/Editors/LabExperiment/Table.vue';
import ProgressSpinner from 'primevue/progressspinner';
import { Button } from 'primevue';
import { useNotifier } from '@/composables/useNotifier';
import Charts from '@/views/Editors/LabExperiment/Charts.vue';
import { Column } from '@/views/Editors/LabExperiment/typing';
import { AxiosError } from 'axios';

interface Props {
    id: string;
}

const props = defineProps<Props>();
const Notifier = useNotifier();

const description = ref('');
const columns = ref<Column[]>([]);
const measurements = ref([]);

const originalDescription = ref('');
const originalColumns = ref<Column[]>([]);
const originalMeasurements = ref([]);

const isLoading = ref(true);
const isChanged = ref(false);

const mainColumnName = computed({
        get: () => columns.value.find(c => c.is_main)?.name ?? '',
        set: (value: string) => {
            columns.value.forEach(c => {
                c.is_main = c.name === value;
            });
        }
    }
);

async function fetchExperiment(id: string) {
    try {
        const response = await api.get(`/experiment/${id}`);
        description.value = response.data.description;
        columns.value = response.data.columns;
        measurements.value = response.data.measurements;
        originalDescription.value = description.value;
        originalColumns.value = JSON.parse(JSON.stringify(columns.value));
        originalMeasurements.value = JSON.parse(JSON.stringify(measurements.value));

        watchEffect(() => {
            if (
                description.value !== originalDescription.value ||
                JSON.stringify(columns.value) !== JSON.stringify(originalColumns.value) ||
                JSON.stringify(measurements.value) !== JSON.stringify(originalMeasurements.value)
            ) {
                isChanged.value = true;
            }
        });
    } catch (error) {
        console.error('Ошибка загрузки эксперимента:', error);
    } finally {
        isLoading.value = false;
    }
}

async function updateExperiment() {
    const patchPayload: Record<string, any> = {};

    if (description.value !== originalDescription.value) {
        patchPayload.description = description.value;
    }
    if (JSON.stringify(columns.value) !== JSON.stringify(originalColumns.value)) {
        patchPayload.columns = columns.value;
    }
    if (JSON.stringify(measurements.value) !== JSON.stringify(originalMeasurements.value)) {
        patchPayload.measurements = measurements.value;
    }

    if (Object.keys(patchPayload).length === 0) return;

    try {
        await api.patch(`/experiment/laboratory/${props.id}`, patchPayload);
    } catch (error) {
        console.error('Ошибка обновления эксперимента:', error);
        throw error;
    }
}

async function saveChanges() {
    try {
        await updateExperiment();
        originalDescription.value = description.value;
        originalColumns.value = JSON.parse(JSON.stringify(columns.value));
        originalMeasurements.value = JSON.parse(JSON.stringify(measurements.value));
        isChanged.value = false;
        Notifier.success({ detail: 'Изменения сохранены' });
    } catch (error) {
        Notifier.error({ detail: error instanceof AxiosError && error.response ? error.response.data.detail : 'Неизвестная ошибка' });
    }
}

onBeforeMount(async () => {
    if (props.id) {
        await fetchExperiment(props.id);
    }
});

onBeforeUnmount(async () => {
    if (isChanged && props.id) {
        await saveChanges();
    }
});
</script>
