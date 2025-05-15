<template>
    <div class="flex gap-2">
        <SplitButton
          :model="exportItems"
          class="p-button-text p-button-rounded p-button-info"
          icon="pi pi-download"
        />
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
import { Button, SplitButton } from 'primevue';

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
        Notifier.success({ detail: 'Эксперимент удалён' });
    } catch (error) {
        console.error('Ошибка при удалении эксперимента:', error);
        Notifier.error({ detail: error instanceof Error ? error.message : 'Неизвестная ошибка' });
    }
};

const exportItems = [
  {
    label: 'JSON',
    icon: 'pi pi-file',
    command: () => exportExperiment('json' as const)
  },
  {
    label: 'XML',
    icon: 'pi pi-file',
    command: () => exportExperiment('xml' as const)
  }
];

const exportExperiment = async (type: 'json' | 'xml' = 'json') => {
    try {
        const response = await api.get(`experiment/export/${props.experimentId}`, {
            params: { export_type: type },
            responseType: 'blob'
        });
        const url = URL.createObjectURL(response.data);
        const link = document.createElement('a');
        link.href = url;
        const disposition = response.headers['Content-Disposition'];
        let filename = `experiment-${props.experimentId}.json`;
        if (disposition) {
            const filenameMatch = disposition.match(/filename="?(.+)"?/);
            if (filenameMatch && filenameMatch[1]) {
                filename = filenameMatch[1];
            }
        }
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
        Notifier.success({ detail: 'Экспорт завершён' });
    } catch (error) {
        console.error('Ошибка при экспорте эксперимента:', error);
        Notifier.error({ detail: error instanceof Error ? error.message : 'Неизвестная ошибка' });
    }
};
</script>
