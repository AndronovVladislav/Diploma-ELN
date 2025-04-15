<template>
    <div v-if="isLoading" class="flex justify-center">
        <ProgressSpinner />
    </div>
    <div v-else-if="units.length > 0" class="card">
        <div class="flex justify-between items-center mb-3">
            <InputText v-model="filterText" placeholder="Фильтр по названию" />
            <Button @click="toggleAllGroups">
                {{ allExpanded ? 'Свернуть все' : 'Развернуть все' }}
            </Button>
        </div>

        <DataTable
            v-model:expandedRowGroups="expandedRowGroups"
            :value="filteredUnits"
            expandableRowGroups
            rowGroupMode="subheader"
            groupRowsBy="dimension"
            sortMode="single"
            sortField="dimension"
            :sortOrder="1"
            :virtualScrollerOptions="{ itemSize: 50 }"
        >
            <Column field="dimension" header="Dimension" />
            <Column field="label" header="Название" />
            <Column field="comment" header="Комментарий" />
            <Column field="uri" header="URI">
                <template #body="{ data }">
                    <a :href="data.uri" target="_blank" class="text-blue-600 hover:underline">
                        {{ data.uri }}
                    </a>
                </template>
            </Column>
            <template #groupheader="slotProps">
                <span class="align-middle ml-2 font-bold leading-normal">{{ slotProps.data.dimension }}</span>
            </template>
            <template #groupfooter="slotProps">
                <div class="flex justify-end text-sm text-surface px-3 py-1">
                    Total Units:
                    {{ calculateUnitsTotal(slotProps.data.dimension) }}
                </div>
            </template>
        </DataTable>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ProgressSpinner from 'primevue/progressspinner';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import api from '@/api/axios';
import { useNotifier } from '@/composables/useNotifier';

const units = ref<Record<string, any>[]>([]);
const isLoading = ref(true);
const filterText = ref<string>('');
const expandedRowGroups = ref<string[]>([]);
const uniqueDimensions = ref<string[]>([]);
const filteredUnits = ref<Record<string, any>[]>([]);
const Notifier = useNotifier();

const allExpanded = computed(() => {
    return expandedRowGroups.value.length !== 0;
});

watch(filterText, () => {
    filteredUnits.value = units.value.filter(unit => {
        return unit.label.toLowerCase().includes(filterText.value.toLowerCase());
    });
});

const calculateUnitsTotal = (dimension: string) => {
    let total = 0;

    if (units.value) {
        for (let unit of units.value) {
            if (unit.dimension === dimension) {
                total++;
            }
        }
    }

    return total;
};

const toggleAllGroups = () => {
    if (allExpanded.value) {
        expandedRowGroups.value = [];
    } else {
        expandedRowGroups.value = uniqueDimensions.value;
    }
};

onMounted(async () => {
    try {
        const response = await api.get(`/ontology/details/om2`);
        units.value = response.data;
        units.value.sort((a, b) => a.dimension.localeCompare(b.dimension));
        uniqueDimensions.value = [...new Set(units.value.map(unit => unit.dimension))];
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
