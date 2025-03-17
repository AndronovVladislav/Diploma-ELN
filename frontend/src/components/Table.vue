<template>
    <DataTable :value="data">
        <Column v-for="col of props.columns" :key="col.name" :header="col.name">
            <template #header>
                <div class="flex items-center gap-2">
                    <Button icon="pi pi-link" class="p-button-text p-button-sm" @click="openDialog(col)" />
                </div>
            </template>
            <template #body="slotProps">
                <InputText
                    v-model="slotProps.data[col.name]"
                    class="w-fit"
                    @update:modelValue="updateValue(slotProps.data, col.name, $event)"
                />
            </template>
        </Column>
    </DataTable>

    <Dialog v-model:visible="showDialog" header="Настройки онтологии" :modal="true" class="w-1/2">
        <div v-if="selectedColumn" class="flex flex-col gap-4 w-full">
            <p><strong>Столбец:</strong> {{ selectedColumn.name }}</p>
            <div class="field flex flex-col gap-2 w-full">
                <label for="ontology">Онтология</label>
                <InputText id="ontology" v-model="selectedColumn.ontology" class="w-full" />
            </div>
            <div class="field flex flex-col gap-2 w-full">
                <label for="ontology_element">Элемент онтологии</label>
                <InputText id="ontology_element" v-model="selectedColumn.ontology_element" class="w-full" />
            </div>
        </div>
        <template #footer>
            <Button label="Закрыть" icon="pi pi-times" @click="showDialog = false" />
        </template>
    </Dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Button, Dialog, InputText } from 'primevue';

interface Props {
    columns: {
        name: string,
        ontology: string,
        ontology_element: string,
    }[],
    data: object[],
}

const props = defineProps<Props>();

const showDialog = ref(false);
const selectedColumn = ref<{ name: string; ontology: string; ontology_element: string } | null>(null);

const openDialog = (column) => {
    selectedColumn.value = { ...column };
    showDialog.value = true;
};

const updateValue = (row, columnName, newValue) => {
    row[columnName] = newValue;
};
</script>
