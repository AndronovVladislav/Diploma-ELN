<template>
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
        <ProgressSpinner />
    </div>

    <div v-else class="flex flex-col gap-4">
        <Editor :description="description" />
        <Table :columns="columns" :data="data" />
    </div>
</template>

<script lang="ts" setup>
import { onBeforeMount, ref } from 'vue';
import Editor from '@/components/Editor.vue';
import api from '@/api/axios';
import { findById } from '@/views/utils';
import { Experiment } from '@/views/Dashboard/typing';
import { useDashboardStore } from '@/stores/dashboard';
import Table from '@/components/Table.vue';
import ProgressSpinner from 'primevue/progressspinner';

const props = defineProps<{ id: string }>();
const dashboardStore = useDashboardStore();

const description = ref('');
const columns = ref([]);
const data = ref([]);
const isLoading = ref(true);

async function fetchExperiment(id: string) {
    try {
        isLoading.value = true;
        await dashboardStore.fetchExperimentFS();

        const kind = (findById(dashboardStore.experimentFS, id) as Experiment).kind;
        const params = new URLSearchParams();
        params.append('kind', kind);

        const response = await api.get(`/experiment/${id}?${params.toString()}`);
        description.value = response.data.description;
        columns.value = response.data.columns;
        data.value = response.data.data;
    } catch (error) {
        console.error('Ошибка загрузки эксперимента:', error);
    } finally {
        isLoading.value = false;
    }
}

onBeforeMount(async () => {
    if (props.id) {
        await fetchExperiment(props.id);
    }
});
</script>
