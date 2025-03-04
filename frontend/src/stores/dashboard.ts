import {defineStore} from 'pinia'
import {computed, ComputedRef, ref, watch} from "vue"
import {Experiment, ExperimentKind, FileSystem, Folder, SimplifiedView} from "@/views/Dashboard/typing"
import {findParent, getFullPath, getSuggestedFolders} from "@/views/Dashboard/utils"

interface DialogState {
    visible: boolean
}

export const useDashboardStore = defineStore('dashboard',
    {
        state: () => ({
            createExperimentDialog: {visible: false} as DialogState,
            createFolderDialog: {visible: false} as DialogState,
            moveExperimentDialog: {visible: false} as DialogState,
            selectedExperiment: null as (Experiment | null),
        }),
        getters: {
            currentFolder: (state): Folder | null => {
                return findParent(state.experimentFS, state.selectedExperiment.id)
            },
            experimentFS: (): FileSystem => {
                // TODO: переделать на вызов в API
                return ref([
                    {
                        'children': [
                            {
                                'children': [
                                    {
                                        'createdAt': '2024-01-15',
                                        'id': 'c47abfbc-d883-43d2-bd98-4d32de87d81e',
                                        'kind': ExperimentKind.LABORATORY,
                                        'path': 'Метод титрования'
                                    },
                                    {
                                        'createdAt': '2024-01-20',
                                        'id': '2536b9cf-c156-4d63-b60f-9f39d630b923',
                                        'kind': ExperimentKind.LABORATORY,
                                        'path': 'Электродный метод'
                                    }],
                                'path': 'Анализ pH воды',
                                'id': 'f0-0'
                            },
                            {
                                'children': [
                                    {
                                        'createdAt': '2024-02-18',
                                        'id': '30a80803-7f5d-491c-af2d-efc765ad545d',
                                        'kind': ExperimentKind.LABORATORY,
                                        'path': 'Метод атомной абсорбции'
                                    },
                                    {
                                        'createdAt': '2024-02-20',
                                        'id': '33354677-f48b-4607-a8ec-12c344cdebbb',
                                        'kind': ExperimentKind.LABORATORY,
                                        'path': 'Флуоресцентный анализ'
                                    }],
                                'path': 'Определение концентрации ионов',
                                'id': 'f0-1'
                            }
                        ],
                        'path': 'Химические исследования',
                        'id': 'f0'
                    },
                    {
                        'children': [
                            {
                                'createdAt': '2024-01-25',
                                'id': '10c14877-bfe9-4ad6-9c77-a4f39338c983',
                                'kind': ExperimentKind.LABORATORY,
                                'path': 'Исследование теплопроводности металлов'
                            },
                            {
                                'children': [
                                    {
                                        'createdAt': '2024-02-15',
                                        'id': '511125a2-5234-4de2-a4a5-1ad56acf63cf',
                                        'kind': ExperimentKind.LABORATORY,
                                        'path': 'Измерение показателя преломления'
                                    }
                                ],
                                'path': 'Оптические свойства материалов',
                                'id': 'f1-0'
                            }],
                        'path': 'Физические эксперименты',
                        'id': 'f1'
                    },
                    {
                        'children': [
                            {
                                'createdAt': '2024-03-01',
                                'id': '95f28c50-e32f-41f5-a9b7-d64279257d09',
                                'kind': ExperimentKind.COMPUTATIONAL,
                                'path': 'Моделирование структуры белка'
                            },
                            {
                                'children': [
                                    {
                                        'createdAt': '2024-04-05',
                                        'id': 'ab6b4c3a-bb4d-46f5-8bc8-fd4161b475bb',
                                        'kind': ExperimentKind.COMPUTATIONAL,
                                        'path': 'DFT-методы'
                                    }
                                ],
                                'path': 'Квантово-химические расчёты',
                                'id': 'f2-0'
                            }
                        ],
                        'path': 'Моделирование молекул',
                        'id': 'f2'
                    },
                    {
                        'children': [
                            {
                                'children': [
                                    {
                                        'createdAt': '2024-05-05',
                                        'id': '4871f50c-b26c-4947-b3ca-be0bf221fc77',
                                        'kind': ExperimentKind.LABORATORY,
                                        'path': 'Метод Sanger'
                                    }
                                ],
                                'path': 'Секвенирование ДНК',
                                'id': 'f3-0'
                            }
                        ],
                        'path': 'Биологические исследования',
                        'id': 'f3'
                    }
                ]).value
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

                return visible
            },
            formattedFolders(kind: ExperimentKind): ComputedRef {
                return computed(() => {
                    return getSuggestedFolders(this.experimentFS, kind).map((folder: SimplifiedView) => ({
                        ...folder,
                        path: getFullPath(this.experimentFS, folder)
                    }))
                })
            }
        }
    })
