<template>
    <Dialog :visible="visible" modal class="w-1/2" header="Настройки столбца" @update:visible="emit('update:visible', false)">
        <div v-if="column" class="flex flex-col gap-4 w-full">
            <div class="field flex flex-col gap-2 w-full">
                <label for="column_name">Название столбца</label>
                <InputText id="column_name" v-model="editedColumn.name" class="w-full" />
            </div>
            <div class="field flex flex-col gap-2 w-full">
                <label for="ontology">Онтология</label>
                <InputText id="ontology" v-model="editedColumn.ontology" class="w-full" />
            </div>
            <div class="field flex flex-col gap-2 w-full">
                <label for="ontology_ref">Элемент онтологии</label>
                <InputText id="ontology_ref" v-model="editedColumn.ontology_ref" class="w-full" />
            </div>
        </div>
        <template #footer>
            <Button label="Отмена" icon="pi pi-times" class="p-button-text" @click="emit('update:visible', false)" />
            <Button label="Сохранить" icon="pi pi-check" @click="handleSave" />
        </template>
    </Dialog>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';
import { Button, Dialog, InputText } from 'primevue';
import { Column } from '@/views/Editors/LabExperiment/typing';

interface Props {
    visible: boolean;
    column: Column;
}

const props = defineProps<Props>();

const emit = defineEmits<{
    (e: 'update', updated: Column): void;
    (e: 'update:visible', visible: boolean): void;
}>();

const editedColumn = ref<Column>(props.column);
watch(() => props.column, (newVal) => {
        editedColumn.value = { ...newVal };
    },
    { immediate: true }
);

const handleSave = () => {
    if (editedColumn.value) {
        emit('update', editedColumn.value);
    }
    emit('update:visible', false);
};
</script>
