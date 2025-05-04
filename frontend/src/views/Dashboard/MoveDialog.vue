<template>
    <Dialog v-model:visible="visibleModel.visible" header="Перемещение" modal>
        <p>Выберите новую папку для "<strong>{{ props.selectedItem?.path }}</strong>":</p>

        <Select v-model="selectedFolder"
                :options="formattedFolders(props.fs).value"
                class="w-full mt-2"
                option-label="path"
                placeholder="Выберите папку"
        />

        <div class="flex justify-end mt-4 gap-2">
            <Button label="Отмена" severity="secondary" @click="visibleModel.visible = false" />
            <Button :disabled="!selectedFolder" label="Переместить" severity="success" @click="confirmMove" />
        </div>
    </Dialog>
</template>

<script lang="ts" setup>
import { Button, Dialog, Select } from 'primevue';
import { ref, watch } from 'vue';
import { Experiment, ExperimentKind, FileSystem, Folder, SimplifiedView, Template } from '@/views/Dashboard/typing';
import { DialogState, useDashboard } from '@/composables/useDashboard';
import { findById, getFullPath, removeFromFS } from '@/utils/fileSystem';
import api from '@/api/axios';
import { useNotifier } from '@/composables/useNotifier';

interface Props {
    fs: FileSystem;
    visibleModel: DialogState;
    selectedItem: Experiment | Template | null;
}

const props = defineProps<Props>();

const { formattedFolders, currentFolder } = useDashboard();
const Notifier = useNotifier();

const selectedFolder = ref<SimplifiedView | null>(null);

watch(() => props.visibleModel, (newVal) => {
    if (!newVal) {
        selectedFolder.value = null;
    }
});

const confirmMove = async () => {
    if (!props.selectedItem || !selectedFolder.value) return;

    const targetFolder = findById(props.fs, selectedFolder.value.id) as Folder;
    const curFolder = currentFolder(props.fs, props.selectedItem) as Folder;
    if (curFolder?.id === targetFolder.id) {
        return;
    }

    removeFromFS(props.fs, props.selectedItem.id);
    if (targetFolder) {
        targetFolder.children.push(props.selectedItem);
    }

    try {
        const newPath = '/' + getFullPath(props.fs, props.selectedItem);
        const url = 'kind' in props.selectedItem
            ? `experiment/${props.selectedItem.kind === ExperimentKind.LABORATORY ? 'laboratory' : 'computational'}`
            : 'template';
        await api.patch(`${url}/${props.selectedItem.id}`, { path: newPath });
    } catch (error) {
        console.error('Ошибка при перемещении:', error);
        Notifier.error({ detail: error instanceof Error ? error.message : 'Неизвестная ошибка' });
    }
    props.visibleModel.visible = false;
};
</script>
