<template>
    <div class="mb-6">
        <TreeTable
            v-if="dashboardStore.experimentFS.length"
            :value="dashboardStore.experimentFS"
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
    </div>
</template>

<script lang="ts" setup>
import {Button, Column, TreeTable} from 'primevue'

import ExperimentActions from '@/views/Dashboard/ExperimentActions.vue'
import {ExperimentKind} from '@/views/Dashboard/typing'
import {useDashboardStore} from '@/stores/dashboard'

const dashboardStore = useDashboardStore()

const goToExperiment = (id: string) => {
    if (!id) return
}
</script>
