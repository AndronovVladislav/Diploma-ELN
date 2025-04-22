<template>
    <Dialog
        v-model:visible="createTemplateDialog.visible"
        class="w-[800px]"
        header="Создать шаблон вычислительного эксперимента"
        modal
        @hide="onHide"
    >
        <TemplateSchemaForm
            :name="templateName"
            :folder-options="formattedFolders(templateFS).value.concat([{ path: '/', id: '-1' }])"
            :selected-folder="selectedFolder"
            :schemas="{
                input: input,
                output: output,
                parameters: parameters,
                context: context
            }"
        />

        <template #footer>
            <Button class="p-button-text" label="Отмена" @click="onHide" />
            <Button class="p-button p-button-success" label="Создать" @click="onCreateTemplate" />
        </template>
    </Dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Button, Dialog } from 'primevue';
import TemplateSchemaForm from '@/views/Dashboard/TemplateSchemaForm.vue';

import { useDashboard } from '@/composables/useDashboard';
import { useNotifier } from '@/composables/useNotifier';
import { Folder, SimplifiedView } from '@/views/Dashboard/typing';
import { findById } from '@/utils/fileSystem';
import api from '@/api/axios';

const { createTemplateDialog, formattedFolders, templateFS } = useDashboard();
const Notifier = useNotifier();

const templateName = ref('');
const selectedFolder = ref<SimplifiedView | null>(null);

const input = ref('');
const output = ref('');
const parameters = ref('');
const context = ref('');

function onHide() {
    createTemplateDialog.value.visible = false;
    templateName.value = '';
    selectedFolder.value = null;
    input.value = '';
    output.value = '';
    parameters.value = '';
    context.value = '';
}

async function onCreateTemplate() {
    try {
        const fields = {
            input,
            output,
            parameters,
            context
        };

        const parsedSchemas: Record<string, any> = {};

        for (const [key, value] of Object.entries(fields)) {
            try {
                parsedSchemas[key] = JSON.parse(value.value);
            } catch {
                throw new Error(`Поле "${key}" содержит некорректный JSON`);
            }
        }

        const prefix = selectedFolder.value?.path === '/' ? '' : `/${selectedFolder.value?.path}`;
        const response = await api.post('/template', {
            path: `${prefix}/${templateName.value}`,
            input: parsedSchemas.input,
            output: parsedSchemas.output,
            parameters: parsedSchemas.parameters,
            context: parsedSchemas.context
        });

        const newTemplate = {
            id: response.data.id,
            path: templateName.value
        };

        if (selectedFolder.value) {
            const parentFolder = findById(templateFS.value, selectedFolder.value.id) as Folder;
            if (parentFolder) {
                parentFolder.children.push(newTemplate);
            } else if (selectedFolder.value.id === '-1') {
                templateFS.value.push(newTemplate);
            }
        }

        onHide();
    } catch (error) {
        console.error('Ошибка при создании шаблона:', error);
        Notifier.error({ detail: error instanceof Error ? error.message : 'Неизвестная ошибка' });
    }
}
</script>
