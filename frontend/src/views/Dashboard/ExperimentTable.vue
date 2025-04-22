<template>
    <div class="mb-6">
        <TreeTable
            v-if="experimentFS"
            :value="experimentFS"
            class="w-full"
            data-key="path"
        >
            <Column expander field="title" header="Название">
                <template #body="{ node }">
                    <span v-if="node.children && node.children.length" class="font-semibold">
                        {{ node.path }}
                    </span>
                    <Button v-else-if="node.kind" class="p-button-text p-0" @click="goToExperiment(node.id)">
                        {{ node.path }}
                    </Button>
                    <span v-else class="font-semibold text-gray-400">
                        {{ node.path }} (пустая папка)
                    </span>
                </template>
            </Column>

            <Column header="Тип">
                <template #body="{ node }">
                    <Tag v-if="node.kind" :severity="node.kind === ExperimentKind.LABORATORY ? 'info' : 'success'">
                        {{ node.kind }}
                    </Tag>
                </template>
            </Column>

            <Column header="Действия">
                <template #body="{ node }">
                    <ExperimentActions
                        v-if="node.kind"
                        :experiment-id="node.id"
                    />
                </template>
            </Column>
        </TreeTable>

        <CreateExperimentDialog />
        <CreateFolderDialog :fs="experimentFS" :visible-model="createExperimentsFolderDialog" />
        <MoveDialog
            :fs="experimentFS"
            :visible-model="moveExperimentDialog"
            :selected-item="selectedExperiment"
        />
    </div>
</template>

<script lang="ts" setup>
import { Button, Column, TreeTable } from 'primevue';

import ExperimentActions from '@/views/Dashboard/ExperimentActions.vue';
import { ExperimentKind } from '@/views/Dashboard/typing';
import { useDashboard } from '@/composables/useDashboard';
import router from '@/router';
import CreateFolderDialog from '@/views/Dashboard/CreateFolderDialog.vue';
import MoveDialog from '@/views/Dashboard/MoveDialog.vue';
import CreateExperimentDialog from '@/views/Dashboard/CreateExperimentDialog.vue';

const { experimentFS, moveExperimentDialog, selectedExperiment, createExperimentsFolderDialog } = useDashboard();

const goToExperiment = (id: string) => {
    if (!id) return;

    router.push(`/experiment/${id}`);
};
</script>
