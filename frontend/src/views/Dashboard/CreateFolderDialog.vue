<template>
    <Dialog v-model:visible="props.visibleModel.visible" class="w-fit" header="Создать папку" modal>
        <div class="flex flex-col justify-center items-end gap-2">
            <div class="card flex flex-col justify-center gap-2">
                <InputGroup>
                    <InputGroupAddon>
                        <i class="pi pi-tag"></i>
                    </InputGroupAddon>
                    <FloatLabel variant="on">
                        <InputText id="folderName" v-model="newFolderName" autocomplete="off" />
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
                                :options="formattedFolders(props.fs).value.concat([{path: '/', id: '-1'}])"
                                class="w-full"
                                optionLabel="path"
                        />
                        <label for="folderLocation">Путь</label>
                    </FloatLabel>
                </InputGroup>
            </div>
        </div>
        <template #footer>
            <Button class="p-button-secondary" label="Отмена" @click="props.visibleModel.visible = false" />
            <Button :disabled="!newFolderName" class="p-button-primary" label="Создать" @click="createFolder" />
        </template>
    </Dialog>
</template>

<script lang="ts" setup>
import { Button, Dialog, FloatLabel, InputGroup, InputGroupAddon, InputText, Select } from 'primevue';
import { ref } from 'vue';
import { FileSystem, Folder, SimplifiedView } from '@/views/Dashboard/typing';
import { findById } from '@/utils/fileSystem';
import { DialogState, useDashboard } from '@/composables/useDashboard';

interface Props {
    fs: FileSystem;
    visibleModel: DialogState;
}

const props = defineProps<Props>();
const { formattedFolders } = useDashboard();

const newFolderName = ref('');
const selectedFolderLocation = ref<SimplifiedView | null>(null);


const createFolder = () => {
    if (!newFolderName.value) return;

    const newFolder: Folder = {
        id: crypto.randomUUID(),
        path: newFolderName.value,
        children: []
    };

    if (selectedFolderLocation.value) {
        const parentFolder = findById(props.fs, selectedFolderLocation.value.id) as Folder;
        if (parentFolder) {
            parentFolder.children.push(newFolder);
        } else if (selectedFolderLocation.value.id === '-1') {
            props.fs.push(newFolder);
        }
    }

    props.visibleModel.visible = false;
};
</script>

