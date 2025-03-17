<template>
    <div class="flex flex-col gap-4">
        <Editor :description="experiment.description" />
        <div class="rounded-lg">
            <Table :columns="experiment.columns" :data="experiment.data" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Editor from '@/components/Editor.vue';
import api from '@/api/axios';
import { findById } from '@/views/utils';
import { Experiment } from '@/views/Dashboard/typing';
import { useDashboardStore } from '@/stores/dashboard';
import Table from '@/components/Table.vue';

const props = defineProps<{ id: string }>();
const dashboardStore = useDashboardStore();


const experiment = ref({
    description: '',
    columns: [],
    data: []
});

// const saveExperiment = async () => {
//     try {
//         await fetch('/api/experiments', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify(experiment.value)
//         });
//         useToast().add({ severity: 'success', summary: 'Успех', detail: 'Эксперимент сохранён!' });
//     } catch (error) {
//         console.error('Ошибка сохранения:', error);
//     }
// };

async function fetchExperiment(id: string) {
    try {
        console.log(dashboardStore.experimentFS);
        const kind = (findById(dashboardStore.experimentFS, id) as Experiment).kind;
        const params = new URLSearchParams();

        params.append('kind', kind);

        const response = await api.get(`/experiment/${id}?${params.toString()}`);
        experiment.value = response.data;
    } catch (error) {
        console.error('Ошибка загрузки эксперимента:', error);
    }
}

onMounted(async () => {
    if (props.id) {
        await dashboardStore.fetchExperimentFS();
        await fetchExperiment(props.id);
    }
});
</script>
