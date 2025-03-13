<template>
    <Editor/>
    <!--    <div class="w-full p-4">-->
    <!--        <Card>-->
    <!--            <template #content>-->
    <!--                <div class="mb-4">-->
    <!--                    <h2 class="text-xl font-bold">Редактор эксперимента</h2>-->
    <!--                    <Editor v-model="experiment.description" :modules="editorModules" />-->
    <!--                </div>-->

    <!--                <DataTable :value="experiment.data" editable>-->
    <!--                    <Column field="name" header="Название"></Column>-->
    <!--                    <Column field="value" header="Значение">-->
    <!--                        <template #editor="slotProps">-->
    <!--                            <InputText v-model="slotProps.data.value" />-->
    <!--                        </template>-->
    <!--                    </Column>-->
    <!--                    <Column field="ontology" header="Онтология">-->
    <!--                        <template #editor="slotProps">-->
    <!--                            <Select v-model="slotProps.data.ontology" :options="ontologies" optionLabel="label" />-->
    <!--                        </template>-->
    <!--                    </Column>-->
    <!--                    <Column header="Действия">-->
    <!--                        <template #body="slotProps">-->
    <!--                            <Button icon="pi pi-trash" class="p-button-danger" @click="removeRow(slotProps.index)" />-->
    <!--                        </template>-->
    <!--                    </Column>-->
    <!--                </DataTable>-->

    <!--                <Button label="Добавить строку" @click="addRow" class="mt-2" />-->
    <!--                <Button label="Сохранить" class="mt-2 p-button-success" @click="saveExperiment" />-->
    <!--            </template>-->
    <!--        </Card>-->
    <!--    </div>-->
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import Editor from '@/components/Editor.vue';

const route = useRoute();

const props = defineProps<{ id: string }>();

const experiment = ref({
    description: '',
    data: []
});

const editorModules = ref({
    toolbar: [
        [{ header: [1, 2, 3, false] }],
        ['bold', 'italic', 'underline'],
        [{ list: 'ordered' }, { list: 'bullet' }],
        ['clean']
    ]
});

const ontologies = ref([
    { label: 'OM2: Длина (м)', value: 'om2:length' },
    { label: 'CHEBI: Вещество', value: 'chebi:compound' }
]);

const addRow = () => {
    experiment.value.data.push({ name: '', value: '', ontology: null });
};

const removeRow = (index) => {
    experiment.value.data.splice(index, 1);
};

// const saveExperiment = async () => {
//     try {
//         await fetch('/api/experiments', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify(experiment.value)
//         });
//         useToast().add({ severity: 'success', summary: 'Успех', detail: 'Эксперимент сохранён!' });
//     } catch (error) {
//         console.error('Ошибка сохранения:', error);
//     }
// };

async function fetchExperiment(id: string) {
    try {
        const response = await fetch(`/api/experiments/${id}`);
        experiment.value = await response.json();
    } catch (error) {
        console.error('Ошибка загрузки эксперимента:', error);
    }
}

// onMounted(() => {
//     if (route.params.id) {
//         fetchExperiment(route.params.id);
//     }
// });
</script>

<style lang="scss">
//.ProseMirror {
//    border: 1px solid;
//    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
//    border-radius: 8px;
//    padding: 12px;
//    min-height: 250px;
//    //background: white;
//}
//
//.editor-container {
//    border: 1px solid;
//    border-radius: 8px;
//    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
//    //background: white;
//}
//
//.editor-toolbar {
//    border-bottom: 1px solid #ddd;
//    padding: 8px;
//    //background: #f8f8f8;
//    border-top-left-radius: 8px;
//    border-top-right-radius: 8px;
//    display: flex;
//    gap: 8px;
//}
//
//.editor-toolbar button {
//    border: none;
//    background: none;
//    cursor: pointer;
//    font-size: 16px;
//    padding: 4px 8px;
//}
//
//.editor-toolbar button.is-active {
//    font-weight: bold;
//    color: #007bff;
//}
</style>
