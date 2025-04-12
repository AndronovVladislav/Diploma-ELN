<template>
    <div class="card">
        <div v-if="isLoading" class="flex justify-center items-center h-screen">
            <ProgressSpinner />
        </div>
        <div v-else>
            <h2>Доступные онтологии</h2>
            <InputText v-model="search" placeholder="Поиск..." class="mb-3" />

            <div class="grid gap-4" style="grid-template-columns: repeat(2, 1fr)">
                <RouterLink
                    v-for="ontology in filteredOntologies"
                    :to="`/ontology/details/${ontology}`"
                    class="p-4 border border-primary rounded-md aspect-auto text-center block"
                >
                    <h2>{{ ontology }}</h2>
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import InputText from 'primevue/inputtext';
import api from '@/api/axios';
import ProgressSpinner from 'primevue/progressspinner';

const isLoading = ref(true);

const search = ref('');
const ontologies = ref<string[]>([]);

async function fetchOntologies() {
    try {
        const response = await api.get(`/ontology/`);
        ontologies.value = response.data;
    } catch (error) {
        console.error('Ошибка загрузки списка онтологий:', error);
    } finally {
        isLoading.value = false;
    }
}

const filteredOntologies = ref<string[]>([]);

watch([ontologies, search], () => {
    if (!search.value.trim()) {
        filteredOntologies.value = ontologies.value;
    } else {
        filteredOntologies.value = ontologies.value.filter(o =>
            o.toLowerCase().includes(search.value.toLowerCase())
        );
    }
}, { immediate: true });

onMounted(async () => {
    await fetchOntologies();
});
</script>
