import { Column } from '@/views/Editors/LabExperiment/typing';
import { Ref, ref } from 'vue';
import { RowData } from '@/typing';

export function useTableEditor(
    columns: Ref<Column[]>,
    data: Ref<RowData[]>,
    emit: (e: 'update:columns' | 'update:data', value: Column[] | RowData[]) => void
) {
    const showDialog = ref(false);
    const selectedColumn = ref<Column | null>(null);
    const columnMenus = ref<Record<string, any>>({});

    const openDialog = (column: Column) => {
        selectedColumn.value = column;
        showDialog.value = true;
    };

    const addColumn = () => {
        const id = columns.value.length.toString();
        const newColumn = {
            id: id,
            name: `column_${id}`,
            ontology: '',
            ontology_element: ''
        };
        columns.value.push(newColumn);

        data.value.forEach(row => {
            row[newColumn.name] = '';
        });

        emit('update:columns', columns.value);
        emit('update:data', data.value);
        openDialog(newColumn);
    };

    const deleteColumn = () => {
        if (!selectedColumn.value) return;

        const columnId = selectedColumn.value.id;
        columns.value = columns.value.filter(col => col.id !== columnId);

        data.value.forEach(row => {
            delete row[selectedColumn.value!.name];
        });

        emit('update:columns', columns.value);
        emit('update:data', data.value);
        closeDialog();
    };

    const addRow = () => {
        const newRow: RowData = {};
        columns.value.forEach(col => {
            newRow[col.name] = '';
        });
        data.value.push(newRow);
        emit('update:data', data.value);
    };

    const deleteRow = (index: number) => {
        data.value.splice(index, 1);
        emit('update:data', data.value);
    };

    const closeDialog = () => {
        showDialog.value = false;
    };

    const getColumnMenuItems = (col: Column) => [
        {
            label: 'Настроить',
            icon: 'pi pi-cog',
            command: () => openDialog(col)
        },
        {
            label: 'Удалить',
            icon: 'pi pi-trash',
            command: () => {
                selectedColumn.value = col;
                deleteColumn();
            }
        }
    ];

    return {
        showDialog,
        selectedColumn,
        columnMenus,
        openDialog,
        addColumn,
        addRow,
        deleteRow,
        deleteColumn,
        closeDialog,
        getColumnMenuItems
    };
}
