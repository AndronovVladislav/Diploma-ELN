<template>
    <Dialog
        v-model:visible="visible"
        class="w-fit"
        header="Создать эксперимент"
        modal
        @hide="onHide"
    >
        <div class="flex flex-col gap-3 px-3 py-4">
            <div class="flex justify-center">
                <i
                    :class="selectedKind === ExperimentKind.LABORATORY ? 'pi-bolt' : 'pi-microchip'"
                    class="pi"
                    style="font-size: 3rem"
                />
            </div>

            <div class="text-center text-xl">
                <label class="block font-bold mb-1" for="experimentKind">Тип эксперимента</label>
                <SelectButton
                    id="experimentKind"
                    v-model="selectedKind"
                    :allowEmpty=false
                    :options="experimentKinds"
                    optionLabel="label"
                    optionValue="value"
                />
            </div>

            <InputGroup>
                <InputGroupAddon>
                    <i class="pi pi-tag"></i>
                </InputGroupAddon>
                <FloatLabel variant="on">
                    <InputText
                        id="experimentName"
                        v-model="experimentName"
                        class="w-full"
                    />
                    <label class="block font-bold mb-1" for="experimentName">Название эксперимента</label>
                </FloatLabel>
            </InputGroup>

            <InputGroup>
                <InputGroupAddon>
                    <i class="pi pi-folder"></i>
                </InputGroupAddon>
                <FloatLabel variant="on">
                    <Select
                        id="experimentFolder"
                        v-model="selectedFolder"
                        :options="formattedFolders(experimentFS).value.concat([{path: '/', id: '-1'}])"
                        class="w-full"
                        optionLabel="path"
                    />
                    <label class="block font-bold mb-1" for="experimentFolder">Путь</label>
                </FloatLabel>
            </InputGroup>
        </div>

        <template #footer>
            <Button class="p-button-text" label="Отмена" @click="onHide" />
            <Button class="p-button p-button-success" label="Создать" @click="onCreateExperiment" />
        </template>
    </Dialog>
</template>

<script lang="ts" setup>
import { Button, Dialog, FloatLabel, InputGroup, InputGroupAddon, InputText, Select } from 'primevue';
import { ref } from 'vue';

import { useDashboard } from '@/composables/useDashboard';
import { Experiment, ExperimentKind, Folder, SimplifiedView } from '@/views/Dashboard/typing';
import { findById } from '@/utils/fileSystem';
import api from '@/api/axios';

const { getVisibleModel, createExperimentDialog, experimentFS, formattedFolders } = useDashboard();

const visible = getVisibleModel(createExperimentDialog.value);

const experimentName = ref('');
const selectedKind = ref(ExperimentKind.LABORATORY);
const selectedFolder = ref<SimplifiedView | null>(null);

const experimentKinds = [
    { label: 'Лабораторный', value: ExperimentKind.LABORATORY },
    { label: 'Вычислительный', value: ExperimentKind.COMPUTATIONAL }
];

function onHide() {
    visible.value = false;
    experimentName.value = '';
    selectedKind.value = ExperimentKind.LABORATORY;
    selectedFolder.value = null;
}

async function onCreateExperiment() {
    try {
        const prefix = selectedFolder.value?.path === '/' ? '' : `/${selectedFolder.value?.path}`;
        const response = await api.post('/experiment', {
            path: `${prefix}/${experimentName.value}`,
            kind: selectedKind.value
        });

        const newExperiment: Experiment = {
            id: response.data.id,
            path: experimentName.value,
            createdAt: new Date().toISOString(),
            kind: selectedKind.value
        };

        if (selectedFolder.value) {
            const parentFolder = findById(experimentFS.value, selectedFolder.value.id) as Folder;
            if (parentFolder) {
                parentFolder.children.push(newExperiment);
            } else if (selectedFolder.value.id === '-1') {
                experimentFS.value.push(newExperiment);
            }
        }

        onHide();
    } catch (error) {
        console.error(error);
    }
}
</script>
