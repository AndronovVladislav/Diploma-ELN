<template>
    <div class="card relative">
        <DataTable v-model:value="tableData" edit-mode="cell" @cell-edit-complete="onCellEditComplete" striped-rows>
            <Column class="!text-center">
                <template #header>
                    <div class="w-full">
                        <Button class="p-button-sm p-button-outlined" icon="pi pi-plus" @click="addColumn" />
                    </div>
                </template>
                <template #body="slotProps">
                    <Button icon="pi pi-trash" @click="deleteRow(slotProps.index)" />
                </template>
            </Column>

            <Column v-for="col of columnsInfo" :key="col.id" :field="col.name">
                <template #header>
                    <div class="flex items-center justify-between">
                        <span>{{ col.name }}</span>
                        <div class="flex items-center gap-1">
                            <Button
                                :icon="col.name === props.mainColumn ? 'pi pi-star-fill' : 'pi pi-star'"
                                class="p-button-text p-button-sm"
                                @click="emit('update:mainColumn', col.name)"
                                :aria-label="col.name === props.mainColumn ? 'Главный столбец' : 'Сделать главным'"
                            />
                            <Menu :ref="el => columnMenus[col.id] = el" :model="getColumnMenuItems(col)" popup />
                            <Button
                                icon="pi pi-ellipsis-v"
                                class="p-button-text p-button-sm"
                                @click="columnMenus[col.id]?.toggle($event)"
                            />
                        </div>
                    </div>
                </template>
                <template #editor="{ data, field }">
                    <InputText v-model="data[field]" />
                </template>
            </Column>
        </DataTable>

        <div class="flex justify-center mt-2">
            <Button class="p-button-sm p-button-outlined" icon="pi pi-plus" label="Добавить строку" @click="addRow" />
        </div>
    </div>

    <EditColumnDialog
        v-if="selectedColumn"
        v-model:visible="showDialog"
        :column="selectedColumn"
        @update="onColumnUpdate"
        @delete="deleteColumn"
        @close="closeDialog"
    />
</template>

<script lang="ts" setup>
import { Button, InputText, Menu } from 'primevue';
import EditColumnDialog from '@/views/Editors/LabExperiment/EditColumnDialog.vue';
import type { Column } from '@/views/Editors/LabExperiment/typing';
import { useTableEditor } from '@/composables/useTableEditor';
import { ref } from 'vue';
import { RowData } from '@/typing';

const emit = defineEmits<{
    (e: 'update:columns', value: Column[]): void
    (e: 'update:data', value: RowData[]): void
    (e: 'update:mainColumn', value: string): void
}>();

interface Props {
    columns: Column[];
    data: RowData[];
    mainColumn: string;
}

const props = defineProps<Props>();
const tableData = ref(props.data);
const columnsInfo = ref(props.columns);

const {
    showDialog,
    selectedColumn,
    columnMenus,
    addColumn,
    addRow,
    deleteRow,
    deleteColumn,
    closeDialog,
    getColumnMenuItems
} = useTableEditor(columnsInfo, tableData, emit);

const onColumnUpdate = (updated: Column) => {
    const columnIndex = columnsInfo.value.findIndex(col => col.id === updated.id);
    if (columnIndex !== -1) {
        columnsInfo.value[columnIndex] = updated;
        emit('update:columns', columnsInfo.value);
    }
};

const onCellEditComplete = (e: any) => {
    const { data, field, newValue } = e;
    if (data[field] !== newValue) {
        data[field] = newValue;
        emit('update:data', tableData.value);
    }
};
</script>
