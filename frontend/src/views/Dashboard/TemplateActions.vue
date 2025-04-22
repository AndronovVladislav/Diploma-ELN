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

const { selectedTemplate, templateFS, moveTemplateDialog } = useDashboard();

interface TemplateActionProps {
    templateId: string;
}

const props = defineProps<TemplateActionProps>();

const moveTemplate = () => {
    selectedTemplate.value = findById(templateFS.value, props.templateId) as Template;
    moveTemplateDialog.value.visible = true;
};

const deleteTemplate = () => {
    removeFromFS(templateFS.value, props.templateId);
};
</script>
