<template>
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
        <ProgressSpinner />
    </div>

    <div v-else class="flex flex-col gap-4">
        <Button v-if="isChanged" label="Сохранить изменения" icon="pi pi-save" class="w-fit" @click="saveChanges" />
        <Editor v-model:description="description" />
        <Table v-model:columns="columns" v-model:data="measurements" />
    </div>
</template>

<script lang="ts" setup>
import { onBeforeMount, onBeforeUnmount, ref, watchEffect } from 'vue';
import Editor from '@/components/Editor.vue';
import api from '@/api/axios';
import Table from '@/components/Table.vue';
import ProgressSpinner from 'primevue/progressspinner';
import { Button } from 'primevue';
import { useNotifier } from '@/composables/useNotifier';

const props = defineProps<{ id: string }>();
const Notifier = useNotifier();

const description = ref('');
const columns = ref([]);
const measurements = ref([]);

const originalDescription = ref('');
const originalColumns = ref([]);
const originalMeasurements = ref([]);

const isLoading = ref(true);
const isChanged = ref(false);

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
        await api.patch(`/experiment/${props.id}`, patchPayload);
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
        Notifier.success('Изменения сохранены');
    } catch (error) {
        Notifier.error('Не удалось сохранить изменения');
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
