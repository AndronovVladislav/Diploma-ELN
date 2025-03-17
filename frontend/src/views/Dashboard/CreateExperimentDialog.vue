<template>
    <Dialog
        v-model:visible="visible"
        header="Создать эксперимент"
        class="w-fit"
        modal
        @hide="onHide"
    >
        <div class="flex flex-col gap-3 px-3 py-4">
            <div class="flex justify-center">
                <i
                    class="pi"
                    :class="selectedKind === ExperimentKind.LABORATORY ? 'pi-bolt' : 'pi-microchip'"
                    style="font-size: 3rem"
                />
            </div>

            <div class="text-center text-xl">
                <label for="experimentKind" class="block font-bold mb-1">Тип эксперимента</label>
                <SelectButton
                    id="experimentKind"
                    v-model="selectedKind"
                    :options="experimentKinds"
                    :allowEmpty=false
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
                    <label for="experimentName" class="block font-bold mb-1">Название эксперимента</label>
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
                        :options="dashboardStore.formattedFolders(ExperimentKind.ANY).value"
                        optionLabel="path"
                        class="w-full"
                    />
                    <label for="experimentFolder" class="block font-bold mb-1">Путь</label>
                </FloatLabel>
            </InputGroup>
        </div>

        <template #footer>
            <Button label="Отмена" class="p-button-text" @click="onHide"/>
            <Button label="Создать" class="p-button p-button-success" @click="onCreateExperiment"/>
        </template>
    </Dialog>
</template>

<script setup lang="ts">
import {Button, Dialog, FloatLabel, InputGroup, InputGroupAddon, InputText, Select} from "primevue"
import {computed, ref} from 'vue'

import {useDashboardStore} from '@/stores/dashboard'
import {Experiment, ExperimentKind, Folder, SimplifiedView} from '@/views/Dashboard/typing'
import {findById} from "@/views/utils";

const dashboardStore = useDashboardStore()

const visible = dashboardStore.getVisibleModel(dashboardStore.createExperimentDialog)

const experimentName = ref('')
const selectedKind = ref(ExperimentKind.LABORATORY)
const selectedFolder = ref<SimplifiedView | null>(null)

const experimentKinds = [
    {label: 'Лабораторный', value: ExperimentKind.LABORATORY},
    {label: 'Вычислительный', value: ExperimentKind.COMPUTATIONAL}
]

function onHide() {
    visible.value = false
    experimentName.value = ''
    selectedKind.value = ExperimentKind.LABORATORY
    selectedFolder.value = null
}

function onCreateExperiment() {
    const newExperiment: Experiment = {
        id: crypto.randomUUID(),
        path: experimentName.value,
        createdAt: new Date().toISOString(),
        kind: selectedKind.value
    };

    if (selectedFolder.value) {
        const parentFolder = findById(dashboardStore.experimentFS, selectedFolder.value.id) as Folder
        if (parentFolder) {
            parentFolder.children.push(newExperiment)
        }
    } else {
        dashboardStore.experimentFS.push(newExperiment)
    }

    onHide()
}
</script>
