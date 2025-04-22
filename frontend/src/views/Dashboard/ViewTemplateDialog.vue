<template>
    <Dialog v-model:visible="visibleModel.visible" class="w-1/2" header="Просмотр шаблона" modal>
        <TemplateSchemaForm
            v-if="template"
            :name="templateName"
            :folder-options="[]"
            :selected-folder="null"
            :schemas="schemas"
            :readonly="true"
        />
    </Dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { Dialog } from 'primevue';
import TemplateSchemaForm from '@/views/Dashboard/TemplateSchemaForm.vue';
import api from '@/api/axios';
import type { Template } from '@/views/Dashboard/typing';
import { DialogState } from '@/composables/useDashboard';

const props = defineProps<{
    visibleModel: DialogState;
    templateId: string | null;
}>();

const template = ref<Template | null>(null);

const templateName = computed(() => {
    return template.value?.path.split('/').pop() ?? '';
});

const schemas = computed(() => ({
    input: JSON.stringify(template.value?.input ?? {}, null, 2),
    output: JSON.stringify(template.value?.output ?? {}, null, 2),
    parameters: JSON.stringify(template.value?.parameters ?? {}, null, 2),
    context: JSON.stringify(template.value?.context ?? {}, null, 2)
}));

watch(() => props.templateId, async (id) => {
    if (!id) {
        template.value = null;
        return;
    }

    try {
        const response = await api.get(`template/${id}`);
        template.value = response.data;
    } catch (error) {
        console.error('Ошибка загрузки шаблона:', error);
        template.value = null;
    }
});
</script>
