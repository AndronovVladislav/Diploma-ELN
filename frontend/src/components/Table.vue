<template>
    <DataTable :value="data">
        <Column v-for="col of props.columns" :key="col.name" :header="col.name">
            <template #header>
                <div class="flex items-center gap-2">
                    <Button icon="pi pi-link" class="p-button-text p-button-sm" @click="toggleMenu" />
                </div>
            </template>
            <template #body="slotProps">
                {{ slotProps.data.name }}
            </template>
        </Column>
    </DataTable>

    <Popover ref="menu">
        <p>Настройки заголовка...</p>
    </Popover>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Popover } from 'primevue';

interface Props {
    columns: {name: string, ontology: string}[]
}

const props = defineProps<Props>();

const menu = ref(null);
const data = ref([
    { id: 1, name: 'Элемент 1' },
    { id: 2, name: 'Элемент 2' }
]);

const toggleMenu = (event) => {
    menu.value.toggle(event);
};
</script>
