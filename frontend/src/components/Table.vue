<template>
    <div class="table-container relative">
        <DataTable :value="data">
            <Column v-for="col of columns" :key="col.name" :header="col.name">
                <template #header>
                    <div class="flex items-center gap-2">
                        <Button class="p-button-text p-button-sm" icon="pi pi-link" @click="openDialog(col)" />
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

            <Column>
                <template #header>
                    <Button class="p-button-sm p-button-outlined" icon="pi pi-plus" @click="addColumn" />
                </template>
            </Column>
        </DataTable>

        <div class="flex justify-center mt-2">
            <Button class="p-button-sm p-button-outlined" icon="pi pi-plus" label="Добавить строку" @click="addRow" />
        </div>
    </div>

    <Dialog v-model:visible="showDialog" :modal="true" class="w-1/2" header="Настройки столбца">
        <div v-if="selectedColumn" class="flex flex-col gap-4 w-full">
            <div class="field flex flex-col gap-2 w-full">
                <label for="column_name">Название столбца</label>
                <InputText id="column_name" v-model="selectedColumn.name" class="w-full" />
            </div>
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
            <Button icon="pi pi-times" label="Закрыть" @click="closeDialog()" />
        </template>
    </Dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { Button, Dialog, InputText } from 'primevue';

interface Column {
    name: string;
    ontology: string;
    ontology_element: string;
}

interface RowData {
    [key: string]: string;
}

interface Props {
    columns: Column[];
    data: RowData[];
}

const props = defineProps<Props>();
const columns = ref([...props.columns]);
const data = ref([...props.data]);

const showDialog = ref(false);
const selectedColumn = ref<Column | null>(null);

const openDialog = (column: Column) => {
    selectedColumn.value = column;
    showDialog.value = true;
};

const updateValue = (row: RowData, columnName: string, newValue: string) => {
    row[columnName] = newValue;
};

const addColumn = () => {
    console.log(columns);
    const newColumn = { name: `column_${columns.value.length + 1}`, ontology: '', ontology_element: '' };
    columns.value.push(newColumn);

    data.value.forEach(row => {
        row[newColumn.name] = '';
    });

    openDialog(newColumn);
};

const addRow = () => {
    const newRow: RowData = {};
    columns.value.forEach(col => {
        newRow[col.name] = '';
    });
    data.value.push(newRow);
};

const updateColumnName = () => {
    if (!selectedColumn.value) return;

    const columnIndex = columns.value.findIndex(col => col.name === selectedColumn.value!.oldName);

    if (columnIndex !== -1) {
        Object.assign(columns.value[columnIndex], { name: selectedColumn.value!.name });
    }
};

const closeDialog = () => {
    updateColumnName();
    showDialog.value = false;
};
</script>
