<template>
    <div class="p-4">
        <h2 class="text-xl font-bold mb-4">Редактирование лабораторного эксперимента</h2>

        <div class="mb-4">
            <label class="font-semibold" for="title">Название:</label>
            <InputText id="title" v-model="experiment.title" class="w-full mt-1" />
        </div>

        <div class="mb-4">
            <label class="font-semibold" for="description">Описание:</label>
            <Textarea id="description" v-model="experiment.description" class="w-full mt-1" rows="4" />
        </div>

        <h3 class="text-lg font-semibold mt-6 mb-2">Таблица измерений</h3>
        <DataTable :value="experiment.measurements" class="w-full" editMode="cell" responsiveLayout="scroll">
            <Column field="name" header="Параметр">
                <template #editor="{ data }">
                    <InputText v-model="data.name" />
                </template>
            </Column>
            <Column field="value" header="Значение">
                <template #editor="{ data }">
                    <InputText v-model="data.value" />
                </template>
            </Column>
            <Column field="unit" header="Единицы">
                <template #editor="{ data }">
                    <Select v-model="data.unit" :options="units" class="w-full" optionLabel="label"
                            optionValue="value" />
                </template>
            </Column>
            <Column header="Действия">
                <template #body="{ index }">
                    <Button class="p-button-danger p-button-text" icon="pi pi-trash" @click="removeRow(index)" />
                </template>
            </Column>
        </DataTable>

        <Button class="mt-2" label="Добавить строку" @click="addRow" />

        <div class="mt-6 flex gap-2">
            <Button class="p-button-success" label="Сохранить" @click="saveExperiment" />
            <Button class="p-button-secondary" label="Отмена" @click="cancelEdit" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Button, Column, DataTable, InputText, Select, Textarea } from 'primevue';

interface Measurement {
    name: string;
    value: string;
    unit: string;
}

interface LabExperiment {
    id: string | null;
    title: string;
    description: string;
    measurements: Measurement[];
}

const route = useRoute();
const router = useRouter();

const experiment = ref<LabExperiment>({
    id: route.params.id as string || null,
    title: '',
    description: '',
    measurements: []
});

const units = ref([
    { label: 'Сантиметры', value: 'см' },
    { label: 'Метры', value: 'м' },
    { label: 'Килограммы', value: 'кг' },
    { label: 'Граммы', value: 'г' },
    { label: 'Литры', value: 'л' }
]);

const addRow = () => {
    experiment.value.measurements.push({ name: '', value: '', unit: 'см' });
};

const removeRow = (index: number) => {
    experiment.value.measurements.splice(index, 1);
};

const saveExperiment = () => {
    console.log('Сохранение эксперимента', experiment.value);
    router.push('/experiments');
};

const cancelEdit = () => {
    router.push('/experiments');
};
</script>
