<template>
    <div class="p-4">
        <h2 class="text-xl font-bold mb-4">Редактирование вычислительного эксперимента</h2>

        <div class="mb-4">
            <label class="font-semibold" for="title">Название:</label>
            <InputText id="title" v-model="experiment.title" class="w-full mt-1" />
        </div>

        <h3 class="text-lg font-semibold mt-6 mb-2">Шаблон эксперимента</h3>
        <div v-for="(field, key) in schemas" :key="key" class="mb-4">
            <label class="font-semibold">{{ field.label }} (JSON):</label>
            <Textarea v-model="experiment[key]" class="w-full mt-1" rows="4" />
        </div>

        <h3 class="text-lg font-semibold mt-6 mb-2">Конкретные данные</h3>
        <div v-for="(field, key) in dataFields" :key="key" class="mb-4">
            <label class="font-semibold">{{ field.label }} (JSON):</label>
            <Textarea v-model="experiment[key]" class="w-full mt-1" rows="4" />
        </div>

        <div class="mt-6 flex gap-2">
            <Button class="p-button-success" label="Сохранить" @click="saveExperiment" />
            <Button class="p-button-secondary" label="Отмена" @click="cancelEdit" />
        </div>
    </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Button, InputText, Textarea } from 'primevue';

interface CompExperiment {
    id: string | null;
    title: string;
    inputSchema: string;
    outputSchema: string;
    parametersSchema: string;
    contextSchema: string;
    inputData: string;
    outputData: string;
    parametersData: string;
    contextData: string;
}

const route = useRoute();
const router = useRouter();

const experiment = ref<CompExperiment>({
    id: route.params.id as string || null,
    title: '',
    inputSchema: '',
    outputSchema: '',
    parametersSchema: '',
    contextSchema: '',
    inputData: '',
    outputData: '',
    parametersData: '',
    contextData: ''
});

const schemas = reactive({
    inputSchema: { label: 'Входные данные' },
    outputSchema: { label: 'Выходные данные' },
    parametersSchema: { label: 'Параметры' },
    contextSchema: { label: 'Контекст' }
});

const dataFields = reactive({
    inputData: { label: 'Входные данные' },
    outputData: { label: 'Выходные данные' },
    parametersData: { label: 'Параметры' },
    contextData: { label: 'Контекст' }
});

const saveExperiment = () => {
    console.log('Сохранение вычислительного эксперимента', experiment.value);
    router.push('/experiments');
};

const cancelEdit = () => {
    router.push('/experiments');
};
</script>
