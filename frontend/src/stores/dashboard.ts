import { defineStore } from 'pinia';
import { computed, ComputedRef, ref, watch } from 'vue';
import { Experiment, ExperimentKind, FileSystem, Folder, SimplifiedView } from '@/views/Dashboard/typing';
import { findParent, getFullPath, getSuggestedFolders } from '@/views/utils';
import api from '@/api/axios';
import { useCoreStore } from '@/stores/core';

interface DialogState {
    visible: boolean;
}

export const useDashboardStore = defineStore('dashboard',
    {
        state: () => ({
            createExperimentDialog: { visible: false } as DialogState,
            createFolderDialog: { visible: false } as DialogState,
            moveExperimentDialog: { visible: false } as DialogState,
            selectedExperiment: null as (Experiment | null),
            experimentFS: ref<FileSystem | null>(null)
        }),
        getters: {
            currentFolder: (state): Folder | null => {
                return findParent(state.experimentFS, state.selectedExperiment.id);
            }
        },
        actions: {
            getVisibleModel(dialogState: DialogState) {
                const visible = ref(dialogState.visible);

                watch(visible, (newValue) => {
                    dialogState.visible = newValue;
                });

                watch(() => dialogState.visible, (newValue) => {
                    visible.value = newValue;
                });

                return visible;
            },
            formattedFolders(kind: ExperimentKind): ComputedRef {
                return computed(() => {
                    return getSuggestedFolders(this.experimentFS, kind).map((folder: SimplifiedView) => ({
                        ...folder,
                        path: getFullPath(this.experimentFS, folder)
                    }));
                });
            },
            async fetchExperimentFS() {
                if (this.experimentFS) {
                    return
                }

                try {
                    const coreStore = useCoreStore();
                    const params = new URLSearchParams();
                    const desired_keys = ['id', 'kind'];

                    params.append('username', coreStore.username);
                    for (const key of desired_keys) {
                        params.append('desired_keys', key)
                    }

                    const response = await api.get<FileSystem>(`experiment/?${params.toString()}`);
                    this.experimentFS = response.data;
                } catch (error) {
                    console.error('Ошибка загрузки experimentFS:', error);
                }
            }
        }
    });
