<template>
    <Dialog v-model:visible="visibleModel" class="w-fit" header="Создать папку" modal>
        <div class="flex flex-col justify-center items-end gap-2">
            <div class="card flex flex-col justify-center gap-2">
                <InputGroup>
                    <InputGroupAddon>
                        <i class="pi pi-tag"></i>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText id="folderName" v-model="newFolderName" autocomplete="off"/>
                        <label for="folderName">Название папки</label>
                    </FloatLabel>
                </InputGroup>

                <InputGroup>
                    <InputGroupAddon>
                        <i class="pi pi-folder"></i>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <Select id="folderLocation"
                                v-model="selectedFolderLocation"
                                :options="dashboardStore.formattedFolders(ExperimentKind.ANY).value"
                                class="w-full"
                                optionLabel="path"
                        />
                        <label for="folderLocation">Путь</label>
                    </FloatLabel>
                </InputGroup>
            </div>
        </div>
        <template #footer>
            <Button class="p-button-secondary" label="Отмена" @click="visibleModel = false"/>
            <Button :disabled="!newFolderName" class="p-button-primary" label="Создать" @click="createFolder"/>
        </template>
    </Dialog>
</template>

<script lang="ts" setup>
import {Button, Dialog, FloatLabel, InputGroup, InputGroupAddon, InputText, Select} from "primevue"
import {ref} from "vue"

import {findById} from "@/views/utils"
import {ExperimentKind, Folder, SimplifiedView} from "@/views/Dashboard/typing"
import {useDashboardStore} from '@/stores/dashboard'

const dashboardStore = useDashboardStore()
const visibleModel = dashboardStore.getVisibleModel(dashboardStore.createFolderDialog)

const newFolderName = ref('')
const selectedFolderLocation = ref<SimplifiedView | null>(null)


const createFolder = () => {
    if (!newFolderName.value) return

    const newFolder: Folder = {
        id: crypto.randomUUID(),
        path: newFolderName.value,
        children: []
    }

    if (selectedFolderLocation.value) {
        const parentFolder = findById(dashboardStore.experimentFS, selectedFolderLocation.value.id) as Folder
        if (parentFolder) {
            parentFolder.children.push(newFolder)
        }
    } else {
        dashboardStore.experimentFS.push(newFolder)
    }

    visibleModel.value = false
}
</script>

