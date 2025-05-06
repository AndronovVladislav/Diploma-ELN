import { computed, ref, watch } from 'vue';
import type { Experiment, FileSystem, Folder, SimplifiedView, Template } from '@/views/Dashboard/typing';
import { findParent, getFullPath, getSuggestedFolders } from '@/utils/fileSystem';
import api from '@/api/axios';

export interface DialogState {
    visible: boolean;
}

const createExperimentDialog = ref<DialogState>({ visible: false });
const createExperimentsFolderDialog = ref<DialogState>({ visible: false });
const createTemplatesFolderDialog = ref<DialogState>({ visible: false });
const createTemplateDialog = ref<DialogState>({ visible: false });
const viewTemplateDialog = ref<DialogState>({ visible: false });
const moveExperimentDialog = ref<DialogState>({ visible: false });
const moveTemplateDialog = ref<DialogState>({ visible: false });

const selectedExperiment = ref<Experiment | null>(null);
const selectedTemplate = ref<Template | null>(null);

const experimentFS = ref<FileSystem>([]);
const templateFS = ref<FileSystem>([]);


export function useDashboard() {
    function getVisibleModel(dialogState: DialogState) {
        const visible = ref(dialogState.visible);

        watch(visible, (newValue) => {
            dialogState.visible = newValue;
        });

        watch(() => dialogState.visible, (newValue) => {
            visible.value = newValue;
        });

        return visible;
    }

    function formattedFolders(fs: FileSystem) {
        return computed(() => {
            return getSuggestedFolders(fs).map((folder: SimplifiedView) => ({
                ...folder,
                path: getFullPath(fs, folder)
            }));
        });
    }

    async function fetchExperimentFS() {
        try {
            const params = new URLSearchParams();
            const desired_keys = ['id', 'kind'];

            for (const key of desired_keys) {
                params.append('desired_keys', key);
            }

            const response = await api.get<FileSystem>(`/experiment/?${params.toString()}`);
            experimentFS.value = response.data;
        } catch (error) {
            console.error('Ошибка загрузки experimentFS:', error);
        }
    }

    async function fetchTemplateFS() {
        try {
            const response = await api.get<FileSystem>(`/template/`);
            templateFS.value = response.data;
        } catch (error) {
            console.error('Ошибка загрузки templateFS:', error);
        }
    }

    function currentFolder(fs: FileSystem, item: Experiment | Template | null): Folder | null {
        if (!item) return null;
        return findParent(fs, item.id);
    }

    function currentExperimentFolder(): Folder | null {
        return currentFolder(experimentFS.value, selectedExperiment.value);
    }

    function currentTemplateFolder(): Folder | null {
        return currentFolder(templateFS.value, selectedTemplate.value);
    }

    return {
        createExperimentDialog,
        createExperimentsFolderDialog,
        createTemplatesFolderDialog,
        createTemplateDialog,
        viewTemplateDialog,
        moveExperimentDialog,
        moveTemplateDialog,
        selectedExperiment,
        selectedTemplate,
        experimentFS,
        templateFS,
        getVisibleModel,
        formattedFolders,
        fetchExperimentFS,
        fetchTemplateFS,
        currentFolder,
        currentExperimentFolder,
        currentTemplateFolder
    };
}
