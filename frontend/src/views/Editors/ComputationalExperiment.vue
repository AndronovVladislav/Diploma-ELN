<template>
    <div v-if="isLoading" class="flex justify-center items-center h-screen">
        <ProgressSpinner />
    </div>

    <div v-else class="flex flex-col gap-4">
        <Button v-if="isChanged" label="Сохранить изменения" icon="pi pi-save" class="w-fit" @click="saveChanges" />
        <Panel toggleable>
            <template #header>
                <div>
                    <span class="text-xl font-bold">Description</span>
                </div>
            </template>
            <Editor v-model:description="description" />
        </Panel>
        <Panel toggleable>
            <template #header>
                <div>
                    <span class="text-xl font-bold">Template</span>
                </div>
            </template>
            <TemplateSchemaForm
                v-if="template"
                :name="template.path"
                :folder-options="[]"
                :selected-folder="null"
                :schemas="schemas"
                :readonly="true"
            />
        </Panel>
        <Panel toggleable>
            <template #header>
                <div>
                    <span class="text-xl font-bold">Data</span>
                </div>
            </template>
            <DataTable v-model:value="data" edit-mode="cell" @cell-edit-complete="onCellEditComplete" striped-rows>
                <Column field="input" header="Input">
                    <template #editor="{ data, field }">
                        <Textarea
                            autoresize
                            v-model="data[field]"
                            @keydown.enter.stop
                            @keydown.shift.enter.stop
                        />
                    </template>
                </Column>
                <Column field="output" header="Output">
                    <template #editor="{ data, field }">
                        <Textarea
                            autoresize
                            v-model="data[field]"
                            @keydown.enter.stop
                            @keydown.shift.enter.stop
                        />
                    </template>
                </Column>
                <Column field="parameters" header="Parameters">
                    <template #editor="{ data, field }">
                        <Textarea
                            autoresize
                            v-model="data[field]"
                            @keydown.enter.stop
                            @keydown.shift.enter.stop
                        />
                    </template>
                </Column>
                <Column field="context" header="Context">
                    <template #editor="{ data, field }">
                        <Textarea
                            autoresize
                            v-model="data[field]"
                            @keydown.enter.stop
                            @keydown.shift.enter.stop
                        />
                    </template>
                </Column>
                <Column header="Действия">
                    <template #body="{ index }">
                        <Button
                            icon="pi pi-trash"
                            class="p-button-sm"
                            @click="removeRow(index)"
                        />
                    </template>
                </Column>
            </DataTable>

            <div class="flex justify-center mt-2">
                <Button class="p-button-sm p-button-outlined" icon="pi pi-plus" label="Добавить строку"
                        @click="addRow" />
            </div>
        </Panel>
    </div>
</template>

<script lang="ts" setup>
import { onBeforeMount, onBeforeUnmount, ref, watchEffect } from 'vue';
import Editor from '@/components/Editor.vue';
import ProgressSpinner from 'primevue/progressspinner';
import { Button, Column, DataTable, Panel, Textarea } from 'primevue';
import api from '@/api/axios';
import { useNotifier } from '@/composables/useNotifier';
import TemplateSchemaForm from '@/views/Dashboard/TemplateSchemaForm.vue';
import type { Template } from '@/views/Dashboard/typing';

interface Props {
    id: string;
}

const props = defineProps<Props>();
const Notifier = useNotifier();

const description = ref('');
const data = ref<any[]>([]);

const originalDescription = ref('');
const originalData = ref<any[]>([]);

const isLoading = ref(true);
const isChanged = ref(false);

const template = ref<Template | null>(null);
const schemas = ref({
    input: '{}',
    output: '{}',
    parameters: '{}',
    context: '{}'
});

async function fetchExperiment(id: string) {
    try {
        const response = await api.get(`/experiment/${id}`);
        description.value = response.data.description;
        data.value = response.data.data.map((row: any) => ({
            input: JSON.stringify(row.input, null, 2),
            output: JSON.stringify(row.output, null, 2),
            parameters: JSON.stringify(row.parameters, null, 2),
            context: JSON.stringify(row.context, null, 2)
        }));

        originalDescription.value = description.value;
        originalData.value = JSON.parse(JSON.stringify(data.value));

        if (response.data.template) {
            template.value = response.data.template;

            schemas.value = {
                input: JSON.stringify(template.value?.input ?? {}, null, 2),
                output: JSON.stringify(template.value?.output ?? {}, null, 2),
                parameters: JSON.stringify(template.value?.parameters ?? {}, null, 2),
                context: JSON.stringify(template.value?.context ?? {}, null, 2)
            };
        }

        watchEffect(() => {
            if (
                description.value !== originalDescription.value ||
                JSON.stringify(data.value) !== JSON.stringify(originalData.value)
            ) {
                isChanged.value = true;
            }
        });
    } catch (error) {
        console.error('Ошибка загрузки эксперимента:', error);
    } finally {
        isLoading.value = false;
    }
}

async function updateExperiment() {
    const patchPayload: Record<string, any> = {};

    if (description.value !== originalDescription.value) {
        patchPayload.description = description.value;
    }
    if (JSON.stringify(data.value) !== JSON.stringify(originalData.value)) {
        patchPayload.data = data.value.map(row => [
            JSON.parse(row.input),
            JSON.parse(row.output),
            JSON.parse(row.parameters),
            JSON.parse(row.context)
        ]);
    }

    if (Object.keys(patchPayload).length === 0) return;

    try {
        await api.patch(`/experiment/computational/${props.id}`, patchPayload);
    } catch (error) {
        console.error('Ошибка обновления эксперимента:', error);
        throw error;
    }
}

async function saveChanges() {
    try {
        await updateExperiment();
        originalDescription.value = description.value;
        originalData.value = JSON.parse(JSON.stringify(data.value));
        isChanged.value = false;
        Notifier.success({ detail: 'Изменения сохранены' });
    } catch (error) {
        Notifier.error({ detail: 'Не удалось сохранить изменения' });
    }
}

function addRow() {
    data.value.push({
        input: '{}',
        output: '{}',
        parameters: '{}',
        context: '{}'
    });
}

function removeRow(index: number) {
    data.value.splice(index, 1);
}

const onCellEditComplete = (e: any) => {
    const { data, field, newValue } = e;
    if (data[field] !== newValue) {
        data[field] = newValue;
    }
};

onBeforeMount(async () => {
    if (props.id) {
        await fetchExperiment(props.id);
    }
});

onBeforeUnmount(async () => {
    if (isChanged.value && props.id) {
        await saveChanges();
    }
});
</script>
