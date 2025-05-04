<template>
    <div class="flex justify-content-end">
        <Button class="p-button-text p-button-rounded p-button-success" icon="pi pi-external-link"
                @click="moveTemplate" />
        <Button class="p-button-text p-button-rounded p-button-danger" icon="pi pi-trash" @click="deleteTemplate" />
    </div>
</template>

<script setup lang="ts">
import { Button } from 'primevue';
import { Template } from '@/views/Dashboard/typing';
import { useDashboard } from '@/composables/useDashboard';
import { findById, removeFromFS } from '@/utils/fileSystem';
import api from '@/api/axios';
import { useNotifier } from '@/composables/useNotifier';
import { AxiosError } from 'axios';

interface TemplateActionProps {
    templateId: string;
}

const props = defineProps<TemplateActionProps>();

const { selectedTemplate, templateFS, moveTemplateDialog } = useDashboard();
const Notifier = useNotifier();

const moveTemplate = () => {
    selectedTemplate.value = findById(templateFS.value, props.templateId) as Template;
    moveTemplateDialog.value.visible = true;
};

const deleteTemplate = async () => {
    try {
        await api.delete(`template/${props.templateId}`);
        removeFromFS(templateFS.value, props.templateId);
    } catch (error) {
        console.error('Ошибка при удалении эксперимента:', error);
        Notifier.error({ detail: error instanceof AxiosError && error.response ? error.response.data : 'Неизвестная ошибка' });
    }
};
</script>
