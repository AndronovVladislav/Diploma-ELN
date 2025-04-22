<template>
    <div class="flex gap-2">
        <Button class="p-button-text p-button-rounded p-button-success" icon="pi pi-external-link"
                @click="moveExperiment" />
        <Button class="p-button-text p-button-rounded p-button-danger" icon="pi pi-trash" @click="deleteExperiment" />
    </div>
</template>

<script lang="ts" setup>
import { Experiment } from '@/views/Dashboard/typing';
import { useDashboard } from '@/composables/useDashboard';
import { findById, removeFromFS } from '@/utils/fileSystem';
import api from '@/api/axios';
import { useNotifier } from '@/composables/useNotifier';

const { selectedExperiment, experimentFS, moveExperimentDialog } = useDashboard();
const Notifier = useNotifier();

interface ExperimentActionProps {
    experimentId: string;
}

const props = defineProps<ExperimentActionProps>();

const moveExperiment = () => {
    selectedExperiment.value = findById(experimentFS.value, props.experimentId) as Experiment;
    moveExperimentDialog.value.visible = true;
};

const deleteExperiment = async () => {
    try {
        await api.delete(`experiment/${props.experimentId}`);
        removeFromFS(experimentFS.value, props.experimentId);
    } catch (error) {
        console.error('Ошибка при удалении эксперимента:', error);
        Notifier.error({ detail: error instanceof Error ? error.message : 'Неизвестная ошибка' });
    }
};
</script>
