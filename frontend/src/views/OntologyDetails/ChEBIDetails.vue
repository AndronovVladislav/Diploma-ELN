<template>
    <div v-if="isLoading" class="flex justify-center">
        <ProgressSpinner />
    </div>
    <div v-else-if="units.length > 0" class="card">
        <h2>Онтология: ChEBI</h2>

        <div class="flex justify-between items-center mb-3">
            <InputText v-model="filterText" placeholder="Фильтр по названию" />
        </div>

        <DataTable :value="filteredUnits" :virtualScrollerOptions="{ itemSize: 50 }">
            <Column field="label" header="Название" />
            <Column field="comment" header="Комментарий" />
            <Column field="uri" header="URI">
                <template #body="{ data }">
                    <a :href="data.uri" target="_blank" class="text-blue-600 hover:underline">
                        {{ data.uri }}
                    </a>
                </template>
            </Column>
        </DataTable>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ProgressSpinner from 'primevue/progressspinner';
import InputText from 'primevue/inputtext';
import api from '@/api/axios';
import { useNotifier } from '@/composables/useNotifier';

const Notifier = useNotifier();
const units = ref<Record<string, any>[]>([]);
const isLoading = ref(true);
const filterText = ref<string>('');
const filteredUnits = ref<Record<string, any>[]>([]);

watch(filterText, () => {
    filteredUnits.value = units.value.filter(unit => {
        return unit.label.toLowerCase().includes(filterText.value.toLowerCase());
    });
});

onMounted(async () => {
    try {
        const response = await api.get(`/ontology/details/chebi`);
        units.value = response.data;
        filteredUnits.value = units.value.filter(unit => {
            return unit.label.toLowerCase().includes(filterText.value.toLowerCase());
        });
    } catch (error) {
        Notifier.error('Ошибка загрузки списка элементов онтологии');
        console.error('Ошибка загрузки списка элементов онтологии:', error);
    } finally {
        isLoading.value = false;
    }
});
</script>
