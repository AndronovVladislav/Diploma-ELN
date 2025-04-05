<template>
    <div class="flex gap-2">
        <Button class="p-button-text p-button-rounded p-button-success" icon="pi pi-external-link"
                @click="moveExperiment" />
        <Button class="p-button-text p-button-rounded p-button-danger" icon="pi pi-trash" @click="deleteExperiment" />
    </div>
</template>

<script lang="ts" setup>
import { Experiment } from '@/views/Dashboard/typing';
import { useDashboardStore } from '@/stores/dashboard';
import { findById, removeExperiment } from '@/utils/fileSystem';

const dashboardStore = useDashboardStore();

interface ExperimentActionProps {
    experimentId: string;
}

const props = defineProps<ExperimentActionProps>();

const moveExperiment = () => {
    dashboardStore.selectedExperiment = findById(dashboardStore.experimentFS, props.experimentId) as Experiment;
    dashboardStore.moveExperimentDialog.visible = true;
};

const deleteExperiment = () => {
    removeExperiment(dashboardStore.experimentFS, props.experimentId);
};
</script>
